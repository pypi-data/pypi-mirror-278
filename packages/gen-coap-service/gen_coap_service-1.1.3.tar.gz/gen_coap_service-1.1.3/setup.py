#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Module
    setup.py
Copyright
    Copyright (C) 2020 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    gen_coap_service is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    gen_coap_service is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines setup for tool gen_coap_service.
'''

from __future__ import print_function
from typing import List
from os.path import abspath, dirname, join
from setuptools import setup

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/gen_coap_service'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_coap_service/blob/dev/LICENSE'
__version__ = '1.1.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

TOOL_DIR: str = 'gen_coap_service/'
CONF: str = 'conf'
TEMPLATE: str = 'conf/template'
LOG: str = 'log'
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
    name='gen_coap_service',
    version='1.1.3',
    description='Generating CoAP Modules',
    author='Vladimir Roncevic',
    author_email='elektron.ronca@gmail.com',
    url='https://vroncevic.github.io/gen_coap_service',
    license='GPL 2020 - 2024 Free software to use and distributed it.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Unix, Linux, Development, CoAP, Modules',
    platforms='POSIX',
    classifiers=PYP_CLASSIFIERS,
    packages=['gen_coap_service', 'gen_coap_service.pro'],
    install_requires=['ats-utilities'],
    package_data={
        'gen_coap_service': [
            'py.typed',
            f'{CONF}/gen_coap_service.logo',
            f'{CONF}/gen_coap_service.cfg',
            f'{CONF}/gen_coap_service_util.cfg',
            f'{CONF}/project.yaml',
            f'{TEMPLATE}/template_coapthon.yaml',
            f'{TEMPLATE}/template_libcoap.yaml',
            f'{TEMPLATE}/template_node_coap.yaml',
            f'{TEMPLATE}/coapthon/basic_resources.template',
            f'{TEMPLATE}/coapthon/coap_client.template',
            f'{TEMPLATE}/coapthon/coap_server.template',
            f'{TEMPLATE}/coapthon/logging.template',
            f'{TEMPLATE}/libcoap/coap_client/build/editorconfig.template',
            f'{TEMPLATE}/libcoap/coap_client/src/client_api.template',
            f'{TEMPLATE}/libcoap/coap_client/src/main.template',
            f'{TEMPLATE}/libcoap/coap_client/src/Makefile.template',
            f'{TEMPLATE}/libcoap/coap_client/src/print_error.template',
            f'{TEMPLATE}/libcoap/coap_client/src/print_success.template',
            f'{TEMPLATE}/libcoap/coap_client/src/print_usage.template',
            f'{TEMPLATE}/libcoap/coap_client/src/print_verbose.template',
            f'{TEMPLATE}/libcoap/coap_client/src/process_options.template',
            f'{TEMPLATE}/libcoap/coap_client/src/time_handler.template',
            f'{TEMPLATE}/libcoap/coap_client/autogen.template',
            f'{TEMPLATE}/libcoap/coap_client/configure.template',
            f'{TEMPLATE}/libcoap/coap_client/Makefile.template',
            f'{TEMPLATE}/libcoap/coap_client/README.template',
            f'{TEMPLATE}/libcoap/coap_server/build/editorconfig.template',
            f'{TEMPLATE}/libcoap/coap_server/src/get_date.template',
            f'{TEMPLATE}/libcoap/coap_server/src/get_full.template',
            f'{TEMPLATE}/libcoap/coap_server/src/get_time.template',
            f'{TEMPLATE}/libcoap/coap_server/src/main.template',
            f'{TEMPLATE}/libcoap/coap_server/src/Makefile.template',
            f'{TEMPLATE}/libcoap/coap_server/src/server_api.template',
            f'{TEMPLATE}/libcoap/coap_server/src/time_handler.template',
            f'{TEMPLATE}/libcoap/coap_server/autogen.template',
            f'{TEMPLATE}/libcoap/coap_server/configure.template',
            f'{TEMPLATE}/libcoap/coap_server/Makefile.template',
            f'{TEMPLATE}/libcoap/coap_server/README.template',
            f'{TEMPLATE}/node_coap/client.template',
            f'{TEMPLATE}/node_coap/server.template',
            f'{LOG}/gen_coap_service.log'
        ]
    },
    data_files=[(
        '/usr/local/bin/', [
            f'{TOOL_DIR}run/gen_coap_service_run.py'
        ]
    )]
)
