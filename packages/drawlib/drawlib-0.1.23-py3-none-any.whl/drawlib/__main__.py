# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Entry point of ``drawlib``

When you run ``drawlib <options>`` or ``python -m drawlib <options>``, 
this module will be called.
And then, latest API's ``command.call()`` will be called.

"""

from drawlib.v0_1.private.command import call


def main():
    call()


if __name__ == "__main__":
    main()
