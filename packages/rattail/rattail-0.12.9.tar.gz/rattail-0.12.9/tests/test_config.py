# -*- coding: utf-8; -*-

import configparser
import datetime
import os
from unittest import TestCase
from unittest.mock import patch

from wuttjamaican.testing import FileConfigTestCase

from rattail import config
from rattail.app import AppHandler


class TestParseBoolFunc(TestCase):

    def test_none(self):
        self.assertIsNone(config.parse_bool(None))

    def test_true(self):
        self.assertIs(config.parse_bool(True), True)

    def test_false(self):
        self.assertIs(config.parse_bool(False), False)

    def test_string(self):
        self.assertTrue(config.parse_bool('true'))
        self.assertTrue(config.parse_bool('yes'))
        self.assertTrue(config.parse_bool('on'))
        self.assertTrue(config.parse_bool('1'))

        self.assertFalse(config.parse_bool('false'))
        self.assertFalse(config.parse_bool('no'))
        self.assertFalse(config.parse_bool('off'))
        self.assertFalse(config.parse_bool('0'))


class TestParseListFunc(TestCase):

    def test_none(self):
        value = config.parse_list(None)
        self.assertEqual(len(value), 0)

    def test_single_value(self):
        value = config.parse_list(u'foo')
        self.assertEqual(len(value), 1)
        self.assertEqual(value[0], u'foo')

    def test_single_value_padded_by_spaces(self):
        value = config.parse_list(u'   foo   ')
        self.assertEqual(len(value), 1)
        self.assertEqual(value[0], u'foo')

    def test_slash_is_not_a_separator(self):
        value = config.parse_list(u'/dev/null')
        self.assertEqual(len(value), 1)
        self.assertEqual(value[0], u'/dev/null')

    def test_multiple_values_separated_by_whitespace(self):
        value = config.parse_list(u'foo bar baz')
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0], u'foo')
        self.assertEqual(value[1], u'bar')
        self.assertEqual(value[2], u'baz')

    def test_multiple_values_separated_by_commas(self):
        value = config.parse_list(u'foo,bar,baz')
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0], u'foo')
        self.assertEqual(value[1], u'bar')
        self.assertEqual(value[2], u'baz')

    def test_multiple_values_separated_by_whitespace_and_commas(self):
        value = config.parse_list(u'  foo,   bar   baz')
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0], u'foo')
        self.assertEqual(value[1], u'bar')
        self.assertEqual(value[2], u'baz')

    def test_multiple_values_separated_by_whitespace_and_commas_with_some_quoting(self):
        value = config.parse_list("""
        foo
        "C:\\some path\\with spaces\\and, a comma",
        baz
        """)
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0], u'foo')
        self.assertEqual(value[1], u'C:\\some path\\with spaces\\and, a comma')
        self.assertEqual(value[2], u'baz')

    def test_multiple_values_separated_by_whitespace_and_commas_with_single_quotes(self):
        value = config.parse_list("""
        foo
        'C:\\some path\\with spaces\\and, a comma',
        baz
        """)
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0], 'foo')
        self.assertEqual(value[1], 'C:\\some path\\with spaces\\and, a comma')
        self.assertEqual(value[2], 'baz')


