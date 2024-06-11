from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Column

from .abstract_env import AbstractEnv
from .app_logger import AppLogger, LogLevel


class ProgressEnv(AbstractEnv):
    def __init__(self):
        super(ProgressEnv, self).__init__()
        self.wanna_quit = False

        self._progress = Progress(
            SpinnerColumn(),
            TextColumn('[progress.description]{task.description}', table_column=Column(ratio=50)),
            TimeElapsedColumn(),
            expand=True,
            transient=True)

        self._logger = AppLogger(console=self._progress.console)
        self._logger.level = LogLevel.WARNING

    def start(self):
        self._progress.start()
        self.info('全局环境已启动')

    def stop(self):
        self._progress.stop()
        self.info('Bye~')

    @property
    def console(self):
        return self._progress.console

    @property
    def progress(self):
        return self._progress
