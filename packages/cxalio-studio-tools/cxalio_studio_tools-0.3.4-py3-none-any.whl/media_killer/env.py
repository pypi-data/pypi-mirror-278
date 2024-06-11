import signal

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.table import Column

from cx_core.app import AppLogger, AbstractEnv, LogLevel


class Env(AbstractEnv):
    def __init__(self):
        super(Env, self).__init__()
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}", table_column=Column(ratio=50)),
            BarColumn(table_column=Column(ratio=20)),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            expand=True,
            transient=True)

        self._logger = AppLogger(console=self._progress.console)
        self._logger.level = LogLevel.WARNING

        self.args = None

        self.current_ffmpeg = None
        self.wanna_quit = False

    def start(self):
        self._progress.start()
        self.info('全局环境已启动')

    def stop(self):
        self._progress.stop()
        self.info('Bye~')

    @property
    def progress(self):
        return self._progress

    @property
    def console(self):
        return self._progress.console


env = Env()


def signal_handler(sig, frame):
    if sig != signal.SIGINT:
        return
    env.info('接收到 SIGINT')
    env.print("[red]收到终止信号，准备退出...[/red]")
    env.wanna_quit = True
    if env.current_ffmpeg:
        env.current_ffmpeg.terminate()


signal.signal(signal.SIGINT, signal_handler)
