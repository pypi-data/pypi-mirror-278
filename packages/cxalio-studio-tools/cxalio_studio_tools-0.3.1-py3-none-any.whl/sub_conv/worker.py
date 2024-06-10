from cx_core import DataPackage
from cx_subtitle import SubtitleFormatter
from cx_subtitle.loader import *
from cx_subtitle.saver import *
from .env import env
from .exceptions import *
from .subtitle_translator import SubtitleTranslator


class Mission:
    def __init__(self, source, profile: DataPackage):
        self._profile = profile
        self._source = Path(source).absolute()

    @property
    def profile(self):
        return self._profile

    @property
    def source(self) -> Path:
        return self._source

    @property
    def name(self) -> str:
        return self._source.name

    @cached_property
    def target_dir(self) -> Path:
        t_dir = self._source.parent
        if self.profile.target_dir:
            t_dir = Path(self.profile.target_dir).absolute()
        if self.profile.sub_dir:
            t_dir = t_dir / str(self.profile.sub_dir)
        return t_dir

    @cached_property
    def target_basename(self) -> str:
        result = self._source.stem
        if self.profile.appending:
            result += str(self.profile.appending)
        return result

    def make_target(self, suffix: str):
        if not suffix.startswith('.'):
            suffix = '.' + suffix
        return self.target_dir / (self.target_basename + suffix)


class Worker:
    __loader_classes = {
        '.srt': SrtLoader,
        '.txt': TxtLoader,
        '.docx': WordLoader,
        '.ttml': TTMLLoader
    }

    __saver_classes = {
        'srt': SrtSaver,
        'txt': TxtSaver,
        'word': WordSaver,
        'excel': ExcelSaver,
        'csv': CsvSaver
    }

    __suffixes = {
        'txt': '.txt',
        'word': '.docx',
        'excel': '.xlsx',
        'csv': '.csv',
        'srt': '.srt',
        'ttml': '.ttml',
        'rtf': '.rtf'
    }

    _formatter = None
    _translator = None

    def __init__(self, mission: Mission):
        self.mission = mission
        self.task = None

    @staticmethod
    def acceptable_suffixes():
        return Worker.__loader_classes.keys()

    @staticmethod
    def supported_formats():
        return Worker.__saver_classes.keys()

    @property
    def profile(self):
        return self.mission.profile

    @cached_property
    def target_suffix(self):
        res = Worker.__suffixes.get(self.profile.format)
        return res or '.txt'

    @cached_property
    def source_suffix(self):
        return self.mission.source.suffix

    @cached_property
    def loader_class(self):
        return Worker.__loader_classes.get(self.source_suffix)

    @cached_property
    def saver_class(self):
        return Worker.__saver_classes.get(self.profile.format)

    @cached_property
    def target(self):
        return self.mission.make_target(self.target_suffix)

    def __enter__(self):
        if not self.profile.bypass_formatter and not Worker._formatter:
            env.print(f'启用[blue]字幕格式检查器')
            Worker._formatter = SubtitleFormatter()

        if self.profile.translate and not Worker._translator:
            env.print(f'启用[blue]字幕文本翻译器')
            Worker._translator = SubtitleTranslator()

        self.task = env.progress.add_task(self.mission.name, total=None)
        env.debug(f'Worker启动: [yellow]{self.mission.source}[/yellow] --> [cyan]{self.target}[/cyan]')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        env.progress.remove_task(self.task)
        self.task = None
        env.debug(f'删除 Worker 的进度条')

        result = False
        if exc_type is None:
            env.print(f'[cyan]{self.target.name}[/cyan]已完成')
        elif issubclass(exc_type, NoLoaderError):
            env.warning(f'未为来源文件 [yellow]{self.mission.name}[/yellow] 找到合适的加载器，'
                        f'[red]将跳过此任务[/red]')
            result = True
        elif issubclass(exc_type, NoSaverError):
            env.warning(f'未为目标文件 [cyan]{self.target.name}[/cyan] 找到合适的加载器，'
                        f'[red]将跳过此任务[/red]')
            result = True
        elif issubclass(exc_type, TargetConflictError):
            env.warning(
                f'来源文件 [yellow]{self.mission.name}[/yellow] 和目标文件 [cyan]{self.target.name}[/cyan] '
                f'的[red]路径与文件名相同,将跳过此任务[/red]')
            result = True
        elif issubclass(exc_type, TargetExistsError):
            env.warning(
                f'目标文件 [cyan]{self.target.name}[/cyan] 已经存在，'
                f'[red]请更改目标位置或手动移除此文件[/red]，本次将跳过此任务')
            result = True
        elif issubclass(exc_type, UserCancelError):
            env.error(
                f'[red]尝试移除未完成的目标文件: [cyan]{self.target.name}[/cyan][/red]')
            self.target.unlink(missing_ok=True)
            result = True

        return result

    def process(self):
        if not self.loader_class:
            raise NoLoaderError()

        if not self.saver_class:
            raise NoSaverError()

        if self.mission.source == self.target:
            raise TargetConflictError()

        if self.target.exists():
            raise TargetExistsError()

        with self.loader_class(self.mission.source,
                               encoding=self.profile.source_encoding) as loader:
            env.info('构建loader...')
            if not self.target.parent.exists():
                env.print(f'目标目录[blue]{self.target.parent.absolute()}[/blue]不存在，正在创建...')
                self.target.parent.mkdir(parents=True, exist_ok=True)

            with self.saver_class(self.target,
                                  keep_time=self.profile.keep_time,
                                  encoding=self.profile.target_encoding) as saver:
                env.info('构建saver...')
                saver.install_processor(Worker._translator) \
                    .install_processor(Worker._formatter)

                env.debug('开始读写...')
                for subtitle in env.progress.track(loader.subtitles(), task_id=self.task):
                    saver.write(subtitle)
                    env.debug(f'写入文本: [yellow]{subtitle.content}[/yellow]')
                    env.progress.update(self.task, description=f'[yellow]{subtitle.content}[/yellow]')
                    if env.wanna_quit:
                        raise UserCancelError

        env.info(f'读写操作完毕')
