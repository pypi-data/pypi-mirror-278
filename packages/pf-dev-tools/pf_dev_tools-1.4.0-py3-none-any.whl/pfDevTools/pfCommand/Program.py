#
# Copyright (c) 2023-present Didier Malenfant
#
# This file is part of pfDevTools.
#
# pfDevTools is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pfDevTools is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with pfDevTools. If not,
# see <https://www.gnu.org/licenses/>.
#

import sys
import traceback
import pfDevTools
import pfDevTools.Utils
import pfDevTools.CoreConfig


# -- Classes
class Program:
    """A tool to program the Analogue Pocket via JTAG."""

    def __init__(self, arguments, debug_on: bool = False):
        """Constructor based on command line arguments."""

        self._debug_on: bool = debug_on

        if len(arguments) > 0:
            raise RuntimeError('Invalid arguments. Maybe start with `pf --help?')

        self._volume_path = pfDevTools.CoreConfig.coreInstallVolumePath()

    def run(self) -> None:
        try:
            command_line: str = 'scons -Q -s program'

            if self._debug_on:
                command_line += ' --debug_on'

            pfDevTools.Utils.shellCommand(command_line)

        except Exception as e:
            if self._debug_on:
                print(traceback.format_exc())
            elif len(str(e)) != 0:
                print(f'ERROR: {e}')
            else:
                print('ERROR: Unknown error while programming Pocket.')

            sys.exit(1)

    @classmethod
    def name(cls) -> str:
        return 'program'

    @classmethod
    def usage(cls) -> None:
        print('   program                               - Build and program the Analogue Pocket.')
