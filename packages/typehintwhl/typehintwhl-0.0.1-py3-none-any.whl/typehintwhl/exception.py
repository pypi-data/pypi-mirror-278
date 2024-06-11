__all__ = ["SetupError", "ConfigurationError"]

class SetupError(Exception):
    """An error occured during setup due to invalid build configurations."""
    pass

class BuildError(Exception):
    """An error that occurs during the building, usually if a configuration has not be set."""
    pass

class ConfigurationError(Exception):
    """Invalid configuration was provided for building."""
    pass