# -*- coding: utf-8; -*-

import datetime
import argparse
from unittest import TestCase
# from unittest.mock import patch, Mock

from rattail.commands import core
from rattail.db import model, ConfigExtension
from rattail.config import RattailConfig


class TestArgumentParser(TestCase):

    def test_parse_args_preserves_extra_argv(self):
        parser = core.ArgumentParser()
        parser.add_argument('--some-optional-arg')
        parser.add_argument('some_required_arg')
        args = parser.parse_args([
                '--some-optional-arg', 'optional-value', 'required-value',
                'some', 'extra', 'args'])
        self.assertEqual(args.some_required_arg, 'required-value')
        self.assertEqual(args.some_optional_arg, 'optional-value')
        self.assertEqual(args.argv, ['some', 'extra', 'args'])


class TestDateArgument(TestCase):

    def test_valid_date_string_returns_date_object(self):
        date = core.date_argument('2014-01-01')
        self.assertEqual(date, datetime.date(2014, 1, 1))

    def test_invalid_date_string_raises_error(self):
        self.assertRaises(argparse.ArgumentTypeError, core.date_argument, 'invalid-date')


class TestCommand(TestCase):

    def test_initial_subcommands_are_sane(self):
        command = core.Command()
        self.assertTrue('filemon' in command.subcommands)

    def test_iter_subcommands_includes_expected_item(self):
        command = core.Command()
        found = False
        for subcommand in command.iter_subcommands():
            if subcommand.name == 'filemon':
                found = True
                break
        self.assertTrue(found)

    # # # TODO: Figure out a better way to test this, or don't bother.
    # # def test_noinit_flag_means_no_config(self):
    # #     command = commands.Command()
    # #     fake = command.subcommands['fake'] = Mock()
    # #     command.run('fake', '--no-init')
    # #     self.assertEqual(len(fake.return_value.config.files_requested), 0)


class TestSubcommand(TestCase):

    def test_get_runas_user(self):

        # ugh what a mess, this should be easier to setup
        config = RattailConfig(defaults={
            'rattail.db.default.url': 'sqlite://',
        })
        ConfigExtension().configure(config)
        model.Base.metadata.create_all(bind=config.rattail_engine)

        # make subcommand
        cmd = core.Command(config=config)
        subcmd = core.Subcommand(cmd)

        # no user if none requested, and config is empty
        self.assertIsNone(subcmd.get_runas_user())

        # requesting nonexistent user returns none
        self.assertIsNone(subcmd.get_runas_user(username='barney'))

        # now create the user for following tests
        app = config.get_app()
        with app.short_session(commit=True) as s:
            s.add(model.User(username='barney'))

        # this should now return our user
        user = subcmd.get_runas_user(username='barney')
        self.assertEqual(user.username, 'barney')

        # default is still null for the subcommand though
        self.assertIsNone(subcmd.get_runas_user())

        # unless subcommand declares a default username
        subcmd.runas_username = 'barney'
        user = subcmd.get_runas_user()
        self.assertEqual(user.username, 'barney')


# TODO: more broken tests..ugh.  these aren't very good or else i might bother
# fixing them...
# class TestFileMonitor(TestCase):

#     @patch('rattail.filemon.linux.start_daemon')
#     def test_start_daemon_with_default_args(self, start_daemon):
#         commands.main('filemon', '--no-init', 'start')
#         start_daemon.assert_called_once_with(None, None, True)

#     @patch('rattail.filemon.linux.start_daemon')
#     def test_start_daemon_with_explicit_args(self, start_daemon):
#         tmp = TempIO()
#         pid_path = tmp.putfile('test.pid', '')
#         commands.main('filemon', '--no-init', '--pidfile', pid_path, '--do-not-daemonize', 'start')
#         start_daemon.assert_called_once_with(None, pid_path, False)

#     @patch('rattail.filemon.linux.stop_daemon')
#     def test_stop_daemon_with_default_args(self, stop_daemon):
#         commands.main('filemon', '--no-init', 'stop')
#         stop_daemon.assert_called_once_with(None, None)

#     @patch('rattail.filemon.linux.stop_daemon')
#     def test_stop_daemon_with_explicit_args(self, stop_daemon):
#         tmp = TempIO()
#         pid_path = tmp.putfile('test.pid', '')
#         commands.main('filemon', '--no-init', '--pidfile', pid_path, 'stop')
#         stop_daemon.assert_called_once_with(None, pid_path)

#     @patch('rattail.commands.sys')
#     def test_unknown_platform_not_supported(self, sys):
#         tmp = TempIO()
#         stderr_path = tmp.putfile('stderr.txt', '')
#         sys.platform = 'bogus'
#         commands.main('--no-init', '--stderr', stderr_path, 'filemon', 'start')
#         sys.exit.assert_called_once_with(1)
#         with open(stderr_path) as f:
#             self.assertEqual(f.read(), "File monitor is not supported on platform: bogus\n")
