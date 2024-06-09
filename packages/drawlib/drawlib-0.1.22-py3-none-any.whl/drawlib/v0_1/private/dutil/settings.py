# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Module for drawlib global settings

You can configure

* logging mode
* debug mode or not
* devdebug mode or not
* suppressing-warning or not

at this module.
Please use ``config()`` for changing drawing settings.

"""

# pylint: disable=global-statement
# pylint: disable=logging-fstring-interpolation

import typing
import warnings
import sys
import logging
from drawlib.v0_1.private.logging import logger

__ARG_QUIET = "--drawlib_quiet"
__ARG_DEBUG = "--drawlib_debug"
__ARG_DEVDEBUG = "--drawlib_devdebug"
__ARG_SUPPRESS_WARNING = "--drawlib_suppress_warning"


class DrawlibSettings:
    """Class for managing drawlib settings.

    Please don't use this class directly.
    But use its singleton instance ``dsettings``.

    """

    def __init__(self) -> None:
        """Initialize DrawlibSettings

        It holds only logging mode.
        But logging mode makes debug/devdebug mode.
        These mode change error handling method.

        """

        self._logging_mode: typing.Literal[
            "normal",
            "quiet",
            "verbose",
            "developer",
        ] = "normal"
        self._suppress_warning: bool = False

    def get_logging_mode(self) -> typing.Literal[
        "normal",
        "quiet",
        "verbose",
        "developer",
    ]:
        """Get current logging mode

        Get current logging mode. drawlib has these 4 logging mode.

        * "quiet": Only show error log. logging level CRITICAL.
        * "normal": Normal logging. logging level INFO.
        * "verbose": Show detail logging. logging level DEBUG.
        * "developer": Verbose + disable error handling. logging level DEBUG.

        Returns:
            str: current logging mode.

        """
        return self._logging_mode

    def set_logging_mode(
        self,
        mode: typing.Literal["normal", "quiet", "verbose", "developer"],
    ) -> None:
        """Set logging mode

        * "quiet" sets logging level CRITICAL
        * "normal" sets logging level INFO
        * "verbose" sets logging level DEBUG
        * "developer" sets logging level DEBUG

        Settung "verbose" enables debug mode.
        Setting "developer" enables debug mode and devdebug mode.
        Stacktrace is shown when error happens on debug mode.
        Error handling is disabled on devdebug mode.

        Args:
            mode: one of "normal", "quiet", "verbose", "developer".

        Returns:
            None

        Note:
            if selected mode string is not supported, call ``sys.exit(1)``

        """

        if mode == "normal":
            logger.setLevel(logging.INFO)
        elif mode in ["verbose", "developer"]:
            logger.setLevel(logging.DEBUG)
        elif mode == "quiet":
            logger.setLevel(logging.CRITICAL)
        else:
            logger.critical(f'logging mode "{mode}" is not supported.')
            sys.exit(1)
        # logger.debug(f'set_log_mode(): "{mode}"')

        self._logging_mode = mode

    def get_suppress_warning(self) -> bool:
        """Get supressing-warning is enabled or not.

        Matplot warnings are shown when it detects small troubles.
        Such as draw non ascii text without specifying font.
        If suppress warning is enabled, suppress those warnings.

        Returns:
            bool: whether suppressing warning or not

        """

        return self._suppress_warning

    def set_suppress_warning(self, enable: bool) -> None:
        """Set enable/disable suppress-warning

        Matplot warnings are shown when it detects small troubles.
        Such as draw non ascii text without specifying font.
        If suppress warning is enabled, suppress those warnings.

        Args:
            enable: True means suppress

        Returns:
            None

        """

        if enable:
            warnings.filterwarnings("ignore")
        else:
            warnings.filterwarnings("default")

        logger.debug(f'set_suppress_warning(): "{enable}"')
        self._suppress_warning = enable

    def is_debug_mode(self) -> bool:
        """Get whether debug mode is enabled or not

        Stacktrace will be shown when error happens on debug mode.
        You can set debug mode at ``set_logging_mode()``.
        Setting "verbose" and "developer" enables debug mode.

        Returns:
            bool: whether debug mode is enabled or not

        """

        if self._logging_mode == "verbose":
            return True
        if self._logging_mode == "developer":
            return True

        return False

    def is_developer_debug_mode(self) -> bool:
        """Get whether devdebug mode is enabled or not

        Error handling is disabled on devdebug mode which is useful on
        development and testing.
        You can set devdebug mode at ``set_logging_mode()``.
        Setting "developer" enables devdebug mode.
        When you run pytest, devdebug is automatically enabled.

        Returns:
            bool: whether devdebug mode is enabled or not

        """

        return self._logging_mode == "developer"


dutil_settings = DrawlibSettings()
"""Singleton instance of class Settings"""

# set logging mode normal first.
dutil_settings.set_logging_mode("normal")

# set logging mode quiet if selected
if __ARG_QUIET in sys.argv:
    dutil_settings.set_logging_mode("quiet")

# set logging mode debug if selected
if __ARG_DEBUG in sys.argv:
    if __ARG_QUIET in sys.argv:
        logger.critical(f"option {__ARG_QUIET} can not be used with option {__ARG_DEBUG}")
        sys.exit(1)
    dutil_settings.set_logging_mode("quiet")

# set logging mode developer if selected
if __ARG_DEVDEBUG in sys.argv:
    if __ARG_QUIET in sys.argv:
        logger.critical(f"option {__ARG_QUIET} can not be used with option {__ARG_DEVDEBUG}")
        sys.exit(1)
    dutil_settings.set_logging_mode("developer")

# set logging mode developer on pytest
for arg in sys.argv:
    # command pytest can be abspath
    if arg.endswith("pytest"):
        if __ARG_QUIET in sys.argv:
            logger.critical(f"option {__ARG_QUIET} can not be used " f"with option {__ARG_DEVDEBUG}")
            sys.exit(1)
        dutil_settings.set_logging_mode("developer")
        break

if __ARG_SUPPRESS_WARNING in sys.argv:
    dutil_settings.set_suppress_warning(True)
