import glob
import pkgutil
from argparse import ArgumentParser

from rich.markdown import Markdown
from rich.panel import Panel
from rich_argparse import RichHelpFormatter

from cx_core import DataPackage
from cx_core.app import AbstractApp, LogLevel
from cx_core.filesystem import PathExpander
from .env import env
from .mission_agent import MissionAgent


class BatchCommanderApp(AbstractApp):
    APP_NAME = 'batchcommander'
    APP_VERSION = '0.3.3'

    PROCESSING_MODES = ['file', 'folder', 'none']

    def __init__(self):
        super(BatchCommanderApp, self).__init__()
        parser = ArgumentParser(prog=BatchCommanderApp.APP_NAME,
                                formatter_class=RichHelpFormatter,
                                description='命令批量执行工具',
                                epilog='Designed by xiii_1991')
        parser.add_argument('--verbose', '-v',
                            dest='verbose', default=False, action='store_true',
                            help='显示命令的输出')
        parser.add_argument('--recursive', '-r',
                            dest='recursive', default=False, action='store_true',
                            help='展开各级子目录')
        parser.add_argument('--processing-mode', '-m',
                            default=None, choices=BatchCommanderApp.PROCESSING_MODES, dest='processing_mode',
                            help=f'指定处理模式，可用选项包括: {' '.join(BatchCommanderApp.PROCESSING_MODES)}',
                            metavar='执行模式')
        parser.add_argument('--command', '-c',
                            default='',
                            help='指定需要执行的指令，使用标签标记输入信息，具体参见完整帮助')
        parser.add_argument('--save-script', '-s',
                            dest='script_output', default=None,
                            help='保存为脚本文件', metavar='目标脚本文件')
        parser.add_argument('--full-help',
                            dest='show_full_help', default=False, action='store_true',
                            help='显示完整帮助')
        parser.add_argument('sources',
                            nargs='*',
                            help='指定需要处理的路径', metavar='路径列表')
        parser.add_argument('--debug', '-d', action='store_true', dest='debug',
                            help='调试模式')

        parser.add_argument('--pretend', '-p', dest='pretend_mode', action='store_true',
                            help='干转模式，不执行操作')

        self._parser = parser
        self.profile = None
        self.global_task = None

        self._target_script = None

    def __enter__(self):
        env.start()
        env.print(f'[yellow]{BatchCommanderApp.APP_NAME}[/yellow] [blue]{BatchCommanderApp.APP_VERSION}[/blue]')
        env.info('解析参数')
        _args = self._parser.parse_args()
        self.profile = DataPackage(**vars(_args))
        env.log_level = LogLevel.DEBUG if self.profile.debug else LogLevel.WARNING
        env.debug('解析的参数', self.profile)
        self.global_task = env.progress.add_task(description='全局任务', total=None)

        if self.profile.script_output is not None:
            self._target_script = open(self.profile.script_output, 'wt', encoding='utf-8')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = False
        if exc_type is None:
            env.print('执行完毕，没有发现错误')

        if self._target_script:
            self._target_script.flush()
            self._target_script.close()
        env.progress.remove_task(self.global_task)
        env.stop()
        return result

    @staticmethod
    def show_full_help():
        data = pkgutil.get_data('batch_commander', 'help.md').decode('utf-8')
        panel = Panel(Markdown(data), width=80)
        env.console.print(panel)

    @property
    def _plans(self):
        sources = []
        for x in self.profile.sources:
            sources += glob.glob(x)
        expander = PathExpander(sources,
                                existed_only=True,
                                search_subdir=self.profile.recursive,
                                accept_file=self.profile.processing_mode != 'folder',
                                accept_dir=self.profile.processing_mode != 'file'
                                )
        yield from expander

    def run(self):
        if self.profile.show_full_help:
            BatchCommanderApp.show_full_help()
            return

        if not self.profile.sources:
            env.error('没有指定待处理的文件')
            return

        if not self.profile.command:
            env.warning('未指定操作命令，将直接打印输入的文件')

        env.progress.start_task(self.global_task)
        for plan in env.progress.track(self._plans, task_id=self.global_task):
            agent = MissionAgent(self.profile, plan)
            env.progress.update(self.global_task, description=agent.source_name)
            if self._target_script:
                self._target_script.write(f'{agent.compiled_cmd}\n')
            else:
                agent.run()
            if env.wanna_quit:
                env.print('正在取消后续任务')
                break
            env.print(f'[yellow]{agent.source}[/yellow] 处理完成')


def run():
    with BatchCommanderApp() as app:
        app.run()
