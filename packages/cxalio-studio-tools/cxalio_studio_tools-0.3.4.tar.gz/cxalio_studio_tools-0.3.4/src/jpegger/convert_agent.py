from functools import cached_property
from pathlib import Path

from PIL import UnidentifiedImageError

from cx_core.filesystem import force_suffix
from cx_core.text import extract_numbers
from cx_image import ImageConverter, ColorSpaceProcessor, MaxAreaResizeProcessor, MaxEdgeResizeProcessor, \
    ForceSizeProcessor
from .env import env


class ConvertAgent:
    RESIZE_MODES = ['auto', 'area', 'edge', 'crop', 'fit', 'stretch', 'none']

    def __init__(self, profile=None):
        self.profile = profile
        self._converter = None

    @cached_property
    def output_format(self):
        f = self.profile.format
        return None if f is None else f.strip().upper()

    @cached_property
    def quality(self):
        return int(self.profile.quality)

    @cached_property
    def color_space(self):
        return str(self.profile.color_space or 'auto').strip().lower()

    @cached_property
    def format(self):
        return str(self.profile.format).strip().upper()

    def _color_space_processor(self):
        if self.color_space == 'auto':
            return None
        return ColorSpaceProcessor(self.color_space)

    def _size_processor(self):
        if not self.profile.max_size:
            return None
        # 解析max_size
        numbers = [abs(int(round(x))) for x in extract_numbers(self.profile.max_size)]
        count = len(numbers)
        env.debug(f'从 {self.profile.max_size} 中解析出数字: {numbers}')

        if count < 1:
            env.warning(f'最大尺寸输入非法，将不进行尺寸限制')
            return None
        elif count == 1:
            if self.profile.resize_mode in {'crop', 'fit', 'stretch', 'none'}:
                env.warning(f'仅指定了一个尺寸，无法应用强制缩放模式。将使用最长边代替。')
            if self.profile.resize_mode == 'area':
                return MaxAreaResizeProcessor(numbers[0])
            else:
                return MaxEdgeResizeProcessor(numbers[0])
        else:
            w, h = numbers[0:2]
            match self.profile.resize_mode:
                case 'stretch':
                    return ForceSizeProcessor(w, h, keep_aspect=False, fill=True)
                case 'crop':
                    return ForceSizeProcessor(w, h, keep_aspect=True, fill=True)
                case 'fit':
                    return ForceSizeProcessor(w, h, keep_aspect=True, fill=False)
                case 'none':
                    return ForceSizeProcessor(w, h, keep_aspect=False, fill=False)
                case 'edge':
                    return MaxEdgeResizeProcessor(max(w, h))
                case _:
                    return MaxAreaResizeProcessor(w, h)

    def __enter__(self):
        self._converter = ImageConverter(self.output_format, self.quality)

        color_space_processor = self._color_space_processor()
        if not color_space_processor:
            env.debug('无需安装色彩空间预处理器')
        else:
            self._converter.install_processor(color_space_processor)
            env.debug('已安装色彩空间预处理器')

        size_processor = self._size_processor()
        if not size_processor:
            env.debug('无需安装尺寸限制器')
        else:
            self._converter.install_processor(size_processor)
            env.debug('已安装尺寸限制器')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = False
        if exc_type is None:
            pass
        elif issubclass(exc_type, InterruptedError):
            pass
        else:
            env.error(f'发生未知错误……')
            env.debug(exc_val)
            result = True

        return result

    def _make_target(self, source):
        folder = Path(self.profile.output_dir)
        suffix = ImageConverter.ACCEPTABLE_OUTPUT_FORMATS.get(self.format, ".???")
        name = force_suffix(source, suffix)
        if self.profile.keep_parent:
            parent_name = source.parent.name
            folder = folder / parent_name
        return folder / name.name

    def convert(self, source):
        source = Path(source).resolve()
        target = self._make_target(source).resolve()
        folder = target.parent
        if not folder.exists():
            env.debug(f'目标目录{folder.absolute()}不存在，将自动创建。')
            folder.mkdir(exist_ok=True)

        if not self.profile.overwrite_target:
            if source == target:
                env.error(f'[yellow]{source.name}[/yellow][red] 源文件与目标相同，将跳过处理。[/red]')
                return
            if target.exists():
                env.critical(f'[red]目标文件[yellow]{target.name}[/yellow]已存在，将跳过！[/red]')
                return

        if self.profile.pretend_mode:
            env.debug(f'假装模式，跳过任务{source.name}')
            return
        try:
            self._converter.convert(source, target)
        except UnidentifiedImageError:
            env.error(f'[yellow]{source.name}[/yellow] 无法识别图片格式，即将跳过。')
