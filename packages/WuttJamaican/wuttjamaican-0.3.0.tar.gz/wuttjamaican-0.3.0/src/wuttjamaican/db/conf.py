# -*- coding: utf-8; -*-
################################################################################
#
#  WuttJamaican -- Base package for Wutta Framework
#  Copyright © 2023 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
WuttJamaican -  database configuration
"""

from collections import OrderedDict

import sqlalchemy as sa

from wuttjamaican.util import parse_list


def get_engines(config, prefix):
    """
    Construct and return all database engines defined for a given
    config prefix.

    For instance if you have a config file with:

    .. code-block:: ini

       [wutta.db]
       keys = default, host
       default.url = sqlite:///tmp/default.sqlite
       host.url = sqlite:///tmp/host.sqlite

    And then you call this function to get those DB engines::

       get_engines(config, 'wutta.db')

    The result of that will be like::

       {'default': Engine(bind='sqlite:///tmp/default.sqlite'),
        'host': Engine(bind='sqlite:///tmp/host.sqlite')}

    :param config: App config object.

    :param prefix: Prefix for the config "section" which contains DB
       connection info.

    :returns: A dictionary of SQLAlchemy engines, with keys matching
       those found in config.
    """
    app = config.get_app()

    keys = config.get(f'{prefix}.keys', usedb=False)
    if keys:
        keys = parse_list(keys)
    else:
        keys = ['default']

    engines = OrderedDict()
    cfg = config.get_dict(prefix)
    for key in keys:
        key = key.strip()
        try:
            engines[key] = app.make_engine_from_config(cfg, prefix=f'{key}.')
        except KeyError:
            if key == 'default':
                try:
                    engines[key] = app.make_engine_from_config(cfg, prefix='sqlalchemy.')
                except KeyError:
                    pass
    return engines


def get_setting(session, name):
    """
    Get a setting value from the DB.

    Note that this assumes (for now?) the DB contains a table named
    ``setting`` with ``(name, value)`` columns.

    :param session: App DB session.

    :param name: Name of the setting to get.

    :returns: Setting value as string, or ``None``.
    """
    sql = sa.text("select value from setting where name = :name")
    return session.execute(sql, params={'name': name}).scalar()
