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

import pfDevTools.Utils


# -- Classes
class DryRun:
    """A tool to clean the project."""

    def __init__(self, arguments, debug_on: bool = False):
        """Constructor based on command line arguments."""

        self._debug_on: bool = debug_on

        if len(arguments) != 0:
            raise RuntimeError('Invalid arguments. Maybe start with `pf --help?')

    def run(self) -> None:
        command_line: str = 'scons --dry-run --tree=all --debug=explain'
        if self._debug_on:
            command_line += ' --debug_on'

        pfDevTools.Utils.shellCommand(command_line)

    @classmethod
    def name(cls) -> str:
        return 'dryrun'

    @classmethod
    def usage(cls) -> None:
        print('   dryrun                                - Simulate building the project.')
