import pkgutil
from argparse import ArgumentParser

from rich.markdown import Markdown
from rich.panel import Panel
from rich_argparse import RichHelpFormatter

from cx_core.app import AbstractApp, LogLevel
from cx_core.filesystem import PathExpander
from .worker import *


class SubConvApp(AbstractApp):
    APP_VERSION = "0.2.5"
    APP_NAME = "subconv"

    def __init__(self):
        super(SubConvApp, self).__init__()

        _parser = ArgumentParser(prog=SubConvApp.APP_NAME,
                                 description=f'批量提取台词本，支持的格式包括{" ".join(Worker.acceptable_suffixes())}',
                                 epilog=f'Version {SubConvApp.APP_VERSION} Designed by xiii_1991',
                                 formatter_class=RichHelpFormatter, exit_on_error=False)

        _parser.add_argument('--format', '-f', dest='format', default='txt',
                             choices=Worker.supported_formats(),
                             help='指定输出格式', metavar='格式代码')

        _parser.add_argument('--appending', '-a', dest='appending', default=None,
                             help='为目标文件添加后缀', metavar='后缀字符串')

        _parser.add_argument('--encoding', '-c', dest='target_encoding', default='auto',
                             help='设定输出编码', metavar='目标编码')

        _parser.add_argument('--force-decoding', dest='source_encoding', default=None,
                             help='强制指定读取编码', metavar='来源编码')

        _parser.add_argument('-o', '--output-dir', dest='target_dir', default=None,
                             help='指定输出目录', metavar='目录')

        _parser.add_argument('--sub-dir', dest='sub_dir', default=None,
                             help='指定子目录', metavar='子目录')

        _parser.add_argument('-t', '--time', dest='keep_time', action='store_true',
                             help='尽量保留时间信息')

        _parser.add_argument('--bypass-formatter', dest='bypass_formatter', default=False,
                             action='store_true', help='跳过默认的内容检查器，使用原样输出')

        _parser.add_argument('--overwrite', '-y', dest='overwrite_target', default=False,
                             action='store_true', help='强制覆盖已存在的目标文件')

        _parser.add_argument('--translate', dest='translate', action='store_true',
                             help='自动翻译为英文版本（需要网络）')

        _parser.add_argument('--debug', '-d', action='store_true', dest='debug',
                             help='调试模式')

        _parser.add_argument('--pretend', '-p', dest='pretend_mode', action='store_true',
                             help='干转模式，不执行写入操作')

        _parser.add_argument('--full-help', help='显示详细的说明',
                             dest='show_full_help', action='store_true')

        _parser.add_argument('sources', nargs='*',
                             help='需要转换的文件', metavar='文件列表')

        self.parser = _parser
        self.profile = None

        self.global_task = None

    def __enter__(self):
        env.start()

        env.info('开始解析参数')
        _args = self.parser.parse_args()
        self.profile = DataPackage(**vars(_args))
        env.debug('解析的参数:', self.profile)

        env.log_level = LogLevel.DEBUG if self.profile.debug else LogLevel.WARNING

        self.global_task = env.progress.add_task(description='全局进度', total=None)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = False

        if exc_type is None:
            env.print('执行完毕，没有发现错误')
        elif issubclass(exc_type, UserCancelError):
            env.error(f'已取消未完成的任务')
            result = True

        env.progress.remove_task(self.global_task)
        self.global_task = None

        env.stop()
        return result

    @staticmethod
    def show_full_help():
        data = pkgutil.get_data('sub_conv', 'help.md').decode('utf-8')
        panel = Panel(Markdown(data), width=80)
        env.console.print(panel)

    def run(self):
        if self.profile.show_full_help:
            self.show_full_help()
            return

        def _validator(p: Path) -> bool:
            sub_dir = self.profile.sub_dir
            suffixes = Worker.acceptable_suffixes()
            if sub_dir and p.parent.name == sub_dir:
                return False
            return p.suffix in suffixes

        expander = PathExpander(self.profile.sources,
                                accept_dir=False,
                                file_validator=_validator)
        env.debug('Expander 已构建')

        env.progress.start_task(self.global_task)
        for source in env.progress.track(expander, task_id=self.global_task):
            if env.wanna_quit:
                raise UserCancelError()
            mission = Mission(source, self.profile)
            env.debug('构建 Mission:', mission)
            env.progress.update(self.global_task, description=mission.name)
            with Worker(mission) as worker:
                worker.process()


def run():
    with SubConvApp() as app:
        app.run()
