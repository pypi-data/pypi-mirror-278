# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Handle drawlib command

Entry point ``__main__`` calls this module's function ``call()``.
After that class ``DrawlibArgParser`` parse options.
Then operate appropriate actions.

"""

import os
import sys
import argparse
from typing import Optional, List, Literal
import importlib.util
import traceback

import drawlib
import drawlib.v0_1
from drawlib.v0_1.private.logging import logger
from drawlib.v0_1.private.dutil.settings import dutil_settings
from drawlib.v0_1.private.util import (
    error_handler,
    get_script_relative_path,
    purge_font_cache,
)
from drawlib.v0_1.private.core_canvas.canvas import clear
from drawlib.v0_1.private.dutil.dutil_canvas import initialize


def call() -> None:
    """drawlib command handling function.

    This method is called from each API's ``__main__`` module.
    If the API is latest, called from root package's ``__main__`` module too.

    Abstract procedure of this function.

    1. Crate DrawlibArgParser instance.
    2. Parse command line options
    3. If options requests version info, show it and quit.
    4. Apply options such as logging level
    5. get target files and directories which drawlib run.
    6. call ``tools.run()`` for each files, directories

    Returns:
        None

    """

    argparser = DrawlibArgParser()
    argparser.parse()

    # show version
    if argparser.is_show_version():
        logger.critical(f"software={drawlib.VERSION}")
        logger.critical(f"api={drawlib.v0_1.VERSION}")
        sys.exit(0)

    # purge font cache
    if argparser.is_purge_font_cache():
        purge_font_cache()
        sys.exit(0)

    # set logging mode
    logging_mode = argparser.get_logging_mode()
    if logging_mode == "quiet":
        dutil_settings.set_logging_mode("quiet")
    elif logging_mode == "normal":
        dutil_settings.set_logging_mode("normal")
    elif logging_mode == "verbose":
        dutil_settings.set_logging_mode("verbose")
    elif logging_mode == "developer":
        dutil_settings.set_logging_mode("developer")
    else:
        raise ValueError()

    # get execution mode
    exec_mode = argparser.get_exec_mode()

    # get target files and directories
    target_files = argparser.get_target_files()

    # if no target, quit with error code
    if len(target_files) == 0:
        logger.critical("no input files and directories")
        logger.critical('check options with "drawlib --help"')
        sys.exit(1)

    # handle target one by one.
    for target_file in target_files:
        # skip wrong file
        if not os.path.isfile(target_file) and not os.path.isdir(target_file):
            msg = f'ignore arg "{target_file}" since it is not a file/dir path'
            logger.warning(msg)
            continue

        # get file path
        abspath = os.path.abspath(target_file)
        realpath = os.path.realpath(abspath)

        # execute file or directory
        executer = DrawlibExecuter(mode=exec_mode)
        executer.execute(realpath)


def show_version(): ...


class DrawlibArgParser:
    """drawlib ArgParser Class"""

    def __init__(self) -> None:
        """Initializa DrawlibArgParser

        In this method, create ``ArgumentParser`` instance and
        define command line options.

        Returns:
            None

        """

        parser = argparse.ArgumentParser(
            description="Ilustration as code by python",
        )

        # main
        parser.add_argument(
            "file_or_directory",
            nargs="...",
            help="Target python file or directory which contains python codes",
        )

        # special mode options
        parser.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="Show version.",
        )
        parser.add_argument(
            "--purge_font_cache",
            action="store_true",
            help="Purge cached font files.",
        )

        # exec mode options
        parser.add_argument(
            "--disable_auto_clear",
            action="store_true",
            help="Disable clearing canvas per executing drawing code files.",
        )
        parser.add_argument(
            "--enable_auto_initialize",
            action="store_true",
            help="Enable initializing theme/canvas/image_cache per executing drawing code files.",
        )

        # log options
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Enable quiet logging. show only error messages",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose logging.",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Enable verbose logging. Equivalent to --verbose",
        )
        parser.add_argument(
            "--developer",
            action="store_true",
            help=("Enable verbose logging. Disable error handling which is designed for library users."),
        )

        self._parser = parser
        self._positional_args: Optional[List[str]] = None
        self._name_args: Optional[argparse.Namespace] = None

    def parse(self) -> None:
        """Parse command line options.

        Parse command line options.
        This method must be called before calling get methods.

        Returns:
            None

        """

        # special options
        self._name_args, _ = self._parser.parse_known_args()

        # main option
        args = self._parser.parse_args()
        self._positional_args = args.file_or_directory

    def is_show_version(self) -> bool:
        """show version if option ``-v/`` or ``--version`` exists. And then quit.

        Check whether option has ``-v`` or ``--version``.
        If yes, show version. And then, quit with ``sys.exit(0)``.

        Returns:
            None

        """

        if self._name_args is None:
            self.parse()
        return self._name_args.version

    def is_purge_font_cache(self) -> bool:
        if self._name_args is None:
            self.parse()
        return self._name_args.purge_font_cache

    def get_logging_mode(self) -> Literal["quiet", "normal", "verbose", "developer"]:
        """Check named args and apply appropriate configs.

        Check these named argses. And do appropriate actions.

        * --quiet: make logging mode quiet
        * --debug: make logging mode verbose
        * --devdebug: make logging mode developer

        Returns:
            None

        """

        if self._name_args is None:
            self.parse()

        if self._name_args.quiet and (self._name_args.verbose or self._name_args.developer):
            raise ValueError("option --quiet can't use with option --debug and --devdebug")

        if self._name_args.quiet:
            return "quiet"

        if self._name_args.verbose:
            return "verbose"

        if self._name_args.debug:
            return "verbose"

        if self._name_args.developer:
            return "developer"

        return "normal"

    def get_exec_mode(self) -> Literal["none", "auto_clear", "auto_initialize"]:
        if self._name_args is None:
            self.parse()

        if self._name_args.enable_auto_initialize:
            return "auto_initialize"

        if self._name_args.disable_auto_clear:
            return "none"

        return "auto_clear"

    def get_target_files(self) -> List[str]:
        """Get positional args. which are files and directories.

        drawlib command requires files and directories as positional args.
        They are the target of ``tool.run()`` function.
        It means specified file or files inside directories
        are called from python.
        If those python files are drawlib's one, generate images.

        This method must be called after ``parse()`` method is called.

        Returns:
            List[str]: Positional args (files and directories)

        """

        if self._positional_args is None:
            self.parse()

        return self._positional_args


class DrawlibExecuter:

    def __init__(self, mode: Literal["none", "auto_clear", "auto_initialize"]) -> None:
        if mode not in ["none", "auto_clear", "auto_initialize"]:
            raise ValueError(f'Arg mode is "{mode}". But it must be one of ["none", "auto_clear", "auto_initialize"].')
        self._mode = mode
        self._topdir_path: str = ""

    @error_handler
    def execute(self, file_or_directory: str) -> None:
        """Run specified python file or python files in specified directory

        Call python file via OS path.
        When you specify python file, only run it.
        When you specify directory, run all python files recursively inside it.
        Each python files are called only 1 time.
        2nd time call is skipped.

        When file1.py calls ``run("file2.py")`` and file2.py calls
        ``run("file3.py")``, loading file3.py first.
        This recursive load situation can be checked on console.
        Please don't make circular loading situation.

        Note:
            We recommend creating ``.drawlib`` directory and put all python files which are loaded.
            Each drawing python file need to declare only ``run(<path_to_.drawlib>)``.

        Strongly recommend ``auto_clear=True`` when specifying directory.
        If user code doesn't call ``clear()``,
        canvas state is shared between python files.
        It means 2nd draw can contain 1st draw results.
        Default value of ``auto_clear`` is True.

        Args:
            file_or_directory: run target. relative to user script path.
            auto_clear(optional): call ``clear()`` method between running each python files.

        Returns:
            None

        """

        path = get_script_relative_path(file_or_directory)
        if not os.path.exists(path):
            raise ValueError(f'"{path}" does not exist')

        self._add_topdir_to_syspath(path)

        logger.info("Execute python files")
        if os.path.isfile(path):
            if not path.endswith(".py"):
                raise ValueError(f'Unable to run "{path}"')
            self._exec_module(path)
        else:
            file_paths = self._get_python_files(path)
            for file_path in file_paths:
                self._exec_module(file_path)

    def _add_topdir_to_syspath(self, path: str):
        if os.path.isfile(path):
            topdir = os.path.dirname(path)
        else:
            init_path = os.path.join(path, "__init__.py")
            if not os.path.exists(init_path):
                logger.critical(f'Target directory "{path}" does not have __init__.py. Abort.')
                sys.exit(1)
            topdir = path

        package_dir = ""
        while os.path.exists(os.path.join(topdir, "__init__.py")):
            package_dir = topdir
            topdir = os.path.dirname(topdir)

        self._topdir_path = topdir
        logger.info(f'Detect package root "{package_dir}".')
        if topdir not in sys.path:
            sys.path.append(topdir)
            logger.info(f'    - Add parent directory of package root "{topdir}" to Python Path.')
        else:
            logger.info(f'    - Parent of package directory "{topdir}" is already in Python Path.')
        logger.info("")

    def _get_python_files(self, directory: str) -> List[str]:
        python_files: List[str] = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)

        def sort_key(path: str):
            # 1. depth
            # 2. alphabetical order
            return (path.count(os.sep), path)

        sorted_files = sorted(python_files, key=sort_key)
        return sorted_files

    def _exec_module(self, file_path: str) -> None:
        """write docstring later"""

        words = self._get_package_words(file_path)
        self._load_parent_modules(words)

        if self._is_module_loaded(file_path):
            logger.info(f"    - {file_path}")
            return

        # load module
        name = ".".join(words).replace(".py", "")
        mspec = importlib.util.spec_from_file_location(
            name=name,
            location=file_path,
        )
        if mspec is None:
            # need to investigate what situation make this
            logger.info(f"    - {file_path} : skipped with unknown reason.")
            return
        module = importlib.util.module_from_spec(mspec)

        # execute and cache
        try:
            if self._mode == "auto_clear":
                clear()
            elif self._mode == "auto_initialize":
                initialize()
            else:
                ...
            logger.info(f"    - {file_path}")
            mspec.loader.exec_module(module)  # type: ignore[union-attr]
            sys.modules[name] = module

        except Exception as e:  # pylint: disable=broad-exception-caught
            # Please don't raise again.
            # Error handler can't detect exact error location of imported module
            file, line, _, _ = traceback.extract_tb(e.__traceback__)[-1]
            logger.critical(f'{type(e).__name__} at file:"{file}", line:"{line}"')
            logger.critical(str(e))
            logger.debug("")
            logger.debug(traceback.format_exc())
            sys.exit(1)

    def _is_module_loaded(self, module_path: str) -> bool:
        # Normalize the module path to ensure consistent comparison
        module_path = os.path.abspath(module_path)

        for module_name, module in sys.modules.items():
            if module is None:
                continue
            if not hasattr(module, "__file__"):
                continue
            if module.__file__ is None:
                continue

            loaded_module_path = os.path.abspath(module.__file__)
            if loaded_module_path == module_path:
                return True

        return False

    def _get_package_words(self, file_path):
        last_path = file_path.replace(self._topdir_path, "")
        words = last_path.split(os.sep)
        if words[0] == "":
            words = words[1:]
        return words

    def _load_parent_modules(self, words: List[str]):
        for i in range(1, len(words)):
            name = ".".join(words[:i])
            if name in sys.modules:
                continue

            location = os.path.join(self._topdir_path, os.sep.join(words[:i]), "__init__.py")
            if not os.path.exists(location):
                raise ValueError(f'"{location}" does not exist. Please create it first.')

            mspec = importlib.util.spec_from_file_location(
                name=name,
                location=location,
            )
            module = importlib.util.module_from_spec(mspec)
            mspec.loader.exec_module(module)
            sys.modules[name] = module
