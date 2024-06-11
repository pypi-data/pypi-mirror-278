from typehintwhl.exception import BuildError
from typehintwhl.log import logger

from pathlib import Path
import shutil
import os

class Builder:
    def __init__(self, package, stub, current=None, exclude=None):
        self.stub = stub
        self.package = package
        self.current = current or Path.cwd()
        self.exclude = exclude or []

        self._pyproject = None
        self._setupcfg = None
    
    @property
    def pyproject(self):
        if self._pyproject is None:
            path = Path(self.current, "pyproject.toml").absolute()

            if not path.exists():
                return
            
            self._pyproject = path
            return path
        
        if self._pyproject.exists():
            return self._pyproject
    
    @property
    def setupcfg(self):
        if self._setupcfg is None:
            path = Path(self.current, "setup.cfg").absolute()

            if not path.exists():
                return
            
            self._setupcfg = path
            return path
        
        if self._setupcfg.exists():
            return self._setupcfg
    
    @staticmethod
    def check_directory_argument(name, value):
        """Raises a BuildError if the argument's value is None"""
        if value is None:
            raise BuildError(f"The {name} directory has not been specified.")
    
    @staticmethod
    def remove_build_from_path(path, build):
        if isinstance(path, str):
            path = Path(path)
        
        if isinstance(build, str):
            build = Path(build)
        
        return Path(str(path.absolute()).removeprefix(str(build.absolute())))

    @staticmethod
    def get_relative_stub_path(stub, base):
        if isinstance(stub, str):
            stub = Path(stub)
        
        if isinstance(base, str):
            base = Path(base)
        
        return Path(str(stub).removeprefix(str(base)))

    def get_build_path_for_stub(self, original_stub):
        # Remove the starting \\ or / else it will consider it as an absolute path.
        return Path(self.get_build_directory(), str(original_stub).removeprefix(str(self.stub)).lstrip('\\/')).absolute()
    
    def get_build_directory(self):
        return Path(self.current, "build/lib", self.package.name)
    
    def create_build_directory(self, path):
        # Remove the old directory if it exists
        self.delete_build_directory(path)

        logger.info(f"copying package {self.package} -> {path}")
        shutil.copytree(str(self.package), str(path))

        # shutil.copytree copies the stub directory if it's
        # with in the project directory, remove it here
        stub_path = path / self.stub.name
        if stub_path.exists():
            shutil.rmtree(str(stub_path))

    def delete_build_directory(self, path):
        if not path.exists():
            return
        
        try:
            logger.info("removing previous build")
            shutil.rmtree(str(path))
        except OSError:
            logger.error("failed to remove previous build.")
            exit(1)
    
    def collect_stub_files(self):
        logger.info(f"collecting stub files in directory {self.stub}")

        stubs = []
        for root, _, files in os.walk(self.stub.absolute()):
            base = Path(self.package.name, self.stub.name)

            for file in files:
                path = Path(root, file).absolute()

                if path.suffix == ".pyi" and path not in self.exclude:
                    logger.info(f"found stub {path}")
                    root_name = root.removeprefix(str(base))
                    stubs.append(Path(base, root_name, file).absolute())
        
        return stubs
    
    def construct_file_source(self, path):
        return (self.stub / path.with_suffix(".pyi")).absolute()
    
    def construct_file_dest(self, root, filename):
        return (root / filename.with_suffix(".pyi")).absolute()
    
    @staticmethod
    def create_copy(src, dst, logging=False):
        if not src.exists():
            raise FileNotFoundError(f"The system cannot find the path specified ('{src.absolute()}')")
        
        if logging:
            logger.info(f"copying {src} -> {dst}")
        
        fsrc = open(src, "rb")
        fdst = open(dst, "wb")

        shutil.copyfileobj(fsrc, fdst)

        fsrc.close()
        fdst.close()
    
    def create(self):
        Builder.check_directory_argument("package", self.package)
        Builder.check_directory_argument("stub", self.stub)

        stub_files = self.collect_stub_files()
        build_path = self.get_build_directory()

        self.create_build_directory(build_path)

        for root, _, files in os.walk(build_path):
            if Path(root).name == "__pycache__":
                continue

            relative_root_path = Builder.remove_build_from_path(root, build_path)
            relative_stub_path = Builder.get_relative_stub_path(self.stub, self.package)
            
            if relative_root_path == relative_stub_path:
                continue

            for filename in files:
                filename = Path(filename)

                # Skip non-source files
                if filename.suffix != ".py":
                    continue
                
                src = self.construct_file_source(filename)
                dst = self.construct_file_dest(root, filename)

                if src in stub_files:
                    stub_files.remove(src)
                    Builder.create_copy(src, dst, logging=True)
        
        for full_stub_path in stub_files:
            stub_build_path = self.get_build_path_for_stub(full_stub_path)
            logger.warn(f"warning: '{full_stub_path}' has no matching source file,\n\tcopying to '{stub_build_path}'")
            Builder.create_copy(full_stub_path, stub_build_path)
        
        logger.info("finished building library with stub files.")
        
        return str(build_path)