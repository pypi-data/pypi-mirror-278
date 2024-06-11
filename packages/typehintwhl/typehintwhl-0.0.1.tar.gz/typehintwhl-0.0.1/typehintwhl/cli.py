from typehintwhl.config import ConfigLoader
from typehintwhl.build import Builder
from typehintwhl.log import logger
from typehintwhl import __version__
from pathlib import Path
import argparse

__all__ = ["run"]

DESCRIPTION = f"""
Distributes a directory of stub files within a package directory, \
enabling you to neatly organize your stub files.
"""

VERSION = f"""
%(prog)s {__version__}
Copyright (C) 2024 Isaiah Coroama. All rights reserved.
"""

def prepare_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="typehintwhl",
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--package",
        metavar="DIR",
        help="The directory to target."
    )

    parser.add_argument(
        "--stub",
        metavar="DIR",
        help="The directory that contains the stub files to be distributed."
    )

    parser.add_argument(
        "--current",
        metavar="DIR",
        help="Specify the current directory to search through. (Defaults to the current workinkg directory)"
    )

    parser.add_argument(
        "--exclude",
        metavar="NAME",
        help="A list of comma-seperated stub directories or files to ignore."
    )

    parser.add_argument(
        "target",
        nargs=argparse.OPTIONAL,
        metavar="DIR",
        help="The directory to target. (Same as --package)"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=VERSION
    )

    return parser

def run():
    parser = prepare_parser()
    args, argv = parser.parse_known_args()

    args.package = args.package or args.target
    args.current = args.current or Path.cwd()
    
    if "-h" in argv or "--help" in argv:
        parser.print_help()
        parser.exit()

    logger.info(f"typehintwhl {__version__}")
    config = ConfigLoader.loadAll(args.current, args)

    builder = Builder(config.package, config.stub, config.current, config.exclude)
    builder.create()