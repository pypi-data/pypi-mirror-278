from collections.abc import Iterable
from pathlib import Path
from types import LambdaType

def get_type_name(value):
    return type(value).__name__

def remove_string_affix(text, prefix, suffix):
    return text.removeprefix(prefix).removesuffix(suffix)

def process_exclude_list(stub, exclude, error = None):
    paths = []

    if error is None:
        error = ValueError

    if isinstance(exclude, str):
        exclude = exclude.split(',')
        
    for name in exclude or []:
        path = Path(name)

        if path.is_absolute() and not path.exists():
            msg = f"Exclude list contains stub file or directory that does not exist. ('{name}')"
            if isinstance(error, LambdaType): error(msg)
            raise error(msg)
        
        if path.exists():
            paths.append(path.absolute())
            continue

        if stub is None:
            msg = f"Exclude list contains stub file or directory that does not exist. ('{name}')"
            if isinstance(error, LambdaType): error(msg)
            raise error(msg)

        path = Path(stub, name).absolute()

        if not path.exists():
            msg = f"Exclude list contains stub file or directory that does not exist. ('{name}')"
            if isinstance(error, LambdaType): error(msg)
            raise error(msg)

        paths.append(path.absolute())
    
    return paths

def remove_string_quotes(value):
    helper = lambda _str: remove_string_affix(remove_string_affix(_str, '"', '"'), "'", "'")

    if isinstance(value, str):
        return helper(value)
    elif isinstance(value, Iterable):
        return [helper(v) for v in value if isinstance(v, str)]

    return value