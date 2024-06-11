# -*- coding: utf-8; -*-

import os
import shutil
import tempfile
import warnings
from unittest import TestCase
from unittest.mock import patch, MagicMock

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool

from wuttjamaican import app, db
from wuttjamaican.conf import WuttaConfig


class TestAppHandler(TestCase):

    def setUp(self):
        self.config = WuttaConfig(appname='wuttatest')
        self.app = app.AppHandler(self.config)
        self.config.app = self.app

    def test_init(self):
        self.assertIs(self.app.config, self.config)
        self.assertEqual(self.app.handlers, {})
        self.assertEqual(self.app.appname, 'wuttatest')

    def test_make_appdir(self):

        # appdir is created, and 3 subfolders added by default
        tempdir = tempfile.mkdtemp()
        appdir = os.path.join(tempdir, 'app')
        self.assertFalse(os.path.exists(appdir))
        self.app.make_appdir(appdir)
        self.assertTrue(os.path.exists(appdir))
        self.assertEqual(len(os.listdir(appdir)), 3)
        shutil.rmtree(tempdir)

        # subfolders still added if appdir already exists
        tempdir = tempfile.mkdtemp()
        self.assertTrue(os.path.exists(tempdir))
        self.assertEqual(len(os.listdir(tempdir)), 0)
        self.app.make_appdir(tempdir)
        self.assertEqual(len(os.listdir(tempdir)), 3)
        shutil.rmtree(tempdir)

    def test_make_engine_from_config_basic(self):
        engine = self.app.make_engine_from_config({
            'sqlalchemy.url': 'sqlite://',
        })
        self.assertIsInstance(engine, Engine)

    def test_make_engine_from_config_poolclass(self):

        engine = self.app.make_engine_from_config({
            'sqlalchemy.url': 'sqlite://',
        })
        self.assertNotIsInstance(engine.pool, NullPool)

        engine = self.app.make_engine_from_config({
            'sqlalchemy.url': 'sqlite://',
            'sqlalchemy.poolclass': 'sqlalchemy.pool:NullPool',
        })
        self.assertIsInstance(engine.pool, NullPool)

    def test_make_engine_from_config_pool_pre_ping(self):

        engine = self.app.make_engine_from_config({
            'sqlalchemy.url': 'sqlite://',
        })
        self.assertFalse(engine.pool._pre_ping)

        engine = self.app.make_engine_from_config({
            'sqlalchemy.url': 'sqlite://',
            'sqlalchemy.pool_pre_ping': 'true',
        })
        self.assertTrue(engine.pool._pre_ping)

    def test_make_session(self):
        session = self.app.make_session()
        self.assertIsInstance(session, db.Session.class_)

    def test_short_session(self):
        short_session = MagicMock()
        mockdb = MagicMock(short_session=short_session)

        with patch.dict('sys.modules', **{'wuttjamaican.db': mockdb}):

            with self.app.short_session(foo='bar') as s:
                short_session.assert_called_once_with(
                    foo='bar', factory=self.app.make_session)

    def test_get_setting(self):
        Session = orm.sessionmaker()
        engine = sa.create_engine('sqlite://')
        session = Session(bind=engine)
        session.execute(sa.text("""
        create table setting (
                name varchar(255) primary key,
                value text
        );
        """))
        session.commit()

        value = self.app.get_setting(session, 'foo')
        self.assertIsNone(value)

        session.execute(sa.text("insert into setting values ('foo', 'bar');"))
        value = self.app.get_setting(session, 'foo')
        self.assertEqual(value, 'bar')


class TestAppProvider(TestCase):

    def setUp(self):
        self.config = WuttaConfig(appname='wuttatest')
        self.app = app.AppHandler(self.config)
        self.config.app = self.app

    def test_constructor(self):

        # config object is expected
        provider = app.AppProvider(self.config)
        self.assertIs(provider.config, self.config)
        self.assertIs(provider.app, self.app)

        # but can pass app handler instead
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            provider = app.AppProvider(self.app)
        self.assertIs(provider.config, self.config)
        self.assertIs(provider.app, self.app)

    def test_get_all_providers(self):

        class FakeProvider(app.AppProvider):
            pass

        # nb. we specify *classes* here
        fake_providers = {'fake': FakeProvider}

        with patch('wuttjamaican.app.load_entry_points') as load_entry_points:
            load_entry_points.return_value = fake_providers

            # sanity check, we get *instances* back from this
            providers = self.app.get_all_providers()
            load_entry_points.assert_called_once_with('wuttatest.providers')
            self.assertEqual(len(providers), 1)
            self.assertIn('fake', providers)
            self.assertIsInstance(providers['fake'], FakeProvider)

    def test_hasattr(self):

        class FakeProvider(app.AppProvider):
            def fake_foo(self):
                pass

        self.app.providers = {'fake': FakeProvider(self.config)}

        self.assertTrue(hasattr(self.app, 'fake_foo'))
        self.assertFalse(hasattr(self.app, 'fake_method_does_not_exist'))

    def test_getattr(self):

        class FakeProvider(app.AppProvider):
            def fake_foo(self):
                return 42

        # nb. using instances here
        fake_providers = {'fake': FakeProvider(self.config)}

        with patch.object(self.app, 'get_all_providers') as get_all_providers:
            get_all_providers.return_value = fake_providers

            self.assertNotIn('providers', self.app.__dict__)
            self.assertIs(self.app.providers, fake_providers)
            get_all_providers.assert_called_once_with()

    def test_getattr_providers(self):

        # collection of providers is loaded on demand
        self.assertNotIn('providers', self.app.__dict__)
        self.assertIsNotNone(self.app.providers)

        # custom attr does not exist yet
        self.assertRaises(AttributeError, getattr, self.app, 'foo_value')

        # but provider can supply the attr
        self.app.providers['mytest'] = MagicMock(foo_value='bar')
        self.assertEqual(self.app.foo_value, 'bar')


class TestGenericHandler(TestCase):

    def setUp(self):
        self.config = WuttaConfig(appname='wuttatest')
        self.app = app.AppHandler(self.config)
        self.config.app = self.app

    def test_constructor(self):
        handler = app.GenericHandler(self.config)
        self.assertIs(handler.config, self.config)
        self.assertIs(handler.app, self.app)
