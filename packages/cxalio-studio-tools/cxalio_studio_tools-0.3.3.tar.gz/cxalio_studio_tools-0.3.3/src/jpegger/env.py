import signal

from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Column

from cx_core.app import AbstractEnv, AppLogger, LogLevel


class Env(AbstractEnv):
    def __init__(self):
        super(Env, self).__init__()
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


env = Env()


def signal_handler(sig, frame):
    if sig != signal.SIGINT:
        return
    env.info('接收到 SIGINT')
    env.print("收到终止信号，准备退出...")
    env.wanna_quit = True


signal.signal(signal.SIGINT, signal_handler)