class TestRattailConfig(FileConfigTestCase):

    def setup_files(self):
        self.site_path = self.write_file('site.conf', """
[rattail]
        """)

        self.host_path = self.write_file('host.conf', """
[rattail.config]
include = "{}"
        """.format(self.site_path))

        self.app_path = self.write_file('app.conf', """
[rattail.config]
include = "{}"
        """.format(self.host_path))

        self.custom_path = self.write_file('custom.conf', """
[rattail.config]
include = "%(here)s/app.conf"
        """)

    def test_init_defaults(self):
        cfg = config.RattailConfig()
        self.assertEqual(cfg.files_requested, [])
        self.assertEqual(cfg.files_read, [])

    def test_init_params(self):
        self.setup_files()

        # files
        cfg = config.RattailConfig()
        self.assertEqual(cfg.files_requested, [])
        self.assertEqual(cfg.files_read, [])
        cfg = config.RattailConfig(files=[self.site_path])
        self.assertEqual(cfg.files_requested, [self.site_path])
        self.assertEqual(cfg.files_read, [self.site_path])

        # usedb
        cfg = config.RattailConfig()
        self.assertFalse(cfg.usedb)
        cfg = config.RattailConfig(usedb=True)
        self.assertTrue(cfg.usedb)

        # preferdb
        cfg = config.RattailConfig()
        self.assertFalse(cfg.preferdb)
        cfg = config.RattailConfig(preferdb=True)
        self.assertTrue(cfg.preferdb)

    def test_read_file_with_recurse(self):
        self.setup_files()
        cfg = config.RattailConfig()
        cfg.read_file(self.custom_path, recurse=True)
        self.assertEqual(cfg.files_requested, [self.custom_path, self.app_path, self.host_path, self.site_path])
        self.assertEqual(cfg.files_read, [self.site_path, self.host_path, self.app_path, self.custom_path])

    def test_read_file_once_only(self):
        self.setup_files()

        another_path = self.write_file('another.conf', """
[rattail.config]
include = "{custom}" "{site}" "{app}" "{site}" "{custom}"
        """.format(custom=self.custom_path, app=self.app_path, site=self.site_path))

        cfg = config.RattailConfig()
        cfg.read_file(another_path, recurse=True)
        self.assertEqual(cfg.files_requested, [another_path, self.custom_path, self.app_path, self.host_path, self.site_path])
        self.assertEqual(cfg.files_read, [self.site_path, self.host_path, self.app_path, self.custom_path, another_path])

    def test_read_file_skip_missing(self):
        self.setup_files()
        bogus_path = '/tmp/does-not/exist'
        self.assertFalse(os.path.exists(bogus_path))

        another_path = self.write_file('another.conf', """
[rattail.config]
include = "{bogus}" "{app}" "{bogus}" "{site}"
        """.format(bogus=bogus_path, app=self.app_path, site=self.site_path))

        cfg = config.RattailConfig()
        cfg.read_file(another_path, recurse=True)
        self.assertEqual(cfg.files_requested, [another_path, bogus_path, self.app_path, self.host_path, self.site_path])
        self.assertEqual(cfg.files_read, [self.site_path, self.host_path, self.app_path, another_path])

    @patch('rattail.config.logging.config.fileConfig')
    def test_configure_logging(self, fileConfig):
        cfg = config.RattailConfig()

        # logging not configured by default
        cfg.configure_logging()
        self.assertFalse(fileConfig.called)

        # but config option can enable it
        cfg.set('rattail.config', 'configure_logging', 'true')
        cfg.configure_logging()
        self.assertEqual(fileConfig.call_count, 1)
        fileConfig.reset_mock()

        # invalid logging config is ignored
        fileConfig.side_effect = configparser.NoSectionError('loggers')
        cfg.configure_logging()
        self.assertEqual(fileConfig.call_count, 1)


