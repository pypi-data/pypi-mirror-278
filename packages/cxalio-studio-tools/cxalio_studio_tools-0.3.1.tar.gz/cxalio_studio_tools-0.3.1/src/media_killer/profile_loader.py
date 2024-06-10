import tomllib
from collections.abc import Iterable
from pathlib import Path

from cx_core import DataPackage
from cx_core.filesystem.path_utils import normalize_path, force_suffix
from .env import env


class ProfileLoader:
    def __init__(self, filename):
        self.task_id = None
        self.filename = force_suffix(filename, 'toml')

    def __enter__(self):
        env.info('进入配置解析器环境')
        self.task_id = env.progress.add_task(description='初始化配置解析器', total=None)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = False
        if exc_type is None:
            pass
        elif issubclass(exc_type, FileNotFoundError):
            env.critical(f'未找到配置文件: {self.filename.name}')
            result = True

        env.progress.remove_task(self.task_id)
        self.task_id = None
        env.info('配置解析器已关闭')

        return result

    @staticmethod
    def __make_sure_list(a=None):
        if not a:
            return []
        if isinstance(a, str):
            return a.split(' ')
        if isinstance(a, Iterable):
            return [str(x) for x in a]
        return [x for x in str(a).split(' ')]

    def __check_data_package(self, package):
        env.progress.update(self.task_id, description='解析配置文件数据', completed=1, total=2)
        env.info('开始检查配置数据...')

        result = DataPackage(**package)
        env.print(f'配置文件：[cyan]{result.general.name}[/cyan] : [yellow]{result.general.description}[/yellow]')

        if not result.general.ffmpeg:
            result.general.ffmpeg = 'ffmpeg'
            env.print('未指定 ffmpeg ，将调用系统环境中的 ffmpeg')

        profile_folder = normalize_path('.' if not result.profile_path else result.profile_path.parent)
        result.profile_folder = profile_folder
        if not result.general.working_folder:
            env.debug('配置文件未指定工作目录')
            result.general.working_folder = profile_folder
        else:
            result.general.working_folder = normalize_path(result.general.working_folder, profile_folder)
        env.debug(f'general.working_folder 已设置为 {result.general.working_folder}')

        if env.args.sources:
            result.source.files.extend(ProfileLoader.__make_sure_list(env.args.sources))
            env.print(f'增加 {len(env.args.sources)} 个手动指定的来源文件')

        if not result.target.folder:
            env.debug('未设置目标文件夹')
            result.target.folder = Path('.')
        result.target.folder = normalize_path(result.target.folder, result.general.working_folder)
        env.debug(f'target.folder 已设置为 {result.target.folder}')

        if not result.target.keep_parent_level:
            env.debug('未设置目标父目录保留层级，将设为 0')
            result.target.keep_parent_level = 0

        env.debug(f'参数解析结果：{result}')

        return result

    def load(self):
        result = {}
        env.progress.update(self.task_id, description=f'读取{self.filename}…')

        with env.progress.open(self.filename, 'rb', task_id=self.task_id) as fp:
            result.update(tomllib.load(fp))
        result['profile_path'] = Path(self.filename).absolute()
        return self.__check_data_package(result)
