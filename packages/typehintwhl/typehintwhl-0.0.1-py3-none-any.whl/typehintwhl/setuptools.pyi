# This is a copy of the typeshed stub files for setuptools
# https://github.com/python/typeshed/tree/main/stubs/setuptools/setuptools
from collections.abc import (
    MutableMapping,
    Sequence,
    Iterable, 
    Iterator, 
    Mapping
)

from .distutils import (
    Distribution as _Distribution,
    Extension as _Extension,
    Command as _Command
)

from typing import Literal, Any
from abc import abstractmethod

class Extension(_Extension):
    py_limited_api: bool
    def __init__(
        self,
        name: str,
        sources: list[str],
        include_dirs: list[str] | None = None,
        define_macros: list[tuple[str, str | None]] | None = None,
        undef_macros: list[str] | None = None,
        library_dirs: list[str] | None = None,
        libraries: list[str] | None = None,
        runtime_library_dirs: list[str] | None = None,
        extra_objects: list[str] | None = None,
        extra_compile_args: list[str] | None = None,
        extra_link_args: list[str] | None = None,
        export_symbols: list[str] | None = None,
        swig_opts: list[str] | None = None,
        depends: list[str] | None = None,
        language: str | None = None,
        optional: bool | None = None,
        *,
        py_limited_api: bool = False,
    ) -> None: ...

class Distribution(_Distribution):
    def patch_missing_pkg_info(self, attrs: Mapping[str, Any]) -> None: ...
    src_root: str | None
    dependency_links: list[str]
    setup_requires: list[str]
    def __init__(self, attrs: MutableMapping[str, Any] | None = None) -> None: ...
    def warn_dash_deprecation(self, opt: str, section: str) -> str: ...
    def make_option_lowercase(self, opt: str, section: str) -> str: ...
    def parse_config_files(self, filenames: Iterable[str] | None = None, ignore_option_errors: bool = False) -> None: ...
    def fetch_build_eggs(self, requires: str | Iterable[str]): ...
    def get_egg_cache_dir(self) -> str: ...
    def fetch_build_egg(self, req): ...
    def get_command_class(self, command: str) -> type[Command]: ...
    def include(self, **attrs) -> None: ...
    def exclude_package(self, package: str) -> None: ...
    def has_contents_for(self, package: str) -> bool | None: ...
    def exclude(self, **attrs) -> None: ...
    def get_cmdline_options(self) -> dict[str, dict[str, str | None]]: ...
    def iter_distribution_names(self) -> Iterator[str]: ...
    def handle_display_options(self, option_order): ...

def setup(
    *,
    name: str = ...,
    version: str = ...,
    description: str = ...,
    long_description: str = ...,
    long_description_content_type: str = ...,
    author: str = ...,
    author_email: str = ...,
    maintainer: str = ...,
    maintainer_email: str = ...,
    url: str = ...,
    download_url: str = ...,
    packages: list[str] = ...,
    py_modules: list[str] = ...,
    scripts: list[str] = ...,
    ext_modules: Sequence[Extension] = ...,
    classifiers: list[str] = ...,
    distclass: type[Distribution] = ...,
    script_name: str = ...,
    script_args: list[str] = ...,
    options: Mapping[str, Any] = ...,
    license: str = ...,
    keywords: list[str] | str = ...,
    platforms: list[str] | str = ...,
    cmdclass: Mapping[str, type[_Command]] = ...,
    data_files: list[tuple[str, list[str]]] = ...,
    package_dir: Mapping[str, str] = ...,
    obsoletes: list[str] = ...,
    provides: list[str] = ...,
    requires: list[str] = ...,
    command_packages: list[str] = ...,
    command_options: Mapping[str, Mapping[str, tuple[Any, Any]]] = ...,
    package_data: Mapping[str, list[str]] = ...,
    include_package_data: bool = ...,
    libraries: list[str] = ...,
    headers: list[str] = ...,
    ext_package: str = ...,
    include_dirs: list[str] = ...,
    password: str = ...,
    fullname: str = ...,
    **attrs: Any,
) -> Distribution: ...

class Command(_Command):
    command_consumes_arguments: bool
    distribution: Distribution
    def __init__(self, dist: Distribution, **kw: Any) -> None: ...
    def ensure_string_list(self, option: str | list[str]) -> None: ...
    def reinitialize_command(
        self, command: _Command | str, reinit_subcommands: bool | Literal[0, 1] = 0, **kw: Any
    ) -> _Command: ...
    @abstractmethod
    def initialize_options(self) -> None: ...
    @abstractmethod
    def finalize_options(self) -> None: ...
    @abstractmethod
    def run(self) -> None: ...