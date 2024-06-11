from typehintwhl.exception import ConfigurationError, SetupError

from typehintwhl.common import (
    process_exclude_list, 
    remove_string_quotes, 
    remove_string_affix,
    get_type_name
)

from pathlib import Path
from types import NoneType

import configparser
import tomllib

class Config:
    def __init__(self, package, stub, current=None, exclude=None):
        self.stub = stub
        self.package = package
        self.current = current
        self.exclude = exclude
    
    def __repr__(self):
        return f"Config(package={self.package}, stub={self.stub}, current={self.current}, exclude={self.exclude})"

class ConfigLoader:
    class _Tracer:
        def __init__(self):
            self.stub = None
            self.package = None
            self.exclude = []
        
        def set(self, name, value):
            # Don't override already set values
            if getattr(self, name) is None:
                setattr(self, name, Path(value).absolute() if isinstance(value, str) else value)
        
        def integrate(self, config):
            if config is None or self.check():
                return

            self.set("stub", config.stub)
            self.set("package", config.package)
            self.exclude.extend(config.exclude or [])
        
        def check(self):
            return self.package is not None and self.stub is not None
        
        @property
        def missing(self):
            return list([v[0] for v in filter(lambda v: v[1] is None, [("package", self.package,), ("stub", self.stub,)])])

    @staticmethod
    def pyproject(file):
        """Load configuration from a pyproject.toml file."""
        file = file.absolute() # Verify absolute path
        
        with open(file, "rb") as fp:
            data = tomllib.load(fp)
        
        config = data.get("tool", {}).get("typehintwhl", {})

        package, stub, exclude = ConfigLoader.process_config_data(
            file,
            config.get("package"), 
            config.get("stub"), 
            config.get("exclude")
        )

        return Config(package, stub, file, exclude)
    
    @staticmethod
    def setupcfg(file):
        """Load configuration from a setup.cfg file."""
        file = file.absolute() # Verify absolute path

        cfg = configparser.RawConfigParser()
        cfg.read(file.absolute())
        cfg = cfg["typehintwhl"] if cfg.has_section("typehintwhl") else None

        if cfg is None:
            return

        package, stub, exclude = ConfigLoader.process_config_data(
            file,
            remove_string_quotes(cfg.get("package", fallback=None)),
            remove_string_quotes(cfg.get("stub", fallback=None)),
            remove_string_quotes(cfg.get("exclude", fallback=None))
        )

        if package is None and stub is None and not exclude:
            return

        return Config(package, stub, file, exclude)
    
    @staticmethod
    def cli(args):
        """Load configuration from command line arguments."""
        
        package, stub, exclude = ConfigLoader.process_config_data(
            args.current,
            args.package,
            args.stub,
            args.exclude or []
        )

        if package is None and stub is None and not exclude:
            return
        
        return Config(package, stub, exclude)

    @staticmethod
    def loadAllFiles(file):
        file = file.absolute() # Verify absolute path
        pyproject_path = Path(file, "pyproject.toml").absolute()
        setupcfg_path = Path(file, "setup.cfg").absolute()

        tracer = ConfigLoader._Tracer()

        tracer.integrate(ConfigLoader.pyproject(pyproject_path) if pyproject_path.exists() else None)
        tracer.integrate(ConfigLoader.setupcfg(setupcfg_path) if setupcfg_path.exists() else None)

        if tracer.check():
            return Config(tracer.package, tracer.stub, tracer.exclude)
    
    @staticmethod
    def loadAll(file, args):
        # Load Order (cli, pyproject.toml, setup.cfg)
        file = file.absolute() # Verify absolute path
        tracer = ConfigLoader._Tracer()

        tracer.integrate(ConfigLoader.cli(args) if args is not None else None)
        tracer.integrate(ConfigLoader.loadAllFiles(file))

        if tracer.check():
            return Config(tracer.package, tracer.stub, file, tracer.exclude)
        
        msg = "\n".join([
            f"Failed to complete configuration, not enough information.", 
            "\tMissing: ", remove_string_affix(repr(tracer.missing), '[', ']').replace("'", "")
        ])

        raise SetupError(msg)

    @staticmethod
    def process_config_data(root, package, stub, exclude):
        base_err_msg = (f"'{root.name}' file contains invalid 'typehintwhl' tool configuration.\n\t", f"\n\tConfig Path: ({root})",)
        type_err_msg = base_err_msg[0] + "\tExpected option '{option}' to be of type {expects}, instead got '{got}'" + base_err_msg[1]
        exists_err_msg = base_err_msg[0] + "\t{option} option contains path that does not exist.\n\tSpecified Path: ({path})" + base_err_msg[1]
        dir_err_msg = base_err_msg[0] + "\tExpected option '{option}' to be a directory path."

        if not isinstance(package, (str, NoneType,)):
            raise ConfigurationError(type_err_msg.format(option="package", expects="str", got=get_type_name(package)))
        
        if not isinstance(stub, (str, NoneType,)):
            raise ConfigurationError(type_err_msg.format(option="stub", expects="str", got=get_type_name(stub)))

        if package is not None:
            package = Path(package).absolute()

            if not package.exists():
                raise ConfigurationError(exists_err_msg.format(option="package", path=package))

            if not package.is_dir():
                raise ConfigurationError(dir_err_msg.format(option="package"))
        
        if stub is not None:
            stub = Path(stub).absolute()

            if not stub.exists():
                raise ConfigurationError(exists_err_msg.format(option="stub", path=stub))

            if not stub.is_dir():
                raise ConfigurationError(dir_err_msg.format(option="stub"))
        
        exclude = process_exclude_list(stub, exclude, lambda msg: ConfigurationError(base_err_msg[0] + msg + base_err_msg[1]))

        return package, stub, exclude