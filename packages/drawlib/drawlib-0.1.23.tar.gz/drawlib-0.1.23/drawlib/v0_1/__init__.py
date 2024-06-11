# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""drawlib API 0.1 package.

this package contains API v0.1 modules.

- basic: provides single interface of basic classes and functions.
- advance: provides single interface of basic and advance classes and functions.
- settings: provides application setting interfaces.

These implementation will not be changed after new API is released.
We recommend user code change before API deprication.

"""

from typing import Final
import drawlib

# this API package is latest now. So, API version is same to software's one.
# When you create newer API, please set string value instead.
VERSION: Final[str] = drawlib.VERSION

# might not be changed
__version__: Final[str] = VERSION
