from collections import defaultdict
from pathlib import Path

from cx_core.text.text_utils import unquote_text


class OptionPackage:

    @staticmethod
    def __format_key(k: str):
        key = str(k).strip()
        if key.startswith('-'):
            key = key[1:]
        return key

    @staticmethod
    def __format_value(v):
        value = str(v) if v else ''
        return unquote_text(value)

    def __init__(self, filename=None):
        self.raw_data = defaultdict(list)
        self.filename = Path(filename) if filename else None

    def insert(self, key, value=None):
        k = OptionPackage.__format_key(key)
        v = OptionPackage.__format_value(value) if value else None
        if v:
            self.raw_data[k].append(v)
        elif k not in self.raw_data:
            self.raw_data[k] = []
        return self

    def iter_options(self):
        for k, vs in self.raw_data.items():
            if not vs:
                yield k, None
            else:
                for v in vs:
                    yield k, v

    def iter_arguments(self):
        for k, v in self.iter_options():
            yield '-' + k
            yield v

    def __rich_repr__(self):
        yield 'filename', self.filename
        yield 'options', self.raw_data
