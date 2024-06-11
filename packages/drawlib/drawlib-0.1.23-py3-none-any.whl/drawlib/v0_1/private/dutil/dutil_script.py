# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""drawlib utility module

This module contains utility functions which is called many points.
Regarding drawing utility functions, they are defined at ``core.util``.

"""

from drawlib.v0_1.private.util import (
    get_script_function_name as get_function_name,
    get_script_path,
    get_script_relative_path as get_relative_path,
)
