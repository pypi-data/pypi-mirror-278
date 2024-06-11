class MediaKillerError(Exception):
    pass


class ProfileNoFoundError(FileNotFoundError, MediaKillerError):
    def __init__(self, target=None):
        super(ProfileNoFoundError, self).__init__()
        self._tgt = target

    def __str__(self):
        if self._tgt:
            return f'ffmpeg 配置文件 "{self._tgt}" 未找到，程序无法执行'
        return '未指定配置文件，程序无法运行'


class UserCanceledError(MediaKillerError):
    def __str__(self):
        return '用户取消操作'


class NoPlansError(MediaKillerError):
    def __str__(self):
        return '没有需要执行的任务'


class NoSourceError(MediaKillerError):
    def __str__(self):
        return '未指定任何来源信息，无事可做'
