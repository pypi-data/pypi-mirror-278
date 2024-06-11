from typehintwhl.common import AbsolutePath
from setuptools import Command
from typing import ClassVar, Tuple, List, Any

def check_directory_option(name: str, value: Any) -> AbsolutePath | None: ...

class build_stub(Command):
    """Build a package with unpacked stub files."""

    description: str | None = __doc__
    user_options: ClassVar[List[Tuple[str, str | None, str]]]

    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    def run(self) -> None: ...