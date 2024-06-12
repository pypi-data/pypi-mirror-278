# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Module for importing functions and classes at latest drawlib API.

drawlib posses lots of functions and classes on various modules.
This module provides single interface for importing public latest API objects.

``from drawlib.apis import *``

If you want to specify API version, 
please use ``drawlib.<version>.apis`` instead.

"""

from drawlib.v0_1.apis import *
