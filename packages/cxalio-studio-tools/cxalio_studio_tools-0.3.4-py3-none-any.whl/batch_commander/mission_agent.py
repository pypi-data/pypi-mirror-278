import os
import signal
import subprocess
from functools import cached_property
from pathlib import Path

from cx_core.text import TagReplacer, split_at_unquoted_spaces
from cx_core.text.tag_replacer_data_source import PathDataSource
from .env import env


class MissionAgent:

    def __init__(self, profile, source):
        self.profile = profile
        self._source = source
        self._tagger = TagReplacer()
        self._tagger.install_data_source('source', PathDataSource(self._source, space_mode='escape'))
        self._tagger.install_data_source('sep', str(os.sep))

    @cached_property
    def compiled_cmd(self):
        if not self.profile.command:
            return None
        return self._tagger(str(self.profile.command))

    @cached_property
    def cmds(self):
        return split_at_unquoted_spaces(self.compiled_cmd)

    @cached_property
    def source_name(self):
        return Path(self._source).name

    @cached_property
    def source(self):
        return self._source

    def run(self):
        if not self.compiled_cmd:
            env.debug('没有命令输入，将输出源文件')
            env.print(self._source)
            return

        with subprocess.Popen(self.cmds, stdout=subprocess.PIPE, shell=True) as proc:
            for line in proc.stdout:
                if self.profile.verbose:
                    env.raw_print(line)
                if env.wanna_quit:
                    env.warning('向任务发送终止信号')
                    proc.send_signal(signal.SIGTERM)
                    break
            proc.wait()
        env.debug('子任务执行完毕')
