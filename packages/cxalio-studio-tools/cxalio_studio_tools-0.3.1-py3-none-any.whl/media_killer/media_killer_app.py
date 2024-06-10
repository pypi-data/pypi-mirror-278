import pkgutil
from argparse import ArgumentParser, ArgumentError

from rich.markdown import Markdown
from rich.panel import Panel
from rich_argparse import RichHelpFormatter

from cx_core import DataPackage
from cx_core.app import AbstractApp
from cx_core.app import LogLevel
from cx_core.filesystem import normalize_path, force_suffix
from cx_core.tui import JobCounter
from .env import env
from .exceptions import *
from .mission import MissionMaker
from .profile_loader import ProfileLoader
from .script_writer import ScriptWriter
from .task_inspector import TaskInspector
from .transcoder import Transcoder


class MediaKillerApp(AbstractApp):
    APP_VERSION = '0.2.7'
    APP_NAME = 'mediakiller'

    def __init__(self):
        super(MediaKillerApp, self).__init__()
        self.global_task = None

        parser = ArgumentParser(prog=MediaKillerApp.APP_NAME, formatter_class=RichHelpFormatter,
                                description='基于配置文件的批量转码工具',
                                epilog=f'Version {MediaKillerApp.APP_VERSION} Designed by xiii_1991')
        parser.add_argument('profile', help='指定配置文件路径', default=None, nargs='?')
        parser.add_argument('-g', '--generate-example-profile',
                            action="store_true", dest='generate_example',
                            help='生成范例文件')
        parser.add_argument('-a', '--add-source',
                            action='append', dest='sources', metavar='SOURCE_FILE',
                            help='增加来源文件')
        parser.add_argument('-s', '--make-script',
                            dest='script_output', metavar='SCRIPT_OUTPUT',
                            help='生成对应的脚本文件')
        parser.add_argument('-d', '--debug',
                            action='store_true', dest='debug', help='显示调试信息')
        parser.add_argument('--pretend', '-p',
                            dest='pretend_mode', action='store_true', help='空转模式，不执行命令')
        parser.add_argument('--full-help', help='显示详细的说明',
                            dest='full_help', action='store_true')
        parser.add_argument('-v', '--version', action='version', version=MediaKillerApp.APP_VERSION,
                            help='显示软件版本信息')
        self.profile = None
        self._parser = parser
        self.args = None

    @staticmethod
    def show_full_help():
        """显示完整的说明文件"""
        data = pkgutil.get_data('media_killer', 'help.md').decode('utf_8')
        panel = Panel(Markdown(data), width=80)
        env.console.print(panel)

    @staticmethod
    def copy_example_profile(tgt):
        tgt = normalize_path(tgt)
        tgt = force_suffix(tgt, '.toml')
        data = pkgutil.get_data('media_killer', 'example_project.toml')
        try:
            with open(tgt, 'xb') as file:
                file.write(data)
            env.print(f'模板配置文件已保存到 {env.args.profile} ，[red]请在修改后运行！[/red]')
        except FileExistsError:
            env.error('文件 {0} 已存在，[red]请手动删除它，或指定其它的目标文件[/red]'.format(tgt))

    def __enter__(self):
        env.start()
        env.debug('env 环境已启动')

        _args = self._parser.parse_args()
        self.args = DataPackage(**vars(_args))
        env.debug('解析命令行参数：', self.args)

        env.log_level = LogLevel.DEBUG if self.args.debug else LogLevel.WARNING
        env.args = self.args

        self.global_task = env.progress.add_task(description='全局进度', start=False, visible=False)
        env.debug('构建全局进度条')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        env.progress.stop_task(self.global_task)
        env.progress.remove_task(self.global_task)
        self.global_task = None
        env.debug('删除全局进度条')

        result = False
        if exc_type is None:
            pass
        elif issubclass(exc_type, ProfileNoFoundError):
            env.critical(exc_val)
            result = True
        elif issubclass(exc_type, ArgumentError):
            env.error('参数输入有误:', exc_val)
            result = True
        elif issubclass(exc_type, MediaKillerError):
            env.error(f'[red]{exc_val}[/red]')
            result = True

        env.stop()
        return result

    def run(self):
        if env.args.full_help:
            env.info('检测到 full_help 设置，打印帮助文件并退出')
            MediaKillerApp.show_full_help()
            return

        if not env.args.profile:
            env.info('未检测到项目文件选项')
            raise ProfileNoFoundError()

        if env.args.generate_example:
            env.info('检测到 "--generate-example" 参数，将拷贝配置文件模板')
            env.progress.update(task_id=self.global_task, description='正在输出配置文件', visible=True)
            self.copy_example_profile(env.args.profile)
            return

        with ProfileLoader(env.args.profile) as profile_loader:
            datas = profile_loader.load()
            self.profile = datas
        env.info('配置信息已初始化')

        if not self.profile.source.files:
            raise NoSourceError()

        plans = []
        with TaskInspector(self.profile) as inspector:
            plans = inspector.make_plans(self.profile.source.files)

        if not plans:
            raise NoPlansError()
        env.print(f'探测到 {len(plans)} 个源文件')

        env.debug('构建 mission maker')
        mission_maker = MissionMaker(self.profile)

        if env.args.script_output is not None:
            env.progress.update(task_id=self.global_task, description='输出脚本文件', visible=True)
            env.info('检测到 "--make-script" 参数，将进行脚本输出')
            output_file = normalize_path(env.args.script_output)
            with ScriptWriter(output_file) as writer:
                for mission in env.progress.track(mission_maker(plans), description=env.args.script_output):
                    writer.write_mission(mission)
            env.print(f'已输出脚本文件 "{env.args.script_output}"')
            return

        env.progress.update(self.global_task, description='总体进度', visible=True, total=len(plans))
        env.progress.start_task(self.global_task)

        job_counter = JobCounter(len(plans))
        for mission in mission_maker(plans):
            job_counter.advance()
            if env.wanna_quit:
                env.print('正在取消未完成的任务...')
                raise UserCanceledError()
            if env.args.pretend_mode:
                env.print(f'模拟运行: [yellow]{mission.source.name}[/yellow] 完毕')
            else:
                with Transcoder(mission) as coder:
                    coder.run()
            env.progress.advance(self.global_task)
            env.print(f'[yellow]{job_counter}[/yellow] [cyan]{mission.source.name}[/cyan] 转换完成')


def run():
    with MediaKillerApp() as media_killer:
        media_killer.run()
