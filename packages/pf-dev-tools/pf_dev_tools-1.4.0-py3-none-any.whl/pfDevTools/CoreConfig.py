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
import getpass

from typing import Dict
from typing import List
from sys import platform
from enum import IntFlag

from .Exceptions import ArgumentError

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


# -- Constants
class FileParameter(IntFlag):
    USER_RELOADABLE = 0x0001
    CORE_SPECIFIC = 0x0002
    NON_VOLATILE_FILENAME = 0x0004
    READ_ONLY = 0x0008
    INSTANCE_JSON = 0x0010
    INIT_NON_VOLATILE_DATA_ON_LOAD = 0x0020
    RESET_CORE_WHILE_LOADING = 0x0040
    RESTART_CORE_AFTER_LOADING = 0x0080
    FULL_RELOAD_CORE = 0x0100
    PERSIST_BROWSED_FILENAME = 0x0200


# -- Classes
class CoreConfig:
    """A class for openFPGA core configurations"""

    @classmethod
    def _greatestCommonFactor(cls, a, b):
        return abs(a) if b == 0 else CoreConfig._greatestCommonFactor(b, a % b)

    @classmethod
    def coreInstallVolumePath(cls) -> str:
        volume_path: str = os.environ.get('PF_CORE_INSTALL_PATH')
        if volume_path is None:
            if platform == 'darwin':
                volume_path = '/Volumes/POCKET'
            elif platform == 'linux':
                volume_path = os.path.join('/media', getpass.getuser(), 'POCKET')
            elif platform == 'win32':
                volume_path = 'P:'
            else:
                raise RuntimeError('PF_CORE_INSTALL_PATH is not defined in the environment.')

        return volume_path

    @classmethod
    def _numericValueToString(cls, value, default_value=None, signed_allowed: bool = False):
        if value is None:
            return default_value

        if isinstance(value, str):
            if not value.startswith('0x') or len(value) > 10:
                return None

            try:
                int(value[2:], 16)
            except Exception:
                return None

            return value
        else:
            if signed_allowed:
                if value > 2147483647 or value < -2147483648:
                    return None
            elif value < 0:
                raise None

            if value > 0xFFFFFFFF:
                return None

            return f"{value}"

    @classmethod
    def coreSectionName(cls, core_id: str) -> str:
        return f'Cores.{core_id}'

    @classmethod
    def fileSlotSectionName(cls, slot_id: str) -> str:
        return f'Files.{slot_id}'

    @classmethod
    def variableSectionName(cls, variable_id: str) -> str:
        return f'Variables.{variable_id}'

    @classmethod
    def controllerSectionName(cls, controller_id: str) -> str:
        return f'Controllers.{controller_id}'

    def __init__(self, config_filename: str):
        """Constructor based on config file path."""

        self.config_filename: str = config_filename
        self._platform_short_name = None
        self._video_width = None
        self._video_height = None
        self._video_ratio_gcf = None

        components = os.path.splitext(self.config_filename)
        if len(components) != 2 or components[1] != '.toml':
            raise ArgumentError('Config file needs to be a toml file.')

        if not os.path.exists(self.config_filename):
            raise ArgumentError('Config file \'' + self.config_filename + '\' does not exist.')

        self.config_file_folder = os.path.dirname(self.config_filename)

        with open(self.config_filename, mode="rb") as fp:
            self._config = tomllib.load(fp)

        # -- If no cores are specified, we default to this single one.
        if self._config.get('Cores', None) is None:
            self._config['Cores'] = {'0': {'name': 'default',
                                           'source_file': 'pf_core.rbf',
                                           'filename': 'bitstream.rbf_r'}}

    def _getConfigCategory(self, category_name: str) -> Dict:
        return self._config.get(category_name, {})

    def _getConfigParam(self, section_name: str, param_name: str, optional=False):
        section: Dict = None

        section_name_parts = section_name.split('.')
        number_of_parts = len(section_name_parts)
        if number_of_parts > 1:
            if number_of_parts > 2:
                raise ArgumentError(f'Invalid section named {section_name} is being searched config file.')

            from_config: Dict = self._config.get(section_name_parts[0])
            section = from_config.get(section_name_parts[1], None)
        else:
            section = self._config.get(section_name, None)

        if section is None:
            if optional is False:
                raise ArgumentError(f'Can\'t find section named {section_name} in config file.')
            else:
                return None

        param = section.get(param_name, None)
        if param is None:
            if optional is False:
                raise ArgumentError(f'Can\'t find parameter {param_name} in section {section_name} in config file.')
            else:
                return None

        return param

    def _readBooleanFromConfigParam(self, section_name: str, param_name: str, optional=False) -> bool:
        value: bool = self._getConfigParam(section_name, param_name, optional=optional)
        if value is not None and not isinstance(value, bool):
            raise ArgumentError(f'Found invalid value \'{value}\' for \'{param_name}\' in \'{section_name}\'. Should be a boolean.')

        return value

    def _readBooleanFromFileParam(self, slot_id: str, param_name: str, optional=False) -> bool:
        return self._readBooleanFromConfigParam(CoreConfig.fileSlotSectionName(slot_id), param_name, optional=optional)

    def _readBooleanFromVariableParam(self, variable_id: str, param_name: str, optional=False) -> bool:
        return self._readBooleanFromConfigParam(CoreConfig.variableSectionName(variable_id), param_name, optional=optional)

    def platformName(self) -> str:
        platform_name: str = self._getConfigParam('Platform', 'name')
        if len(platform_name) > 31:
            raise ArgumentError(f'Invalid platform name \'{platform_name}\'. Maximum length is 31 characters.')

        return platform_name

    def platformImage(self) -> str:
        return os.path.join(self.config_file_folder, self._getConfigParam('Platform', 'image'))

    def platformShortName(self) -> str:
        if self._platform_short_name is None:
            self._platform_short_name = self._getConfigParam('Platform', 'short_name')

            if len(self._platform_short_name) > 31:
                raise ArgumentError(f'Invalid platform short name \'{self._platform_short_name}\'. Maximum length is 31 characters.')

            for c in self._platform_short_name:
                if (c.isalnum() is False) or c.isupper():
                    raise ArgumentError(f'Invalid platform short name \'{self._platform_short_name}\'. Should be lower-case and can only contain a-z, 0-9 or _.')

        return self._platform_short_name

    def platformCategory(self) -> str:
        category: str = self._getConfigParam('Platform', 'category')
        if len(category) > 31:
            raise ArgumentError(f'Invalid platform category \'{category}\'. Maximum length is 31 characters.')

        return category

    def platformDescription(self) -> str:
        value = self._getConfigParam('Platform', 'description')
        if len(value) > 63:
            raise ArgumentError(f'Invalid platform description \'{value}\'. Maximum length is 63 characters.')

        return value

    def platformInfoFile(self) -> str:
        platform_config = self._config.get('Platform', None)
        if platform_config is not None:
            info_file = platform_config.get('info', None)

            if info_file is not None:
                return os.path.expandvars(os.path.join(self.config_file_folder, info_file))

        return None

    def coresList(self) -> List[str]:
        list = self._getConfigCategory('Cores').keys()
        if len(list) == 0:
            raise ArgumentError('Did not find any cores to build in the config file.')
        if len(list) > 8:
            raise ArgumentError('Found more than 8 cores in the config file.')

        for core_id in list:
            if int(core_id) > 0xFFFF:
                raise ArgumentError(f'Found invalid core id \'{CoreConfig.coreSectionName(core_id)}\'. ID should fit in a 16-bit unsigned.')

        return list

    def coreName(self, core_id: str) -> str:
        core_section_name: str = CoreConfig.coreSectionName(core_id)
        core_name: str = self._getConfigParam(core_section_name, 'name', optional=True)
        if core_name is not None and len(core_name) > 15:
            raise ArgumentError(f'Found invalid core name for \'{core_section_name}\'. Maximum length is 15 characters.')

        return core_name

    def coreFilename(self, core_id: str) -> str:
        core_section_name: str = CoreConfig.coreSectionName(core_id)
        filename: str = self._getConfigParam(core_section_name, 'filename')
        if len(filename) > 15:
            raise ArgumentError(f'Found invalid core filename for \'{core_section_name}\'. Maximum length is 15 characters.')

        return filename

    def coreSourceFile(self, core_id: str) -> str:
        return self._getConfigParam(CoreConfig.coreSectionName(core_id), 'source_file')

    def buildVersion(self) -> str:
        value = self._getConfigParam('Build', 'version')
        if len(value) > 31:
            raise ArgumentError(f'Invalid platform version \'{value}\'. Maximum length is 31 characters.')

        return value

    def authorName(self) -> str:
        value = self._getConfigParam('Author', 'name')
        if len(value) > 31:
            raise ArgumentError(f'Invalid platform author \'{value}\'. Maximum length is 31 characters.')

        return value

    def authorIcon(self) -> str:
        return os.path.join(self.config_file_folder, self._getConfigParam('Author', 'icon'))

    def authorURL(self) -> str:
        value = self._getConfigParam('Author', 'url')
        if len(value) > 63:
            raise ArgumentError(f'Invalid platform URL \'{value}\'. Maximum length is 63 characters.')

        return value

    def videoWidth(self) -> int:
        if self._video_width is None:
            self._video_width = self._getConfigParam('Hardware', 'video_width')

        return self._video_width

    def videoHeight(self) -> int:
        if self._video_height is None:
            self._video_height = self._getConfigParam('Hardware', 'video_height')

        return self._video_height

    def _videoRatioGcf(self) -> int:
        if self._video_ratio_gcf is None:
            self._video_ratio_gcf = CoreConfig._greatestCommonFactor(int(self.videoWidth()), int(self.videoHeight()))

        return self._video_ratio_gcf

    def videoHorizontalAspectRatio(self) -> str:
        common_factor: int = self._videoRatioGcf()
        if common_factor == 1:
            raise ArgumentError(f'Could not find a valid common factor for aspect ratio given a resolution of {self.videoWidth()}x{self.videoHeight()}.')

        return self.videoWidth() / common_factor

    def videoVerticalAspectRatio(self) -> str:
        common_factor: int = self._videoRatioGcf()
        if common_factor == 1:
            raise ArgumentError(f'Could not find a valid common factor for aspect ratio given a resolution of {self.videoWidth()}x{self.videoHeight()}.')

        return self.videoHeight() / common_factor

    def videoRotationAngle(self) -> int:
        value = self._getConfigParam('Hardware', 'video_rotation_angle', optional=True)
        if value is None:
            value = 0
        elif not isinstance(value, int) or (value != 0 and value != 90 and value != 180 and value != 270):
            raise ArgumentError(f'Invalid platform video_rotation_angle \'{value}\'. Should be 0, 90, 180 or 270.')

        return value

    def videoFlipHorizontal(self) -> bool:
        value = self._readBooleanFromConfigParam('Hardware', 'video_flip_horizontal', optional=True)
        return value if value is not None else False

    def videoFlipVertical(self) -> bool:
        value = self._readBooleanFromConfigParam('Hardware', 'video_flip_vertical', optional=True)
        return value if value is not None else False

    def linkPort(self) -> bool:
        link_port: bool = self._readBooleanFromConfigParam('Hardware', 'link_port', optional=True)
        return link_port if link_port is not None else False

    def powerCartridgePort(self) -> bool:
        power_port: bool = self._readBooleanFromConfigParam('Hardware', 'power_cartridge_port', optional=True)
        return power_port if power_port is not None else False

    def displayModes(self) -> List[str]:
        values: Dict[str, str] = {
            'crt_trinitron': '0x10',
            'grayscale_lcd': '0x20',
            'original_gb_dmg': '0x21',
            'original_gbp': '0x22',
            'original_gbp_light': '0x23',
            'reflective_color': '0x30',
            'original_gbc': '0x31',
            'original_gbc+': '0x32',
            'backlit_color': '0x40',
            'original_gba': '0x41',
            'original_gba_sp101': '0x42',
            'original_gg': '0x51',
            'original_gg+': '0x52',
            'pinball_neon_matrix': '0xE0'
        }
        selected_display_modes: List[str] = self._getConfigParam('Hardware', 'display_modes', optional=True)
        output_list: List[str] = []

        if selected_display_modes is not None:
            for display_mode in selected_display_modes:
                display_code = values[display_mode]
                if display_code is None:
                    raise ArgumentError(f'Found invalid display mode \'{display_mode}\'.')
                output_list.append(display_code)

        return output_list

    def fullPlatformName(self) -> str:
        return f'{self.authorName()}.{self.platformShortName()}'

    def fileSlotList(self) -> List[str]:
        list = self._getConfigCategory('Files').keys()
        if len(list) > 32:
            raise ArgumentError('Found more than 32 file slots in the config file.')

        for slot_id in list:
            if int(slot_id) > 0xFFFF:
                raise ArgumentError(f'Found invalid file slot id \'{CoreConfig.fileSlotSectionName(slot_id)}\'. Must be a 16-bit unsigned integer.')

        return list

    def fileSlotName(self, slot_id: str) -> str:
        file_section_name: str = CoreConfig.fileSlotSectionName(slot_id)
        slot_name: str = self._getConfigParam(file_section_name, 'name')
        if len(slot_name) > 15:
            raise ArgumentError(f'Found invalid slot name for \'{file_section_name}\'. Maximum length is 15 characters.')

        return slot_name

    def fileSlotRequired(self, slot_id: str) -> bool:
        return self._readBooleanFromFileParam(slot_id, 'required', optional=True) or True

    def fileSlotDeferLoading(self, slot_id: str) -> bool:
        return self._readBooleanFromFileParam(slot_id, 'defer_loading', optional=True) or False

    def fileSlotSecondary(self, slot_id: str) -> bool:
        return self._readBooleanFromFileParam(slot_id, 'secondary', optional=True) or False

    def fileSlotNonVolatile(self, slot_id: str) -> bool:
        return self._readBooleanFromFileParam(slot_id, 'non_volatile', optional=True) or False

    def fileSlotParameters(self, slot_id: str) -> int:
        values: Dict[str, int] = {
            'user-reloadable': FileParameter.USER_RELOADABLE,
            'core-specific': FileParameter.CORE_SPECIFIC,
            'non-volatile-filename': FileParameter.NON_VOLATILE_FILENAME,
            'read-only': FileParameter.READ_ONLY,
            'instance-json': FileParameter.INSTANCE_JSON,
            'init-non-volatile-data-on-load': FileParameter.INIT_NON_VOLATILE_DATA_ON_LOAD,
            'reset-core-while-loading': FileParameter.RESET_CORE_WHILE_LOADING,
            'restart-core-after-loading': FileParameter.RESTART_CORE_AFTER_LOADING,
            'full-reload-core': FileParameter.FULL_RELOAD_CORE,
            'persist-browsed-filename': FileParameter.PERSIST_BROWSED_FILENAME
        }

        parameters: int = 0

        file_section_name: str = CoreConfig.fileSlotSectionName(slot_id)
        params = self._getConfigParam(file_section_name, 'parameters', optional=True)
        for param in params if params is not None else []:
            bit_value: FileParameter = values.get(param, None)

            if bit_value is None:
                raise ArgumentError(f'Unknown data slot parameter \'{param}\' for file slot \'{file_section_name}\'.')

            parameters |= bit_value

        if parameters & FileParameter.INSTANCE_JSON and not parameters & FileParameter.CORE_SPECIFIC:
            raise ArgumentError(f'\'core-specific\' parameter is required if \'instance-json\' is used for file slot \'{file_section_name}\'.')

        return parameters

    def fileSlotExtensions(self, slot_id: str) -> List[str]:
        file_section_name: str = CoreConfig.fileSlotSectionName(slot_id)
        extensions: List[str] = self._getConfigParam(file_section_name, 'extensions')
        if len(extensions) > 4:
            raise ArgumentError(f'Too many extensions for file slot \'{file_section_name}\'. Limit is 4.')

        for extension in extensions:
            if len(extension) > 7:
                raise ArgumentError(f'Invalid extension \'{extension}\' file slot \'{file_section_name}\'. Maximum length is 7 characters.')

        return extensions

    def fileSlotRequiredSize(self, slot_id: str) -> str:
        file_section_name: str = CoreConfig.fileSlotSectionName(slot_id)
        size = self._getConfigParam(file_section_name, 'required_size', optional=True)
        if size is not None:
            size = CoreConfig._numericValueToString(size)
            if size is None:
                raise ArgumentError(f'Invalid required size for \'{file_section_name}\'. Required size is 32-bit unsigned integer or hex string with 0x prefix.')

        return size

    def fileSlotMaximumSize(self, slot_id: str) -> str:
        file_section_name: str = CoreConfig.fileSlotSectionName(slot_id)
        size = self._getConfigParam(file_section_name, 'maximum_size', optional=True)
        if size is not None:
            size = CoreConfig._numericValueToString(size)

            if size is None:
                raise ArgumentError(f'Invalid maximum size for \'{file_section_name}\'. Maximum size is 32-bit unsigned integer or hex string with 0x prefix.')

        return size

    def fileSlotAddress(self, slot_id: str) -> str:
        file_section_name: str = CoreConfig.fileSlotSectionName(slot_id)
        address = CoreConfig._numericValueToString(self._getConfigParam(file_section_name, 'address'))
        if address is None:
            raise ArgumentError(f'Invalid address for \'{file_section_name}\'. Maximum size is 32-bit unsigned integer or hex string with 0x prefix.')

        return address

    def fileSlotFilePath(self, slot_id: str) -> str:
        file_section_name: str = CoreConfig.fileSlotSectionName(slot_id)
        file_path: str = self._getConfigParam(file_section_name, 'filename', optional=True)
        if file_path is None:
            return None

        file_path = os.path.expandvars(os.path.join(self.config_file_folder, file_path))

        if not os.path.exists(file_path):
            raise ArgumentError(f'Cannot find file \'{file_path}\' needed to include with the core.')

        return file_path

    def fileSlotFilename(self, slot_id: str) -> str:
        file_path = self.fileSlotFilePath(slot_id)
        if file_path is None:
            return None

        base_filename = os.path.basename(file_path)
        if len(base_filename) > 31:
            file_section_name: str = CoreConfig.fileSlotSectionName(slot_id)
            raise ArgumentError(f'Found invalid filename for \'{file_section_name}\'. Maximum length is 31 characters.')

        return base_filename

    def fileSlotFilesToInclude(self, slot_id: str) -> List[str]:
        file_section_name: str = CoreConfig.fileSlotSectionName(slot_id)
        files: List[str] = []
        for file_path in self._getConfigParam(file_section_name, 'include_files', optional=True) or []:
            filename = os.path.basename(file_path)
            if len(filename) > 31:
                raise ArgumentError(f'Found invalid filename for \'{file_section_name}\'. Maximum length is 31 characters.')

            file_path = os.path.expandvars(os.path.join(self.config_file_folder, file_path))

            if not os.path.exists(file_path):
                raise ArgumentError(f'Cannot find file \'{file_path}\' needed to include with the core.')

            files.append(file_path)

        return files

    def variableList(self) -> List[str]:
        list = self._getConfigCategory('Variables').keys()
        if len(list) > 16:
            raise ArgumentError('Found more than 16 variables in the config file.')

        for variable_id in list:
            if int(variable_id) > 0xFFFF:
                raise ArgumentError(f'Found invalid variable id \'{CoreConfig.variableSectionName(variable_id)}\'. Must be a 16-bit unsigned integer.')

        return list

    def variableName(self, variable_id: str) -> str:
        variable_section_name: str = CoreConfig.variableSectionName(variable_id)
        variable_name: str = self._getConfigParam(variable_section_name, 'name')
        if len(variable_name) > 23:
            raise ArgumentError(f'Found invalid variable name for \'{variable_section_name}\'. Maximum length is 23 characters.')

        return variable_name

    def variableType(self, variable_id: str) -> str:
        values: Dict[str, int] = {
            'radio_button': 'radio',
            'checkbox': 'check',
            'slider': 'slider_u32',
            'list': 'list',
            'number': 'number_u32',
            'action': 'action'
        }

        variable_section_name: str = CoreConfig.variableSectionName(variable_id)
        variable_type: str = self._getConfigParam(variable_section_name, 'type')
        json_variable_type: str = values.get(variable_type, None)
        if json_variable_type is None:
            raise ArgumentError(f'Found invalid variable type \'{variable_type}\' for \'{variable_section_name}\'.')

        return json_variable_type

    def variableIsEnabled(self, variable_id: str) -> bool:
        return self._readBooleanFromVariableParam(variable_id, 'enabled', optional=True) or True

    def variableAddress(self, variable_id: str) -> str:
        variable_section_name: str = CoreConfig.variableSectionName(variable_id)
        address = CoreConfig._numericValueToString(self._getConfigParam(variable_section_name, 'address'))
        if address is None:
            raise ArgumentError(f'Invalid \'address\' for \'{variable_section_name}\'. Must be a 32-bit unsigned integer or hex string.')

        return address

    def variableIsPersistent(self, variable_id: str) -> bool:
        return self._readBooleanFromVariableParam(variable_id, 'persistent', optional=True)

    def variableIsWriteOnly(self, variable_id: str) -> bool:
        return self._readBooleanFromVariableParam(variable_id, 'write-only', optional=True)

    def variableDefaultBooleanValue(self, variable_id: str) -> bool:
        value: bool = self._readBooleanFromVariableParam(variable_id, 'default')
        if value is None:
            raise ArgumentError(f'Invalid or missing \'default\' for \'{CoreConfig.variableSectionName(variable_id)}\'.')

        return value

    def variableIntOrHexStringValue(self, variable_id: str, value_name: str, optional: bool = False, signed_allowed: bool = False):
        variable_section_name: str = CoreConfig.variableSectionName(variable_id)
        value = self._getConfigParam(variable_section_name, value_name, optional=optional)
        if value is not None:
            value = CoreConfig._numericValueToString(value, signed_allowed)
            if value is None:
                sign_string = 'signed' if signed_allowed else 'unsigned'
                raise ArgumentError(f'Invalid \'{value_name}\' for \'{variable_section_name}\'. Must be a 32-bit {sign_string} integer or hex string.')

        return value

    def variableGroup(self, variable_id: str):
        return self.variableIntOrHexStringValue(variable_id, 'group')

    def variableValueOn(self, variable_id: str):
        return self.variableIntOrHexStringValue(variable_id, 'value_on')

    def variableValueOff(self, variable_id: str):
        return self.variableIntOrHexStringValue(variable_id, 'value_off', optional=True) or '0'

    def variableMask(self, variable_id: str):
        return self.variableIntOrHexStringValue(variable_id, 'mask', optional=True)

    def variableDefaultIntOrHexValue(self, variable_id: str):
        return self.variableIntOrHexStringValue(variable_id, 'default')

    def variableValue(self, variable_id: str):
        return self.variableIntOrHexStringValue(variable_id, 'value', signed_allowed=True)

    def variableValueIsSigned(self, variable_id: str):
        return self._readBooleanFromVariableParam(variable_id, 'signed_value', optional=True) or False

    def variableMinimumValue(self, variable_id: str):
        return self.variableIntOrHexStringValue(variable_id, 'minimum_value', signed_allowed=True if self.variableValueIsSigned(variable_id) is True else False)

    def variableMaximumValue(self, variable_id: str):
        return self.variableIntOrHexStringValue(variable_id, 'maximum_value', signed_allowed=True if self.variableValueIsSigned(variable_id) is True else False)

    def variableSmallStep(self, variable_id: str):
        return self.variableIntOrHexStringValue(variable_id, 'small_step', signed_allowed=True if self.variableValueIsSigned(variable_id) is True else False)

    def variableLargeStep(self, variable_id: str):
        return self.variableIntOrHexStringValue(variable_id, 'large_step', signed_allowed=True if self.variableValueIsSigned(variable_id) is True else False)

    def variableOptions(self, variable_id: str):
        variable_section_name: str = CoreConfig.variableSectionName(variable_id)
        options = self._getConfigParam(variable_section_name, 'choices')
        if len(options) > 16:
            raise ArgumentError(f'Too many options for variable \'{variable_section_name}\'. Maximum supported is 16.')

        results = []
        for option in options:
            if len(option) != 2:
                raise ArgumentError(f'Invalid option for variable \'{variable_section_name}\'. Format is [ <name>, <value> ].')

            name: str = option[0]
            if len(name) > 23:
                raise ArgumentError(f'Invalid option name \'{name}\' for variable \'{variable_section_name}\'. Maximum length is 23 characters.')

            value_as_string = CoreConfig._numericValueToString(option[1], signed_allowed=True)
            if value_as_string is None:
                raise ArgumentError(f'Invalid option value \'{option[1]}\' for variable \'{variable_section_name}\'. Must be a 32-bit integer or hex string.')

            results.append([name, value_as_string])

        return results

    def controllerList(self) -> List[str]:
        list = self._getConfigCategory('Controllers').keys()
        if len(list) > 4:
            raise ArgumentError('Found more than 4 controllers in the config file.')

        for controller_id in list:
            id_as_int: int = int(controller_id)
            if id_as_int < 1 or id_as_int > 4:
                raise ArgumentError(f'Found invalid controller id \'{CoreConfig.controllerSectionName(controller_id)}\'. ID should be between 1 and 4.')

        return list

    def controllerKeyMapping(self, controller_id: str) -> List[List[str]]:
        values: Dict[str, int] = {
            'A': 'pad_btn_a',
            'B': 'pad_btn_b',
            'X': 'pad_btn_x',
            'Y': 'pad_btn_y',
            'L': 'pad_trig_l',
            'R': 'pad_trig_r',
            'Start': 'pad_btn_start',
            'Select': 'pad_btn_select',
        }

        controller_section_name: str = CoreConfig.controllerSectionName(controller_id)
        mappings = self._getConfigParam(controller_section_name, 'key_mapping')

        if len(mappings) > 8:
            raise ArgumentError(f'Found too many mappings for controller id \'{controller_section_name}\'. Maximum allowed is 8.')

        results = []
        for mapping in mappings:
            if len(mapping) != 2:
                raise ArgumentError(f'Invalid mapping for controller \'{controller_section_name}\'. Format is [ <name>, <button> ].')

            name: str = mapping[0]
            if len(name) > 19:
                raise ArgumentError(f'Invalid mapping name \'{name}\' for controller \'{controller_section_name}\'. Maximum length is 20 characters.')

            button = values.get(mapping[1], None)
            if button is None:
                raise ArgumentError(f'Invalid button name \'{mapping[1]}\' for controller \'{controller_section_name}\'.')

            results.append([name, button])

        return results
