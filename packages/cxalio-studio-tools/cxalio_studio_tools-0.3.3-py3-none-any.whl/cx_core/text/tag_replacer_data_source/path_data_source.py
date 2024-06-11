from functools import cached_property, cache
from pathlib import Path


class PathDataSource:
    def __init__(self, path: Path):
        self._source = Path(path)

    @cached_property
    def _neat_source(self):
        return self._source.resolve()

    @cache
    def _handle(self, argument):
        match argument:
            case 'absolute':
                return self._neat_source.absolute()
            case 'name':
                return self._source.name
            case 'basename':
                return self._source.stem
            case 'suffix':
                return self._source.suffix
            case 'complete_suffix':
                return ''.join(self._source.suffixes)
            case 'suffix_no_dot':
                suffix = self._source.suffix
                if suffix.startswith('.'):
                    return suffix[1:]
                return suffix
            case 'complete_suffix_no_dot':
                suffix = ''.join(self._source.suffixes)
                if suffix.startswith('.'):
                    return suffix[1:]
                return suffix
            case 'complete_basename':
                basename = self._source.stem
                suffixes = self._source.suffixes
                return basename + ''.join(suffixes[:-1])
            case 'parent':
                return self._source.parent
            case 'parent_absolute':
                return self._neat_source.parent.absolute()
            case 'parent_name':
                return self._source.parent.name
            case _:
                return self._source

    def __call__(self, argument):
        return str(self._handle(argument))
