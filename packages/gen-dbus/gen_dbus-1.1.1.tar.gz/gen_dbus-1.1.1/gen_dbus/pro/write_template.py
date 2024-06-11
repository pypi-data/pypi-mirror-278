# -*- coding: UTF-8 -*-

'''
Module
    write_template.py
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
    Defines class WriteTemplate with attribute(s) and method(s).
    Creates an API for writing templates.
'''

import sys
from typing import List, Dict, Tuple
from os import getcwd, chmod, mkdir
from datetime import date
from string import Template

try:
    from ats_utilities.config_io.file_check import FileCheck
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.error import error_message
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


class WriteTemplate(FileCheck):
    '''
        Defines class WriteTemplate with attribute(s) and method(s).
        Creates an API for writing templates.

        It defines:

            :attributes:
                | _GEN_VERBOSE - Console text indicator for process-phase.
            :methods:
                | __init__ - Initials WriteTemplate constructor.
                | write - Writes a template files.
    '''

    _GEN_VERBOSE = 'GEN_DBUS::PRO::WRITE_TEMPLATE'

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials WriteTemplate constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        super().__init__(verbose)
        verbose_message(verbose, [f'{self._GEN_VERBOSE} init writer'])

    def is_empty_substructure(
        self, pro_setup: List[Tuple[Dict[str, str], Dict[str, str]]]
    ) -> bool:
        '''
            Check empty substructure.

            :param pro_setup: Project templates
            :type pro_setup: <List[Tuple[Dict[str, str], Dict[str, str]]]>
            :return: True (detect empty section) | False
            :rtype: <bool>
            :exception: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        error_msg, error_id = self.check_params([
            ('list:pro_setup', pro_setup)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pro_setup):
            raise ATSValueError('missing project configuration')
        for tpl in pro_setup:
            if not tpl or any(not d for d in tpl):
                return True
        return False

    def write(
        self,
        pro_setup: List[Tuple[Dict[str, str], Dict[str, str]]],
        pro_name: str | None,
        pro_type: str | None,
        verbose: bool = False
    ) -> bool:
        '''
            Writes a template files.

            :param pro_setup: Project templates
            :type pro_setup: <List[Tuple[Dict[str, str], Dict[str, str]]]>
            :param pro_name: Project name | None
            :type pro_name: <str> | <NoneType>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exception: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        error_msg, error_id = self.check_params([
            ('list:pro_setup', pro_setup),
            ('str:pro_name', pro_name),
            ('str:pro_type', pro_type)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pro_setup):
            raise ATSValueError('missing project configuration')
        if self.is_empty_substructure(pro_setup):
            error_message([f'{self._GEN_VERBOSE} empty substructure'])
            return False
        if not bool(pro_name):
            raise ATSValueError('missing project name')
        if not bool(pro_type):
            raise ATSValueError('missing project type')
        verbose_message(verbose, [f'{self._GEN_VERBOSE} write', pro_name])
        mkdir(f'{pro_name}/')
        mkdir(f'{pro_name}/dbus_client/')
        mkdir(f'{pro_name}/dbus_client/src/')
        mkdir(f'{pro_name}/dbus_client/po/')
        mkdir(f'{pro_name}/dbus_server/')
        mkdir(f'{pro_name}/dbus_server/src/')
        mkdir(f'{pro_name}/dbus_server/po/')
        package: Dict[str, str] = {
            'PRO': f'{pro_name}', 'YEAR': f'{date.today().year}'
        }
        work_dir: str = getcwd()
        for entity in pro_setup:
            client: Dict[str, str] = entity[0]
            server: Dict[str, str] = entity[1]
            for key, value in client.items():
                if all([bool(value), bool(key)]):
                    template = Template(value)
                    if not bool(template):
                        return False
                else:
                    return False
                module: str = f'{work_dir}/{pro_name}/dbus_client/{key}'
                with open(module, 'w', encoding='utf-8') as module_file:
                    if not bool(module_file):
                        return False
                    module_file.write(template.substitute(package))
                    chmod(module, 0o644)
            for key, value in server.items():
                if any([not bool(value), not bool(key)]):
                    return False
                template = Template(value)
                if not bool(template):
                    return False
                module: str = f'{work_dir}/{pro_name}/dbus_server/{key}'
                with open(module, 'w', encoding='utf-8') as module_file:
                    if not bool(module_file):
                        return False
                    module_file.write(template.substitute(package))
                    chmod(module, 0o644)
        return True
