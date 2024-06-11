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

import os
import shutil
import errno
import stat
import time
import sys

from typing import List

if sys.platform == 'win32':
    import subprocess
else:
    import pty


# -- Classes
class Utils:
    @classmethod
    def _handleRemoveReadonly(cls, func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # -- 0777
            func(path)
        else:
            raise

    @classmethod
    def shellCommand(cls, command_and_args: str, capture_output=False) -> List[str]:
        try:
            args: List[str] = command_and_args.split(' ')
            captured_output: str = None
            return_code = None

            # print(f'--- Command {command_and_args}')

            if sys.platform == 'win32':
                if capture_output:
                    result = subprocess.run(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                    captured_output = result.stdout.decode('utf-8')
                else:
                    result = subprocess.run(args, stderr=sys.stderr, stdout=sys.stdout)

                return_code = result.returncode
            else:
                if capture_output:
                    output_bytes: List = []

                    def read_pty_output(fd):
                        data = os.read(fd, 1024)

                        if len(data) != 0:
                            output_bytes.append(data)

                            # -- We don't need to print anything out, we're just capturing.
                            data = bytearray()
                            data.append(0)

                        return data

                    return_code = pty.spawn(args, master_read=read_pty_output)
                    captured_output = b''.join(output_bytes).decode('utf-8')
                else:
                    return_code = pty.spawn(args)

            if return_code != 0:
                raise RuntimeError

            return captured_output.split('\n') if captured_output is not None else []
        except RuntimeError:
            raise
        except SyntaxError:
            raise
        except Exception as e:
            raise RuntimeError(str(e))

    @classmethod
    def commandExists(cls, command: str) -> bool:
        try:
            Utils.shellCommand(f'{"where" if os.name == "nt" else "which"} {command}', capture_output=True)
        except Exception:
            return False

        return True

    @classmethod
    def requireCommand(cls, command: str):
        if not Utils.commandExists(command):
            raise RuntimeError('❌ Cannot find command \'' + command + '\'.')

    @classmethod
    def deleteFolder(cls, folder: str, force_delete: bool = False):
        if os.path.exists(folder):
            if force_delete is True:
                ignore_errors = False
                on_error = Utils._handleRemoveReadonly
            else:
                ignore_errors = True
                on_error = None

            shutil.rmtree(folder, ignore_errors=ignore_errors, onerror=on_error)

    @classmethod
    def fileOlderThan(cls, path: str, time_in_seconds: int):
        if not os.path.exists(path):
            return True

        return (time.time() - os.path.getmtime(path)) > time_in_seconds
