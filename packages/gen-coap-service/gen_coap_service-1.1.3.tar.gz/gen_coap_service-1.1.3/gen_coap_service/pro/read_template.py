# -*- coding: UTF-8 -*-

'''
Module
    read_template.py
Copyright
    Copyright (C) 2020 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    gen_coap_service is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    gen_coap_service is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class ReadTemplate with attribute(s) and method(s).
    Reads a template.
'''

import sys
from typing import List

try:
    from ats_utilities.config_io.file_check import FileCheck
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/gen_coap_service'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_coap_service/blob/dev/LICENSE'
__version__ = '1.1.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReadTemplate(FileCheck):
    '''
        Defines class ReadTemplate with attribute(s) and method(s).
        Reads a template.

        It Definess:

            :attributes:
                | _GEN_VERBOSE - Console text indicator for process-phase.
            :methods:
                | __init__ - Initials ReadTemplate constructor.
                | read - Reads a template.
    '''

    _GEN_VERBOSE: str = 'GEN_AUTOCONF::PRO::READ_TEMPLATE'

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials ReadTemplate constructor.

            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        super().__init__(verbose)
        verbose_message(verbose, [f'{self._GEN_VERBOSE.lower()} init reader'])

    def read(
        self, template: str | None, verbose: bool = False
    ) -> str | None:
        '''
            Reads a template.

            :param template: Template file name | None
            :type template: <str> | <NoneType>
            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :return: Template content | None
            :rtype: <str> | <NoneType>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        error_msg, error_id = self.check_params([('str:template', template)])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(template):
            raise ATSValueError('missing template')
        self.check_path(template, verbose)
        self.check_mode('r', verbose)
        self.check_format(template, 'template', verbose)
        template_content: str | None = None
        if self.is_file_ok():
            with open(template, 'r', encoding='utf-8') as file_template:
                template_content = file_template.read()
        return template_content
