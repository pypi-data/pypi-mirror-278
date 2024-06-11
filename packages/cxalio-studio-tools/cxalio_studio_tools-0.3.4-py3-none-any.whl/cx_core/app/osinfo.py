import os
import platform
from functools import cached_property
from pathlib import Path


class OSInfo:
    def __init__(self):
        self.__system = platform.system()

    @cached_property
    def system(self):
        return self.__system

    @cached_property
    def hosts_file(self):
        if self.system == 'Windows':
            win_dir = Path(os.getenv('windir'))
            return win_dir / "System32/drivers/etc/hosts"
        return Path("/etc/hosts")
