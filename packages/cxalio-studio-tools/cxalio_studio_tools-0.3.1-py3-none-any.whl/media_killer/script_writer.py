from pathlib import Path

from cx_core.text.text_utils import quote_text
from .env import env
from .mission import Mission


class ScriptWriter:
    def __init__(self, target):
        self.target = Path(target).absolute()
        self.output = None
        self.planned_folders = set()

    def __enter__(self):
        self.output = open(self.target, 'w')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.output.flush()
        self.output.close()
        return False

    @staticmethod
    def compile_cmd(mission: Mission):
        """将Mission编译为命令行"""
        line = [mission.profile.general.ffmpeg]
        line += mission.general_options.iter_arguments()
        for input_ in mission.inputs:
            line += input_.iter_arguments()
            line += ['-i', quote_text(input_.filename)]
        for output_ in mission.outputs:
            line += output_.iter_arguments()
            line += quote_text(output_.filename)
        return ' '.join([item for item in line if item is not None])

    def check_target_folders(self, mission):
        """检查潜在的目标文件夹，并写入新建文件夹的命令"""
        for folder in mission.iter_target_folders():
            if folder in self.planned_folders:
                continue
            self.output.write(f'mkdir -p {quote_text(folder.absolute())}\n')
            self.planned_folders.add(folder)
            env.info(f'计划创建目录： {folder}')

    def write_mission(self, mission: Mission):
        self.check_target_folders(mission)

        cmd = ScriptWriter.compile_cmd(mission)
        self.output.write(f'{cmd}\n')
        env.info(f'写入命令： [purple]{cmd}[/purple]')
