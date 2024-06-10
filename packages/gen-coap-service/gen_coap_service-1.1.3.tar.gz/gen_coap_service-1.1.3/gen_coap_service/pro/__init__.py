# -*- coding: UTF-8 -*-

'''
Module
    __init__.py
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
    Defines class GenCoAP with attribute(s) and method(s).
    Generates project_structure by templates and parameters.
'''

import sys
from typing import Any, List, Dict
from os import makedirs
from os.path import dirname, realpath, exists

try:
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.config_io.yaml.yaml2object import Yaml2Object
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
    from ats_utilities.pro_config import ProConfig
    from ats_utilities.pro_config.pro_name import ProName
    from ats_utilities.config_io.file_check import FileCheck
    from gen_coap_service.pro.read_template import ReadTemplate
    from gen_coap_service.pro.write_template import WriteTemplate
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


class GenCoAP(FileCheck, ProConfig, ProName):
    '''
        Defines class GenCoAP with attribute(s) and method(s).
        Generates project_structure by template and parameters.

        It Definess:

            :attributes:
                | _GEN_VERBOSE - Console text indicator for process-phase.
                | _PRO_STRUCTURE - Project setup (templates, modules).
                | _reader - Reader API.
                | _writer - Writer API.
            :methods:
                | __init__ - Initials GenCoAP constructor.
                | get_reader - Gets template reader.
                | get_writer - Gets template writer.
                | gen_project - Generates autotools project skeleton.
    '''

    _GEN_VERBOSE: str = 'GEN_COAP_SERVICE::PRO::GEN_PRO'
    _PRO_STRUCTURE: str = '/../conf/project.yaml'

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials GenCoAP constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        FileCheck.__init__(self, verbose)
        ProConfig.__init__(self, verbose)
        ProName.__init__(self, verbose)
        verbose_message(
            verbose, [f'{self._GEN_VERBOSE.lower()} init generator']
        )
        self._reader: ReadTemplate | None = ReadTemplate(verbose)
        self._writer: WriteTemplate | None = WriteTemplate(verbose)
        current_dir: str = dirname(realpath(__file__))
        pro_structure: str = f'{current_dir}{self._PRO_STRUCTURE}'
        self.check_path(pro_structure, verbose)
        self.check_mode('r', verbose)
        self.check_format(pro_structure, 'yaml', verbose)
        if self.is_file_ok():
            yml2obj = Yaml2Object(pro_structure)
            self.config = yml2obj.read_configuration()

    def get_reader(self) -> ReadTemplate | None:
        '''
            Gets template reader.

            :return: Template reader object | None
            :rtype: <ReadTemplate> | <NoneType>
            :exceptions: None
        '''
        return self._reader

    def get_writer(self) -> WriteTemplate | None:
        '''
            Gets template writer.

            :return: Template writer object | none
            :rtype: <WriteTemplate> | <NoneType
            :exceptions: None
        '''
        return self._writer

    def project_setup(
        self,
        pro_name: str | None,
        pro_type: str | None,
        verbose: bool = False
    ) -> bool:
        '''
            Generates autotools project skeleton.

            :param pro_name: Project name | None
            :type pro_name: <str> | <NoneType>
            :param pro_type: Project type | None
            :type pro_type: <str> | <NoneType>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        error_msg, error_id = self.check_params([
            ('str:pro_name', pro_name), ('str:pro_type', pro_type)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pro_name):
            raise ATSValueError('missing project name')
        if not bool(pro_type):
            raise ATSValueError('missing project type')
        if not bool(self.config):
            raise ATSValueError('missing project configuration')
        else:
            if pro_type not in self.config['types']:
                raise ATSValueError('not supported project type')
        verbose_message(
            verbose, [
                f'{self._GEN_VERBOSE.lower()} generate',
                pro_type, 'project', pro_name
            ]
        )
        current_dir: str = dirname(realpath(__file__))
        template_dir: str = f'{current_dir}/../conf/template/'
        yml2obj: Yaml2Object | None = Yaml2Object(
            f'{template_dir}template_{pro_type}.yaml', verbose
        )
        all_stat: List[bool] = []
        templates: List[str] = []
        if bool(yml2obj) and bool(self._reader) and bool(self._writer):
            pro_cfg: Dict[Any, Any] = yml2obj.read_configuration()
            pro_data: Dict[Any, Any] = {}
            modules: List[str] = []
            if bool(pro_cfg):
                templates: List[str] = pro_cfg['templates']
                modules: List[str] = pro_cfg['modules']
                pro_data['name'] = pro_name
                pro_data['type'] = pro_type
                if pro_type == 'libcoap':
                    directories: List[str] = [
                        'coap_client',
                        'coap_server',
                        'coap_client/build',
                        'coap_client/src',
                        'coap_server/build',
                        'coap_server/src'
                    ]
                    for directory in directories:
                        if not exists(directory):
                            makedirs(directory)
                for template, module in zip(templates, modules):
                    pro_data['template'] = self._reader.read(
                        f'{template_dir}{template}', verbose
                    )
                    pro_data['module'] = module
                    all_stat.append(self._writer.write(pro_data, verbose))
        return all([
            bool(all_stat), all(all_stat), len(templates) == len(all_stat)
        ])