class TestRattailConfig(FileConfigTestCase):

    def test_prioritized_files(self):
        first = self.write_file('first.conf', """\
[foo]
bar = 1
""")

        second = self.write_file('second.conf', """\
[rattail.config]
require = %(here)s/first.conf
""")

        myconfig = config.RattailConfig(files=[second])
        files = myconfig.prioritized_files
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0], second)
        self.assertEqual(files[1], first)
        self.assertIs(files, myconfig.get_prioritized_files())

    def test_setdefault(self):
        myconfig = config.RattailConfig()

        # nb. the tests below are effectively testing the custom get()
        # method in addition to setdefault()

        # value is empty by default
        self.assertIsNone(myconfig.get('foo.bar'))
        self.assertIsNone(myconfig.get('foo', 'bar'))

        # but we can change that by setting default
        myconfig.setdefault('foo.bar', 'baz')
        self.assertEqual(myconfig.get('foo.bar'), 'baz')
        self.assertEqual(myconfig.get('foo', 'bar'), 'baz')

        # also can set a default via section, option (as well as key)
        self.assertIsNone(myconfig.get('foo.blarg'))
        myconfig.setdefault('foo' ,'blarg', 'blast')
        self.assertEqual(myconfig.get('foo.blarg'), 'blast')
        self.assertEqual(myconfig.get('foo', 'blarg'), 'blast')

        # error is raised if args are ambiguous
        self.assertRaises(ValueError, myconfig.setdefault, 'foo', 'bar', 'blarg', 'blast')

        # try that for get() too
        self.assertRaises(ValueError, myconfig.get, 'foo', 'bar', 'blarg', 'blast')

    def test_getbool(self):
        myconfig = config.RattailConfig()
        self.assertFalse(myconfig.getbool('foo.bar'))
        myconfig.setdefault('foo.bar', 'true')
        self.assertTrue(myconfig.getbool('foo.bar'))

    def test_getint(self):
        myconfig = config.RattailConfig()
        self.assertIsNone(myconfig.getint('foo.bar'))
        myconfig.setdefault('foo.bar', '42')
        self.assertEqual(myconfig.getint('foo.bar'), 42)

    def test_getlist(self):
        myconfig = config.RattailConfig()
        self.assertIsNone(myconfig.getlist('foo.bar'))
        myconfig.setdefault('foo.bar', 'hello world')
        self.assertEqual(myconfig.getlist('foo.bar'), ['hello', 'world'])

    def test_getdate(self):
        myconfig = config.RattailConfig()
        self.assertIsNone(myconfig.getdate('foo.date'))
        myconfig.setdefault('foo.date', '2023-11-20')
        value = myconfig.getdate('foo.date')
        self.assertIsInstance(value, datetime.date)
        self.assertEqual(value, datetime.date(2023, 11, 20))

    def test_get_app(self):
        myconfig = config.RattailConfig()
        app = myconfig.get_app()
        self.assertIsInstance(app, AppHandler)
        self.assertIs(type(app), AppHandler)

    def test_parse_bool(self):
        myconfig = config.RattailConfig()
        self.assertTrue(myconfig.parse_bool('true'))
        self.assertFalse(myconfig.parse_bool('false'))

    def test_parse_list(self):
        myconfig = config.RattailConfig()
        self.assertEqual(myconfig.parse_list(None), [])
        self.assertEqual(myconfig.parse_list('hello world'), ['hello', 'world'])

    def test_make_list_string(self):
        myconfig = config.RattailConfig()

        value = myconfig.make_list_string(['foo', 'bar'])
        self.assertEqual(value, 'foo, bar')

        value = myconfig.make_list_string(['hello world', 'how are you'])
        self.assertEqual(value, "'hello world', 'how are you'")

        value = myconfig.make_list_string(["you don't", 'say'])
        self.assertEqual(value, "\"you don't\", say")

    def test_beaker_invalidate_setting(self):
        # TODO: this doesn't really test anything, just gives coverage
        myconfig = config.RattailConfig()
        myconfig.beaker_invalidate_setting('foo')


class TestRattailDefaultFiles(FileConfigTestCase):

    def test_quiet_conf(self):
        generic = self.write_file('generic.conf', '')
        quiet = self.write_file('quiet.conf', '')

        with patch('rattail.config.generic_default_files') as generic_default_files:
            generic_default_files.return_value = [generic]

            with patch('rattail.config.os') as mockos:
                mockos.path.join.return_value = quiet

                # generic files by default
                mockos.path.exists.return_value = False
                files = config.rattail_default_files('rattail')
                generic_default_files.assert_called_once_with('rattail')
                self.assertEqual(files, [generic])

                # but if quiet.conf exists, will return that
                generic_default_files.reset_mock()
                mockos.path.exists.return_value = True
                files = config.rattail_default_files('rattail')
                generic_default_files.assert_not_called()
                self.assertEqual(files, [quiet])


class TestMakeConfig(FileConfigTestCase):

    def test_files(self):
        generic = self.write_file('generic.conf', '')
        myfile = self.write_file('my.conf', '')

        # generic files by default
        myconfig = config.make_config(default_files=[generic])
        self.assertEqual(myconfig.files_read, [generic])

        # can specify single primary file
        myconfig = config.make_config(myfile, default_files=[generic])
        self.assertEqual(myconfig.files_read, [myfile])

        # can specify primary files as list
        myconfig = config.make_config([myfile], default_files=[generic])
        self.assertEqual(myconfig.files_read, [myfile])

        # can specify primary files via env
        myconfig = config.make_config(env={'RATTAIL_CONFIG_FILES': myfile},
                                      default_files=[generic])
        self.assertEqual(myconfig.files_read, [myfile])
