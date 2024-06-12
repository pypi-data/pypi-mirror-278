# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Setup global logger instance.

logging.logger is initialized and configured at this module.
This logger instance is imported at almost all modules in this library.
Module ``settings`` will modify this logger's logging level.

Note:
    Note for drawlib library developers.
    Importing other module will make circular imports.
    Please take care not to import utility modules.

"""

import logging
import drawlib

logger = logging.getLogger(drawlib.LIB_NAME)
"""Global logger object which is shared on this library. 
Logger name comes from ``drawlib.LIB_NAME``.
"""

# set default level
logger.setLevel(logging.INFO)

# set default log format
_formatter = logging.Formatter("%(message)s")
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)
logger.addHandler(_handler)
