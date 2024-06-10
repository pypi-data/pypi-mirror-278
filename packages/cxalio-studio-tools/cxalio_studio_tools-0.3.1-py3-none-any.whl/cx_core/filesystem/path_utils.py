from pathlib import Path


def normalize_path(path: Path, anchor=Path('.')) -> Path:
    path = Path(path)
    anchor = Path(anchor)
    if path.is_absolute():
        return path.absolute()

    t = str(path)
    if t.startswith('~'):
        return Path(t.replace('~', str(Path.home()))).absolute()

    return (anchor / path).resolve(strict=False)


def normalize_suffix(suffix: str, with_dot=True) -> str:
    """检查扩展名是否带点"""
    s = str(suffix).strip().strip('.').lower()
    return '.' + s if with_dot else s


def force_suffix(source: Path, suffix: str, ignore_dir=True):
    if not source:
        return None
    source = Path(source)
    if source.is_dir() and ignore_dir:
        return source
    suffix = normalize_suffix(suffix)
    return source if source.suffix == suffix else source.with_suffix(suffix)


def quote_path(path, quote_char='"') -> str:
    path = str(path)
    return f'{quote_char}{path}{quote_char}' if ' ' in path else path
