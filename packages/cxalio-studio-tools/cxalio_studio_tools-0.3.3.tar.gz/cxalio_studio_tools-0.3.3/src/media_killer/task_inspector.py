import itertools

from cx_core import DataPackage
from cx_core.filesystem.path_expander import *
from cx_core.filesystem.path_utils import normalize_path, normalize_suffix
from .env import env
from .source_adapter import adapters


class TaskInspector:
    """处理输入的队列，并解析可接受的文件"""

    DEFAULT_SUFFIXES = ("mov mkv mp4 flv 3gp 3gpp rmvb mp3 aac"
                        " mxf mxf_op1a vob wmv wma srt ass aas ttml ogg oga ogv m4a"
                        " m4v 3g2 mpeg mpg ts lrc h264 flac ast asf gif")

    def __init__(self, profile: DataPackage):
        self._profile = profile
        self.task = None
        self._expander_settings = None

    def __enter__(self):
        env.info('计算扩展名白名单...')

        default_suffixes = TaskInspector.DEFAULT_SUFFIXES.split()

        if self.profile.source.bypass_default_suffixes:
            env.print('[yellow]已忽略内置的扩展名白名单[/yellow]')
            default_suffixes = []

        _suffixes = {str(x).strip('.') for x in
                     itertools.chain(
                         default_suffixes,
                         self.profile.source.suffix_includes)
                     if x not in {str(x).strip('.')
                                  for x in self.profile.source.suffix_excludes}
                     }
        env.debug(f'计划接受的扩展名: [green]{' '.join(_suffixes)}[/green]')

        self._expander_settings = PathExpander.Settings(
            accept_dir=False,
            file_validator=SuffixValidator(_suffixes),
            anchor_dir=self.profile.general.working_folder
        )
        env.info('已构建 PathExpander.Settings')

        self.task = env.progress.add_task(description='任务探测器', total=None)
        env.info('任务探测器启动')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        env.progress.remove_task(self.task)
        return False

    @property
    def profile(self):
        return self._profile

    def _expand_source(self, source: Path) -> []:
        """
        检查来源文件是否是列表文件并展开
        """
        source = normalize_path(source, self.profile.general.working_folder)
        suffix = normalize_suffix(source.suffix, False)
        result = []
        if suffix in adapters:
            env.print(f'[cyan]{source.name}[/cyan] 为列表文件，将会展开')
            env.progress.update(self.task, description=f'正在展开 [cyan]{source.name}[/cyan] 中包含的媒体信息')
            with adapters[suffix](source) as adapter:
                for item in adapter.items():
                    k = Path(item)
                    env.debug(f'发现新的文件路径: [cyan]{k}[/cyan]')
                    result.append(k)
        else:
            result.append(source)
        return result

    def _arrange(self, sources: []) -> []:
        env.progress.update(self.task, description='检查计划列表…')
        env.info('开始根据路径进行排序…')
        sources = sorted(sources, key=lambda a: Path(a).absolute())

        env.info('开始逐个检查…')
        result = []
        for k, v in env.progress.track(itertools.groupby(sources), task_id=self.task):
            kk = Path(k).absolute()
            env.progress.update(self.task,
                                description=f'检查项目: [cyan]{kk.name}[/cyan] …')
            if not kk.exists():
                env.warning(f'[red]文件 [cyan]{kk.name}[/cyan] 不存在，将从任务列表中去除[/red]')
                continue
            result.append(kk)
            env.debug(f'添加任务 [cyan]{kk}[/cyan]')

            count = len(list(v))
            if count > 1:
                env.warning(
                    f'[yellow][cyan]{kk.name}[/cyan]有 [red]{count - 1}[/red] 个重复项，已从任务列表中去除[/yellow]')

        env.info('计划列表整理完毕')
        return result

    def make_plans(self, sources) -> [Path]:
        env.print(f'检测到 {len(sources)} 个输入，正在展开路径…')
        env.progress.update(self.task, description='构建路径展开器…')
        expander = PathExpander(sources, self._expander_settings)

        result = []

        for source in expander:
            env.progress.update(self.task, description=f'检测 [cyan]{source.name}[/cyan]')
            result += self._expand_source(source)

        return self._arrange(result)
