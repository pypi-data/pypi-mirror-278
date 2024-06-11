# -*- coding: UTF-8 -*-

'''
Module
    read_template.py
Copyright
    Copyright (C) 2021 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    gen_dbus is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    gen_dbus is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class ReadTemplate with attribute(s) and method(s).
    Creates an API for reading a template files.
'''

import sys
from typing import Any, List, Dict, Tuple
from os.path import dirname, realpath

try:
    from ats_utilities.config_io.file_check import FileCheck
    from ats_utilities.pro_config import ProConfig
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/gen_dbus'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_dbus/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReadTemplate(FileCheck):
    '''
        Defines class ReadTemplate with attribute(s) and method(s).
        Creates an API for reading a template files.

        It defines:

            :attributes:
                | _GEN_VERBOSE - Console text indicator for process-phase.
                | _TEMPLATE_DIR - Template dir path.
                | _POSIX_C_TYPE - Posix C project type id.
                | _POSIX_CXX_TYPE - Posix C++ project type id.
                | _POSIX_PY_TYPE - Posix Python project type id.
                | _NOT_SUPPORTED - Not supported project type id.
                | _DBUS_CLIENT - DBUS client section name.
                | _DBUS_SERVER - DBUS server section name.
            :methods:
                | __init__ - Initials ReadTemplate constructor.
                | _get_artifacts - Gets artifacts from project configuration.
                | read - Reads a templates.
    '''

    _GEN_VERBOSE: str = 'GEN_DBUS::PRO::READ_TEMPLATE'
    _TEMPLATE_DIR: str = '/../conf/template/'
    _POSIX_C_TYPE: int = 0
    _POSIX_CXX_TYPE: int = 1
    _POSIX_PY_TYPE: int = 2
    _NOT_SUPPORTED: int = -1
    _DBUS_CLIENT: str = 'dbus_client'
    _DBUS_SERVER: str = 'dbus_server'

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials ReadTemplate constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        super().__init__(verbose)
        verbose_message(verbose, [f'{self._GEN_VERBOSE} init reader'])

    def _get_template_type_id(
        self, pro_type: str | None, pro_setup: Dict[Any, Any] | None
    ) -> int:
        '''
            Gets project type id.

            :param pro_type: Project type
            :type pro_type: <str>
            :param pro_setup: Project configuration
            :type pro_setup: <dict>
            :return: Project type ID (0 | 1 | 2 | -1)
            :rtype: <int>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        error_msg, error_id = self.check_params([
            ('dict:pro_setup', pro_setup), ('str:pro_type', pro_type)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pro_setup):
            raise ATSValueError('missing project configuration')
        if not bool(pro_type):
            raise ATSValueError('missing project type')
        if pro_type in pro_setup[ProConfig.TEMPLATES][self._POSIX_C_TYPE]:
            return self._POSIX_C_TYPE
        if pro_type in pro_setup[ProConfig.TEMPLATES][self._POSIX_CXX_TYPE]:
            return self._POSIX_CXX_TYPE
        if pro_type in pro_setup[ProConfig.TEMPLATES][self._POSIX_PY_TYPE]:
            return self._POSIX_PY_TYPE
        return self._NOT_SUPPORTED

    def _get_artifacts(
        self,
        pro_type: str | None,
        pro_setup: Dict[Any, Any] | None,
        pro_artifact_type: str | None
    ) -> Tuple[List[str], List[str]]:
        '''
            Gets artifacts from project configuration.

            :param pro_type: Project type
            :type pro_type: <str>
            :param pro_setup: Project configuration
            :type pro_setup: <dict>
            :return: Project modules (client and server)
            :rtype: <Tuple[List[str], List[str]]>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        error_msg, error_id = self.check_params([
            ('dict:pro_setup', pro_setup),
            ('str:pro_type', pro_type),
            ('str:pro_artifact_type', pro_artifact_type)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pro_setup):
            raise ATSValueError('missing project configuration')
        if not bool(pro_type):
            raise ATSValueError('missing project type')
        if not bool(pro_artifact_type):
            raise ATSValueError('missing project artifact type')
        if pro_artifact_type not in [ProConfig.TEMPLATES, ProConfig.MODULES]:
            raise ATSValueError('invalid project artifact type')
        artifacts: List[str] = []
        client_artifacts: List[str] = []
        server_artifacts: List[str] = []
        pro_type_index: int = self._get_template_type_id(pro_type, pro_setup)
        if pro_type_index == self._NOT_SUPPORTED:
            return (client_artifacts, server_artifacts)
        artifacts = pro_setup[pro_artifact_type][pro_type_index][pro_type]
        for artifact in artifacts:
            if isinstance(artifact, dict):
                if self._DBUS_CLIENT in artifact:
                    client_artifacts.extend(
                        artifact[self._DBUS_CLIENT]  # type: ignore
                    )
                if self._DBUS_SERVER in artifact:
                    server_artifacts.extend(
                        artifact[self._DBUS_SERVER]  # type: ignore
                    )
        return (client_artifacts, server_artifacts)

    def read(
        self,
        pro_setup: Dict[Any, Any] | None,
        pro_type: str | None,
        verbose: bool = False
    ) -> List[Tuple[Dict[str, str], Dict[str, str]]]:
        '''
            Reads a templates.

            :param pro_setup: Project templates
            :type pro_setup: <Dict[Any, Any]>
            :param pro_type: Project type | None
            :type pro_type: <str> | <NoneType>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: Template files for project setup
            :rtype: <List[Tuple[Dict[str, str], Dict[str, str]]]>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        error_msg, error_id = self.check_params([
            ('dict:pro_setup', pro_setup), ('str:pro_type', pro_type)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pro_setup):
            raise ATSValueError('missing templates')
        if not bool(pro_type):
            raise ATSValueError('missing project type')
        pro_content: List[Tuple[Dict[str, str], Dict[str, str]]] = []
        client_templates: List[str] = []
        server_templates: List[str] = []
        client_modules: List[str] = []
        server_modules: List[str] = []
        client_templates, server_templates = self._get_artifacts(
            pro_type, pro_setup, ProConfig.TEMPLATES
        )
        client_modules, server_modules = self._get_artifacts(
            pro_type, pro_setup, ProConfig.MODULES
        )
        for key_cl_module, cl_module, key_sr_module, sr_module in zip(
            client_modules, client_templates, server_modules, server_templates
        ):
            client_content: str = ''
            server_content: str = ''
            current_dir: str = dirname(realpath(__file__))
            template_dir: str = f'{current_dir}{self._TEMPLATE_DIR}{pro_type}'
            cl_module_path: str = f'{template_dir}/dbus_client/{cl_module}'
            self.check_path(cl_module_path, verbose)
            self.check_mode('r', verbose)
            self.check_format(cl_module_path, 'template', verbose)
            if self.is_file_ok():
                with open(cl_module_path, 'r', encoding='utf-8') as client_io:
                    client_content = client_io.read()
            sr_module_path: str = f'{template_dir}/dbus_server/{sr_module}'
            self.check_path(sr_module_path, verbose)
            self.check_mode('r', verbose)
            self.check_format(sr_module_path, 'template', verbose)
            if self.is_file_ok():
                with open(sr_module_path, 'r', encoding='utf-8') as server_io:
                    server_content = server_io.read()
            if bool(client_content) or bool(server_content):
                pro_content.append((
                    {key_cl_module: client_content},
                    {key_sr_module: server_content}
                ))
        return pro_content
