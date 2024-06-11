from typing_extensions import TypeAlias
from collections.abc import Iterable
from pathlib import Path

from typing import List, Any
from types import LambdaType

AbsolutePath: TypeAlias = Path
RelativePath: TypeAlias = Path

def copy_stub_file(src: Path, dst: Path) -> None: ...
def get_type_name(value: Any) -> str: ...
def remove_string_affix(text: str, prefix: str, suffix: str) -> str: ...
def process_exclude_list(
    stub: str | None, 
    exclude: List[str] | str, 
    error: LambdaType | Exception | None = None
) -> List[Path]: ...
def remove_string_quotes(value: Iterable[str] | str) -> List[str] | str: ...