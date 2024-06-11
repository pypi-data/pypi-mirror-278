import signal

from cx_core.app import ProgressEnv

env = ProgressEnv()


def signal_handler(sig, frame):
    if sig != signal.SIGINT:
        return
    env.info('接收到 SIGINT')
    env.print("收到终止信号，准备退出...")
    env.wanna_quit = True


signal.signal(signal.SIGINT, signal_handler)
