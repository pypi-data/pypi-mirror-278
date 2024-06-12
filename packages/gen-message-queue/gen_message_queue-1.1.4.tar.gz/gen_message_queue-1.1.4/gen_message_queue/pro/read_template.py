# -*- coding: UTF-8 -*-

'''
Module
    read_template.py
Copyright
    Copyright (C) 2018 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    gen_message_queue is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    gen_message_queue is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class ReadTemplate with attribute(s) and method(s).
    Creates an API for reading a LKM template.
'''

import sys
from typing import Any, List, Dict
from os.path import dirname, realpath

try:
    from ats_utilities.config_io.file_check import FileCheck
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/gen_message_queue'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_message_queue/blob/dev/LICENSE'
__version__ = '1.1.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReadTemplate(FileCheck):
    '''
        Defines class ReadTemplate with attribute(s) and method(s).
        Creates an API for reading a LKM template.

        It defines:

            :attributes:
                | _GEN_VERBOSE - Console text indicator for process-phase.
                | _TEMPLATE_DIR - Prefix path to templates.
            :methods:
                | __init__ - Initials ReadTemplate constructor.
                | read - Reads a template.
    '''

    _GEN_VERBOSE: str = 'GEN_MESSAGE_QUEUE::PRO::READ_TEMPLATE'
    _TEMPLATE_DIR: str = '/../conf/template/'

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials ReadTemplate constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        super().__init__(verbose)
        verbose_message(verbose, [f'{self._GEN_VERBOSE.lower()} init reader'])

    def read(
        self,
        config: Dict[Any, Any],
        pro_name: str | None,
        pro_type: str | None,
        verbose: bool = False
    ) -> Dict[str, str]:
        '''
            Reads a template.

            :param config: LKM configuration
            :type config: <Dict[Any, Any]>
            :param pro_name: LKM name | None
            :type pro_name: <str> | <NoneType>
            :param pro_type: LKM type | None
            :type pro_type: <str> | <NoneType>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: Loaded templates
            :rtype: <Dict[str, str]>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        error_msg, error_id = self.check_params([
            ('dict:config', config),
            ('str:pro_name', pro_name),
            ('str:pro_type', pro_type)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(config):
            raise ATSValueError('missing project templates')
        if not bool(pro_name):
            raise ATSValueError('missing project name')
        if not bool(pro_type):
            raise ATSValueError('missing project type')
        current_dir: str = dirname(realpath(__file__))
        pro_structure: str = f'{current_dir}{self._TEMPLATE_DIR}'
        template_dir: str = f'{pro_structure}{pro_type}/'
        template_content: Dict[str, str] = {}
        index: int = -1
        if pro_type in config['modules'][0]:
            index = 0
        elif pro_type in config['modules'][1]:
            index = 1
        else:
            return template_content
        modules: List[str] = config['modules'][index][pro_type]
        templates: List[str] = config['templates'][index][pro_type]
        for module, template in zip(modules, templates):
            template_file: str = f'{template_dir}{template}'
            with open(template_file, 'r', encoding='utf-8') as module_file:
                template_content[module] = module_file.read()
        verbose_message(
            verbose, [f'{self._GEN_VERBOSE.lower()} {template_content}']
        )
        return template_content
