#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Module
    setup.py
Copyright
    Copyright (C) 2021 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    gen_dbus is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    gen_dbus is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Define setup for tool gen_dbus.
'''

from __future__ import print_function
from typing import List
from os.path import abspath, dirname, join
from setuptools import setup

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/gen_dbus'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_dbus/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

TOOL_DIR: str = 'gen_dbus/'
CONF: str = 'conf'
TEMPLATE: str = 'conf/template'
LOG: str = 'log'
POSIX_C: str = 'template/posix_c'
POSIX_CC: str = 'template/posix_cxx'
POSIX_PY: str = 'template/posix_py'
THIS_DIR: str = abspath(dirname(__file__))
long_description: str | None = None
with open(join(THIS_DIR, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()
PROGRAMMING_LANG: str = 'Programming Language :: Python ::'
VERSIONS: List[str] = ['3.10', '3.11']
SUPPORTED_PY_VERSIONS: List[str] = [
    f'{PROGRAMMING_LANG} {VERSION}' for VERSION in VERSIONS
]
LICENSE_PREFIX: str = 'License :: OSI Approved ::'
LICENSES: List[str] = [
    'GNU Lesser General Public License v2 (LGPLv2)',
    'GNU Lesser General Public License v2 or later (LGPLv2+)',
    'GNU Lesser General Public License v3 (LGPLv3)',
    'GNU Lesser General Public License v3 or later (LGPLv3+)',
    'GNU Library or Lesser General Public License (LGPL)'
]
APPROVED_LICENSES: List[str] = [
    f'{LICENSE_PREFIX} {LICENSE}' for LICENSE in LICENSES
]
PYP_CLASSIFIERS: List[str] = SUPPORTED_PY_VERSIONS + APPROVED_LICENSES
setup(
    name='gen_dbus',
    version='1.1.1',
    description='Generating DBus modules',
    author='Vladimir Roncevic',
    author_email='elektron.ronca@gmail.com',
    url='https://vroncevic.github.io/gen_dbus',
    license='GPL 2024 Free software to use and distributed it.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Unix, Linux, Development, DBus, Modules',
    platforms='POSIX',
    classifiers=PYP_CLASSIFIERS,
    packages=['gen_dbus', 'gen_dbus.pro'],
    install_requires=['ats-utilities'],
    package_data={
        'gen_dbus': [
            'py.typed',
            f'{CONF}/gen_dbus.logo',
            f'{CONF}/gen_dbus.cfg',
            f'{CONF}/gen_dbus_util.cfg',
            f'{CONF}/project.yaml',
            f'{POSIX_C}/dbus_client/AUTHORS.template',
            f'{POSIX_C}/dbus_client/COPYING.template',
            f'{POSIX_C}/dbus_client/ChangeLog.template',
            f'{POSIX_C}/dbus_client/Makefile.template',
            f'{POSIX_C}/dbus_client/NEWS.template',
            f'{POSIX_C}/dbus_client/README.template',
            f'{POSIX_C}/dbus_client/autogen.template',
            f'{POSIX_C}/dbus_client/configure.template',
            f'{POSIX_C}/dbus_client/src/Makefile.template',
            f'{POSIX_C}/dbus_client/src/main.template',
            f'{POSIX_C}/dbus_server/AUTHORS.template',
            f'{POSIX_C}/dbus_server/COPYING.template',
            f'{POSIX_C}/dbus_server/ChangeLog.template',
            f'{POSIX_C}/dbus_server/Makefile.template',
            f'{POSIX_C}/dbus_server/NEWS.template',
            f'{POSIX_C}/dbus_server/README.template',
            f'{POSIX_C}/dbus_server/autogen.template',
            f'{POSIX_C}/dbus_server/configure.template',
            f'{POSIX_C}/dbus_server/src/Makefile.template',
            f'{POSIX_C}/dbus_server/src/main.template',
            f'{POSIX_CC}/dbus_client/AUTHORS.template',
            f'{POSIX_CC}/dbus_client/COPYING.template',
            f'{POSIX_CC}/dbus_client/ChangeLog.template',
            f'{POSIX_CC}/dbus_client/Makefile.template',
            f'{POSIX_CC}/dbus_client/NEWS.template',
            f'{POSIX_CC}/dbus_client/README.template',
            f'{POSIX_CC}/dbus_client/autogen.template',
            f'{POSIX_CC}/dbus_client/configure.template',
            f'{POSIX_CC}/dbus_client/po/ChangeLog.template',
            f'{POSIX_CC}/dbus_client/po/LINGUAS.template',
            f'{POSIX_CC}/dbus_client/po/POTFILES.template',
            f'{POSIX_CC}/dbus_client/src/Makefile.template',
            f'{POSIX_CC}/dbus_client/src/main.template',
            f'{POSIX_CC}/dbus_server/AUTHORS.template',
            f'{POSIX_CC}/dbus_server/COPYING.template',
            f'{POSIX_CC}/dbus_server/ChangeLog.template',
            f'{POSIX_CC}/dbus_server/Makefile.template',
            f'{POSIX_CC}/dbus_server/NEWS.template',
            f'{POSIX_CC}/dbus_server/README.template',
            f'{POSIX_CC}/dbus_server/autogen.template',
            f'{POSIX_CC}/dbus_server/configure.template',
            f'{POSIX_CC}/dbus_server/po/ChangeLog.template',
            f'{POSIX_CC}/dbus_server/po/LINGUAS.template',
            f'{POSIX_CC}/dbus_server/po/POTFILES.template',
            f'{POSIX_CC}/dbus_server/src/Makefile.template',
            f'{POSIX_CC}/dbus_server/src/main.template',
            f'{POSIX_PY}/dbus_client/AUTHORS.template',
            f'{POSIX_PY}/dbus_client/COPYING.template',
            f'{POSIX_PY}/dbus_client/ChangeLog.template',
            f'{POSIX_PY}/dbus_client/Makefile.template',
            f'{POSIX_PY}/dbus_client/NEWS.template',
            f'{POSIX_PY}/dbus_client/README.template',
            f'{POSIX_PY}/dbus_client/autogen.template',
            f'{POSIX_PY}/dbus_client/configure.template',
            f'{POSIX_PY}/dbus_client/src/Makefile.template',
            f'{POSIX_PY}/dbus_client/src/dbus_client.template',
            f'{POSIX_PY}/dbus_server/AUTHORS.template',
            f'{POSIX_PY}/dbus_server/COPYING.template',
            f'{POSIX_PY}/dbus_server/ChangeLog.template',
            f'{POSIX_PY}/dbus_server/Makefile.template',
            f'{POSIX_PY}/dbus_server/NEWS.template',
            f'{POSIX_PY}/dbus_server/README.template',
            f'{POSIX_PY}/dbus_server/autogen.template',
            f'{POSIX_PY}/dbus_server/configure.template',
            f'{POSIX_PY}/dbus_server/src/Makefile.template',
            f'{POSIX_PY}/dbus_server/src/dbus_server.template',
            f'{LOG}/gen_dbus.log'
        ]
    },
    data_files=[(
        '/usr/local/bin/', [
            f'{TOOL_DIR}run/gen_dbus_run.py'
        ]
    )]
)
