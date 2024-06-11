# -*- coding: utf-8; -*-

import warnings
from unittest import TestCase

from sqlalchemy import pool

from rattail.db import config as dbconfig
from rattail.config import RattailConfig


class TestGetEngines(TestCase):

    def setUp(self):
        self.config = RattailConfig()

    def test_default_section_is_rattail_db(self):
        self.config.setdefault('rattail.db', 'keys', 'default')
        self.config.setdefault('rattail.db', 'default.url', 'sqlite://')
        engines = dbconfig.get_engines(self.config)
        self.assertEqual(len(engines), 1)
        self.assertEqual(list(engines)[0], 'default')
        self.assertEqual(str(engines['default'].url), 'sqlite://')

    def test_custom_section_is_honored(self):
        self.config.setdefault('mycustomdb', 'keys', 'default')
        self.config.setdefault('mycustomdb', 'default.url', 'sqlite://')
        engines = dbconfig.get_engines(self.config, section=u'mycustomdb')
        self.assertEqual(len(engines), 1)
        self.assertEqual(list(engines)[0], 'default')
        self.assertEqual(str(engines['default'].url), 'sqlite://')

    def test_default_prefix_does_not_require_keys_declaration(self):
        self.config.setdefault('rattail.db', 'default.url', 'sqlite://')
        engines = dbconfig.get_engines(self.config)
        self.assertEqual(len(engines), 1)
        self.assertEqual(list(engines)[0], 'default')
        self.assertEqual(str(engines['default'].url), 'sqlite://')

    def test_default_prefix_falls_back_to_sqlalchemy(self):
        # Still no need to define "keys" option here.
        self.config.setdefault('rattail.db', 'sqlalchemy.url', 'sqlite://')
        engines = dbconfig.get_engines(self.config)
        self.assertEqual(len(engines), 1)
        self.assertEqual(list(engines)[0], 'default')
        self.assertEqual(str(engines['default'].url), 'sqlite://')

    def test_defined_keys_are_included_in_engines_result(self):
        # Note there is no "default" key here.
        self.config.setdefault('rattail.db', 'keys', 'host, store')
        self.config.setdefault('rattail.db', 'host.url', 'sqlite:///rattail.host.sqlite')
        self.config.setdefault('rattail.db', 'store.url', 'sqlite:///rattail.store.sqlite')
        engines = dbconfig.get_engines(self.config)
        self.assertEqual(len(engines), 2)
        self.assertEqual(sorted(engines.keys()), [u'host', u'store'])
        self.assertEqual(str(engines['host'].url), 'sqlite:///rattail.host.sqlite')
        self.assertEqual(str(engines['store'].url), 'sqlite:///rattail.store.sqlite')


class TestGetDefaultEngine(TestCase):

    def setUp(self):
        self.config = RattailConfig()

    def test_default_engine_is_loaded_from_rattail_db_section_by_default(self):
        self.config.setdefault('rattail.db', 'keys', 'default')
        self.config.setdefault('rattail.db', 'default.url', 'sqlite://')
        engine = dbconfig.get_default_engine(self.config)
        self.assertEqual(str(engine.url), 'sqlite://')

    def test_default_engine_is_loaded_from_custom_section_if_specified(self):
        self.config.setdefault('mycustomdb', 'keys', 'default')
        self.config.setdefault('mycustomdb', 'default.url', 'sqlite://')
        engine = dbconfig.get_default_engine(self.config, section=u'mycustomdb')
        self.assertEqual(str(engine.url), 'sqlite://')

    def test_no_engine_is_returned_if_none_is_defined(self):
        engine = dbconfig.get_default_engine(self.config)
        self.assertTrue(engine is None)
