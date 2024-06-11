from typehintwhl.command.build_stub import build_stub

import setuptools

__all__ = ["__version__", "setup"]

__version__ = "0.0.1"

def setup(**attrs):
    cmdclass = attrs.setdefault("cmdclass", {})
    cmdclass.setdefault("build_stub", build_stub)
    return setuptools.setup(**attrs)