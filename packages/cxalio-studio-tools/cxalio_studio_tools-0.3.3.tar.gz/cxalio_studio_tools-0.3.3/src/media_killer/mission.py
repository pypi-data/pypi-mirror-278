from functools import cache
from pathlib import Path

from cx_core import DataPackage
from cx_core.filesystem.path_utils import normalize_path
from cx_core.misc.misc_utils import limit_number
from cx_core.text.tag_replacer import TagReplacer
from cx_core.text.text_utils import split_at_unquoted_spaces
from .env import env
from .option_package import OptionPackage


class OptionParser:
    def __init__(self, options):
        self._options = options

    @staticmethod
    def _iter_list(elements: list):
        prev_token = None
        for t in elements:
            token = str(t).strip()
            if token.startswith('-'):
                if prev_token:
                    yield prev_token, None
                    prev_token = None
                else:
                    prev_token = token[1:]
            else:
                if prev_token:
                    yield prev_token, token
                    prev_token = None
                else:
                    env.debug(f'忽略无法识别的参数： {token}')
        if prev_token:
            yield prev_token, None

    @staticmethod
    def _iter_dict(elements: dict):
        for k, v in elements.items():
            yield k, v

    def __iter__(self):
        if isinstance(self._options, list):
            return self._iter_list(self._options)
        if isinstance(self._options, dict | DataPackage):
            return self._iter_dict(self._options)
        return self._iter_list(split_at_unquoted_spaces(str(self._options)))


class Mission:
    def __init__(self, source: Path, profile):
        self.source = Path(source)
        self.profile = profile
        self.tag_replacer = TagReplacer(keep_unknown_tags=False)
        self.tag_replacer \
            .install_data_source('source', self.__source_handler) \
            .install_data_source('target', self.__target_handler) \
            .install_data_source('source_parent', self.__source_parent_handler) \
            .install_data_source('target_parent', self.__target_parent_handler) \
            .install_data_source('custom', self.__custom_handler)

        self.general_options = self.__parse_general_table(self.profile.general)
        self.inputs: [OptionPackage] = [self.__parse_io_table(i) for i in self.profile.input]
        self.outputs: [OptionPackage] = [self.__parse_io_table(o) for o in self.profile.output]

    def __parse_general_table(self, general_table: DataPackage):
        result = OptionPackage()
        option_pairs = OptionParser(general_table.options)
        for k, v in option_pairs:
            value = self.tag_replacer(v)
            result.insert(k, value)

        if general_table.hardware_accelerate:
            result.insert('hwaccel', general_table.hardware_accelerate)

        overwrite_option = '-y' if general_table.overwrite_existed else '-n'
        result.insert(overwrite_option)
        return result

    def __parse_io_table(self, io_table: DataPackage) -> OptionPackage:
        filename = self.tag_replacer(io_table.filename)
        result = OptionPackage(filename=filename)
        opt_parser = OptionParser(io_table.options)
        for k, v in opt_parser:
            result.insert(k, self.tag_replacer(v))
        return result

    @cache
    def __custom_handler(self, param=None):
        if param:
            return self.profile.get(f'custom.{str(param)}', str(param))
        return str(param)

    @cache
    def __source_handler(self, param=None):
        match param:
            case 'absolute':
                return str(self.source.absolute())
            case 'dot_suffix':
                return str(self.source.suffix)
            case 'suffix':
                return str(self.source.suffix)[1:]
            case 'parent':
                return str(self.source.parent)
            case 'parent_name':
                return str(self.source.parent.stem)
            case 'name':
                return str(self.source.name)
            case 'basename':
                return str(self.source.stem)
            case _:
                return str(self.source)

    @cache
    def __target_handler(self, param=None):
        match param:
            case 'absolute':
                return str(self.target.absolute())
            case 'dot_suffix':
                return str(self.target.suffix)
            case 'suffix':
                return str(self.target.suffix)[1:]
            case 'parent':
                return str(self.target.parent)
            case 'parent_name':
                return str(self.target.parent.stem)
            case 'name':
                return str(self.target.name)
            case 'basename':
                return str(self.target.stem)
            case _:
                return str(self.target)

    @cache
    def __source_parent_handler(self, param=None):
        level = int(param) if param else 1
        ps = self.source.parent.parts
        level = limit_number(level, 1, len(ps))
        selected_parts = ps[-1 * level:]
        return str(Path(*selected_parts))

    @cache
    def __target_parent_handler(self, param=None):
        level = int(param) if param else 1
        ps = self.target.parent.parts
        level = limit_number(level, 1, len(ps))
        selected_parts = ps[-1 * level:]
        return str(Path(*selected_parts))

    @property
    @cache
    def target(self) -> Path:
        target_folder = normalize_path(self.profile.target.folder, self.profile.general.working_folder)

        t_suffix = self.profile.target.suffix
        if not t_suffix.startswith('.'):
            t_suffix = '.' + t_suffix

        p_folder = Path()
        p_level = self.profile.target.keep_parent_level
        if p_level > 0:
            parents = self.source.parent.parts
            selected_parts = parents[-1 * p_level:]
            p_folder = Path(*selected_parts)
            env.debug(f'取用 {p_level} 个上级目录：{p_folder}')

        result = target_folder / p_folder / self.source.name
        return result.with_suffix(t_suffix)

    def iter_target_folders(self):
        for o in self.outputs:
            t = o.filename
            yield t.absolute().parent

    def __rich_repr__(self):
        yield 'from', self.source
        yield 'to', self.target
        yield 'general', self.general_options
        for x in self.inputs:
            yield 'input', x
        for x in self.outputs:
            yield 'output', x

    def check_output_writable(self):
        """检测全部目标文件是否可写入"""
        if self.profile.general.overwrite_existed:
            return True
        for o in self.outputs:
            file = o.filename
            if file.exists():
                return False
        return True


class MissionMaker:
    def __init__(self, profile):
        self.profile = profile

    def __call__(self, sources: [Path]):
        for s in sources:
            m = Mission(Path(s).absolute(), self.profile)
            env.debug(f'构建任务:', m)
            yield m
