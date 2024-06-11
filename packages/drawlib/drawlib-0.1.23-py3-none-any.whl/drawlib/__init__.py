# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""drawlib root package

this package contains latest modules.

- basic: provides single interface of basic classes and functions.
- advance: provides single interface of basic and advance classes and functions.
- settings: provides application setting interfaces.

subpackages contains latest and old implementations.

- drawlib.v0_1: API v0.1 interface (latest)

"""

from typing import Final

# please update here when you release new version
VERSION = "0.1.23"

# might not be changed
LIB_NAME: Final[str] = "drawlib"
AUTHOR: Final[str] = "Yuichi Ito"
CONTACT: Final[str] = "yuichi@yuichi.com"
__version__: Final[str] = VERSION
