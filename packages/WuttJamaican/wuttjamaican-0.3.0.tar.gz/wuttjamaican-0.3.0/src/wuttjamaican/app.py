# -*- coding: utf-8; -*-
################################################################################
#
#  WuttJamaican -- Base package for Wutta Framework
#  Copyright © 2023-2024 Lance Edgar
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
WuttJamaican - app handler
"""

import os
import warnings

from wuttjamaican.util import load_entry_points, load_object, parse_bool


class AppHandler:
    """
    Base class and default implementation for top-level :term:`app
    handler`.

    aka. "the handler to handle all handlers"

    aka. "one handler to bind them all"

    For more info see :doc:`/narr/handlers/app`.

    There is normally no need to create one of these yourself; rather
    you should call :meth:`~wuttjamaican.conf.WuttaConfig.get_app()`
    on the :term:`config object` if you need the app handler.

    :param config: Config object for the app.  This should be an
       instance of :class:`~wuttjamaican.conf.WuttaConfig`.

    .. attribute:: providers

       Dictionary of :class:`AppProvider` instances, as returned by
       :meth:`get_all_providers()`.
    """

    def __init__(self, config):
        self.config = config
        self.handlers = {}

    @property
    def appname(self):
        """
        The :term:`app name` for the current app.  This is just an
        alias for :attr:`wuttjamaican.conf.WuttaConfig.appname`.

        Note that this ``appname`` does not necessariy reflect what
        you think of as the name of your (e.g. custom) app.  It is
        more fundamental than that; your Python package naming and the
        :term:`app title` are free to use a different name as their
        basis.
        """
        return self.config.appname

    def __getattr__(self, name):
        """
        Custom attribute getter, called when the app handler does not
        already have an attribute named with ``name``.

        This will delegate to the set of :term:`app providers<app
        provider>`; the first provider with an appropriately-named
        attribute wins, and that value is returned.

        :returns: The first value found among the set of app
           providers.
        """

        if name == 'providers':
            self.providers = self.get_all_providers()
            return self.providers

        # if 'providers' not in self.__dict__:
        #     self.__dict__['providers'] = self.get_all_providers()

        for provider in self.providers.values():
            if hasattr(provider, name):
                return getattr(provider, name)

        raise AttributeError(f"attr not found: {name}")

    def get_all_providers(self):
        """
        Load and return all registered providers.

        Note that you do not need to call this directly; instead just
        use :attr:`providers`.

        :returns: Dictionary keyed by entry point name; values are
           :class:`AppProvider` *instances*.
        """
        providers = load_entry_points(f'{self.appname}.providers')
        for key in list(providers):
            providers[key] = providers[key](self.config)
        return providers

    def make_appdir(self, path, subfolders=None, **kwargs):
        """
        Establish an :term:`app dir` at the given path.

        Default logic only creates a few subfolders, meant to help
        steer the admin toward a convention for sake of where to put
        things.  But custom app handlers are free to do whatever.

        :param path: Path to the desired app dir.  If the path does
           not yet exist then it will be created.  But regardless it
           should be "refreshed" (e.g. missing subfolders created)
           when this method is called.

        :param subfolders: Optional list of subfolder names to create
           within the app dir.  If not specified, defaults will be:
           ``['data', 'log', 'work']``.
        """
        appdir = path
        if not os.path.exists(appdir):
            os.makedirs(appdir)

        if not subfolders:
            subfolders = ['data', 'log', 'work']

        for name in subfolders:
            path = os.path.join(appdir, name)
            if not os.path.exists(path):
                os.mkdir(path)

    def make_engine_from_config(
            self,
            config_dict,
            prefix='sqlalchemy.',
            **kwargs):
        """
        Construct a new DB engine from configuration dict.

        This is a wrapper around upstream
        :func:`sqlalchemy:sqlalchemy.engine_from_config()`.  For even
        broader context of the SQLAlchemy
        :class:`~sqlalchemy:sqlalchemy.engine.Engine` and their
        configuration, see :doc:`sqlalchemy:core/engines`.

        The purpose of the customization is to allow certain
        attributes of the engine to be driven by config, whereas the
        upstream function is more limited in that regard.  The
        following in particular:

        * ``poolclass``
        * ``pool_pre_ping``

        If these options are present in the configuration dict, they
        will be coerced to appropriate Python equivalents and then
        passed as kwargs to the upstream function.

        An example config file leveraging this feature:

        .. code-block:: ini

           [wutta.db]
           default.url = sqlite:///tmp/default.sqlite
           default.poolclass = sqlalchemy.pool:NullPool
           default.pool_pre_ping = true

        Note that if present, the ``poolclass`` value must be a "spec"
        string, as required by
        :func:`~wuttjamaican.util.load_object()`.
        """
        import sqlalchemy as sa

        config_dict = dict(config_dict)

        # convert 'poolclass' arg to actual class
        key = f'{prefix}poolclass'
        if key in config_dict and 'poolclass' not in kwargs:
            kwargs['poolclass'] = load_object(config_dict.pop(key))

        # convert 'pool_pre_ping' arg to boolean
        key = f'{prefix}pool_pre_ping'
        if key in config_dict and 'pool_pre_ping' not in kwargs:
            kwargs['pool_pre_ping'] = parse_bool(config_dict.pop(key))

        engine = sa.engine_from_config(config_dict, prefix, **kwargs)

        return engine

    def make_session(self, **kwargs):
        """
        Creates a new SQLAlchemy session for the app DB.  By default
        this will create a new :class:`~wuttjamaican.db.sess.Session`
        instance.

        :returns: SQLAlchemy session for the app DB.
        """
        from .db import Session

        return Session(**kwargs)

    def short_session(self, **kwargs):
        """
        Returns a context manager for a short-lived database session.

        This is a convenience wrapper around
        :class:`~wuttjamaican.db.sess.short_session`.

        If caller does not specify ``factory`` nor ``config`` params,
        this method will provide a default factory in the form of
        :meth:`make_session`.
        """
        from .db import short_session

        if 'factory' not in kwargs and 'config' not in kwargs:
            kwargs['factory'] = self.make_session

        return short_session(**kwargs)

    def get_setting(self, session, name, **kwargs):
        """
        Get a setting value from the DB.

        This does *not* consult the config object directly to
        determine the setting value; it always queries the DB.

        Default implementation is just a convenience wrapper around
        :func:`~wuttjamaican.db.conf.get_setting()`.

        :param session: App DB session.

        :param name: Name of the setting to get.

        :returns: Setting value as string, or ``None``.
        """
        from .db import get_setting

        return get_setting(session, name)


class AppProvider:
    """
    Base class for :term:`app providers<app provider>`.

    These can add arbitrary extra functionality to the main :term:`app
    handler`.  See also :doc:`/narr/providers/app`.

    :param config: Config object for the app.  This should be an
       instance of :class:`~wuttjamaican.conf.WuttaConfig`.

    Instances have the following attributes:

    .. attribute:: config

       Reference to the config object.

    .. attribute:: app

       Reference to the parent app handler.
    """

    def __init__(self, config):

        if isinstance(config, AppHandler):
            warnings.warn("passing app handler to app provider is deprecated; "
                          "must pass config object instead",
                          DeprecationWarning, stacklevel=2)
            config = config.config

        self.config = config
        self.app = config.get_app()


class GenericHandler:
    """
    Generic base class for handlers.

    When the :term:`app` defines a new *type* of :term:`handler` it
    may subclass this when defining the handler base class.

    :param config: Config object for the app.  This should be an
       instance of :class:`~wuttjamaican.conf.WuttaConfig`.
    """

    def __init__(self, config, **kwargs):
        self.config = config
        self.app = self.config.get_app()
