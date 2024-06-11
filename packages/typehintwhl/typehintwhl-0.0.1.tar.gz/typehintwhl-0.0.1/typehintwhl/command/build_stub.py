from typehintwhl.exception import SetupError
from typehintwhl.common import process_exclude_list
from typehintwhl.config import ConfigLoader
from typehintwhl.build import Builder

from setuptools import Command
from pathlib import Path

def check_directory_option(name, value):
    if not isinstance(value, str):
        return value
    
    path = Path(value).absolute()

    if not path.exists():
        raise SetupError(f"The {name} directory does not exist. ('{path}')")

    if not path.is_dir():
        raise SetupError(f"The {name} path must specify a directory.")
    
    return path

class build_stub(Command):
    """Build a package with unpacked stub files."""

    description = __doc__
    user_options = [
        ("stub=",    "s", "specify the stub directory to unpack."),
        ("current=", "b", "specify the current directory. (Defaults to the current working directory)"),
        ("package=", "p", "specify the package directory."),
        ("exclude=", "e", "comma-separated list of stub files to exclude")
    ]

    def initialize_options(self):
        self.stub = None
        self.package = None
        self.current = Path.cwd()
        self.exclude = []
    
    def finalize_options(self):
        self.stub = check_directory_option("stub", self.stub)
        self.package = check_directory_option("package", self.package)
        self.current = check_directory_option("current", self.current)
        self.exclude = process_exclude_list(self.stub, self.exclude, SetupError)
    
    def run(self):
        config = ConfigLoader.loadAllFiles(self.current)

        package, stub, exclude = None, None, []

        if config is not None:
            stub = config.stub
            package = config.package
            current = config.current or Path.cwd()
            exclude = config.exclude or []

        self.exclude.extend(exclude)

        builder = Builder(
            self.package or package,
            self.stub or stub,
            self.current or current,
            self.exclude
        )

        builder.create()