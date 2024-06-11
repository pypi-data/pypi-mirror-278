import glob
import pkgutil
from argparse import ArgumentParser, ArgumentError
from pathlib import Path

from rich.markdown import Markdown
from rich.panel import Panel
from rich_argparse import RichHelpFormatter

from cx_core import DataPackage
from cx_core.app import AbstractApp, LogLevel
from cx_core.filesystem import PathExpander
from cx_core.tui import JobCounter
from cx_image import ColorSpaceProcessor
from cx_image import ImageConverter
from .convert_agent import ConvertAgent
from .env import env


class JpeggerApp(AbstractApp):
    APP_VERSION = "0.3.2"
    APP_NAME = "jpegger"

    def __init__(self):
        super(JpeggerApp, self).__init__()

        parser = ArgumentParser(prog=JpeggerApp.APP_NAME,
                                description=f"批量转换图像文件，支持的格式包括：{' '.join(ImageConverter.ACCEPTABLE_OUTPUT_FORMATS.keys())}",
                                epilog=f'Version {JpeggerApp.APP_VERSION} Designed by xiii_1991',
                                formatter_class=RichHelpFormatter, exit_on_error=False)

        parser.add_argument('--format', '-f', dest='format', default='JPEG',
                            choices=ImageConverter.ACCEPTABLE_OUTPUT_FORMATS.keys(),
                            help=f'指定目标格式:[ {' | '.join(ImageConverter.ACCEPTABLE_OUTPUT_FORMATS.keys())} ]',
                            metavar='格式代码')

        parser.add_argument('--recursive', '-r', dest='recursive', default=True,
                            action='store_true',
                            help='迭代输入路径中的子目录')

        parser.add_argument('--output', '-o', dest='output_dir', default='.',
                            help='指定目标目录', metavar='目标目录')

        parser.add_argument('--keep-parent', '-k', dest='keep_parent', default=False,
                            action='store_true',
                            help='为目标保留源文件的上级文件夹')

        parser.add_argument('--max-size', '-s', dest='max_size', default=None,
                            help='限制图像尺寸', metavar='尺寸')

        parser.add_argument('--resize-mode', '-m', dest='resize_mode', default='auto',
                            choices=ConvertAgent.RESIZE_MODES,
                            help=f'设置图片缩放方式:[ {' | '.join(ConvertAgent.RESIZE_MODES)} ]', metavar='模式代码')

        parser.add_argument('--color-space', '-c', dest='color_space', default='auto',
                            choices=ColorSpaceProcessor.COLOR_SPACES.keys(),
                            help=f'强制设置色彩空间:[ {' | '.join(ColorSpaceProcessor.COLOR_SPACES.keys())} ]',
                            metavar='色彩空间代码')

        parser.add_argument('--quality', '-q', dest='quality', default=80,
                            help='指定图像质量', metavar='压缩质量')

        parser.add_argument('--overwrite', '-y', dest='overwrite_target', default=False,
                            action='store_true', help='强制覆盖已存在的目标文件')

        parser.add_argument('--debug', '-d', action='store_true', dest='debug',
                            help='调试模式')

        parser.add_argument('--pretend', '-p', dest='pretend_mode', action='store_true',
                            help='干转模式，不执行写入操作')

        parser.add_argument('--full-help', help='显示详细的说明',
                            dest='show_full_help', action='store_true')

        parser.add_argument('sources', nargs='*',
                            help='需要转换的文件', metavar='文件列表')

        self._parser = parser
        self.profile = None
        self.global_task = None

    def __enter__(self):
        env.start()

        env.print(f'[yellow]{JpeggerApp.APP_NAME}[/yellow] [blue]{JpeggerApp.APP_VERSION}[/blue]')

        env.info('开始解析参数')
        args = self._parser.parse_args()
        self.profile = DataPackage(**vars(args))
        env.debug('解析的参数: ', self.profile)

        env.log_level = LogLevel.DEBUG if self.profile.debug else LogLevel.WARNING

        self.global_task = env.progress.add_task(description='全局进度', total=None)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = False

        if exc_type is None:
            env.debug('执行完毕，没有发生异常。')
        elif issubclass(exc_type, InterruptedError):
            env.error('用户取消操作！')
            result = True
        elif issubclass(exc_type, ArgumentError):
            env.error('参数输入错误，请“自查自纠”。')
            result = True

        env.progress.remove_task(self.global_task)
        self.global_task = None

        env.stop()
        return result

    @staticmethod
    def show_full_help():
        data = pkgutil.get_data('jpegger', 'help.md').decode('utf-8')
        panel = Panel(Markdown(data), width=80)
        env.console.print(panel)

    def _preprocessed_sources(self):
        """预处后的文件列表"""
        sources = []
        for x in self.profile.sources:
            sources += glob.glob(str(x))

        for s in sources:
            a = Path(s)
            if a.is_file():
                yield a
            elif a.is_dir():
                yield from [a / x for x in a.iterdir()]

    def run(self):
        if self.profile.show_full_help:
            JpeggerApp.show_full_help()
            return

        expander = PathExpander(self._preprocessed_sources(),
                                accept_dir=False,
                                search_subdir=self.profile.recursive)
        env.debug('expander 构建完成')

        plans = [x for x in expander]

        job_counter = JobCounter(len(plans))
        env.progress.start_task(self.global_task)
        env.progress.update(self.global_task, total=len(plans), completed=0)
        with ConvertAgent(self.profile) as agent:
            for source in plans:
                job_counter.advance()
                if env.wanna_quit:
                    raise InterruptedError('用户取消操作!')
                env.progress.update(self.global_task, description=source.name)
                agent.convert(source)
                env.progress.advance(self.global_task)
                env.print(f'[yellow]{job_counter}[/yellow] [cyan]{source.name}[/cyan] 转换完成')


def run():
    with JpeggerApp() as app:
        app.run()
