# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
CORE Office utility logic
"""

import json
import os
import subprocess

from rattail.files import resource_path


def get_fannie_config_value(config, name, fannie_config_path=None):
    """
    Retrieve a config value from `fannie/config.php`

    :param config: Rattail config object.

    :param name: Name of the config value to be returned.  This need
       not be prefixed with ``FANNIE_`` although it can be.

    :param fannie_config_path: Optional path to fannie config file.
       If not specified, it is will be determined via ``config``.

    :returns: Config value as Python object, e.g. a string or dict.
       This is believed to work okay but since the Fannie config file
       represents data with PHP code, which is then converted to JSON
       and finally to Python, some discrepancies may be possible.
    """
    if not name.startswith('FANNIE_'):
        name = f'FANNIE_{name}'

    if not fannie_config_path:
        is4c = config.require('corepos', 'srcdir')
        fannie_config_path = os.path.join(is4c, 'fannie', 'config.php')
    script = resource_path('rattail_corepos.corepos.office:scripts/parse-fannie-config.php')

    try:
        output = subprocess.check_output(['php', script,
                                          '--path', fannie_config_path,
                                          '--setting', name])
    except subprocess.CalledProcessError as error:
        output = error.output.decode('utf_8')
        if "file does not contain setting" in output:
            raise ValueError(output)
        raise

    return json.loads(output.decode('utf_8'))


def set_fannie_config_value(config, name, value, fannie_config_path=None):
    """
    Update a config value in `fannie/config.php`

    :param config: Rattail config object.

    :param name: Name of the config value to set.  This need not be
       prefixed with ``FANNIE_`` although it can be.

    :param value: Config value to set This must be provided as a
       JSON-compatible string.

    :param fannie_config_path: Optional path to fannie config file.
       If not specified, it is will be determined via ``config``.
    """
    if not name.startswith('FANNIE_'):
        name = f'FANNIE_{name}'

    if not fannie_config_path:
        is4c = config.require('corepos', 'srcdir')
        fannie_config_path = os.path.join(is4c, 'fannie', 'config.php')
    script = resource_path('rattail_corepos.corepos.office:scripts/update-fannie-config.php')

    output = subprocess.check_output(['php', script,
                                      '--path', fannie_config_path,
                                      '--name', name,
                                      '--value', json.dumps(value)])


def get_blueline_template(config):
    return get_fannie_config_value(config, 'BLUELINE_TEMPLATE')


def make_blueline(config, customer, template=None):
    if not template:
        template = get_blueline_template(config)

    blueline = template
    blueline = blueline.replace('{{ACCOUNTNO}}', str(customer.card_number))
    blueline = blueline.replace('{{ACCOUNTTYPE}}', customer.member_type.description if customer.member_type else '??')
    blueline = blueline.replace('{{FIRSTNAME}}', customer.first_name or '')
    blueline = blueline.replace('{{FIRSTINITIAL}}', customer.first_name[0] if customer.first_name else '')
    blueline = blueline.replace('{{LASTNAME}}', customer.last_name or '')
    blueline = blueline.replace('{{LASTINITIAL}}', customer.last_name[0] if customer.last_name else '')
    return blueline
