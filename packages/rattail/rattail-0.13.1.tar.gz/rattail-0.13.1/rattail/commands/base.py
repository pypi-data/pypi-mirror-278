# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
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
Console Commands - base classes and core commands
"""

import os
import sys
import json
import argparse
import datetime
import warnings
import logging

from wuttjamaican.cmd.base import (Command as WuttaCommand,
                                   CommandArgumentParser,
                                   Subcommand as WuttaSubcommand)
from wuttjamaican.util import parse_list

from rattail import __version__
from rattail.progress import ConsoleProgress, SocketProgress
from rattail.config import make_config
from rattail.db.config import configure_versioning
from rattail.commands.typer import make_typer


rattail_typer = make_typer(
    name='rattail',
    help="Rattail Software Framework"
)


class ArgumentParser(CommandArgumentParser):
    """
    Custom argument parser.

    This is a compatibility wrapper around upstream
    :class:`wuttjamaican:wuttjamaican.commands.base.CommandArgumentParser`.
    New code should use that instead; this will eventually be removed.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn("the custom ArgumentParser in rattail is deprecated; "
                      "please use the one from wuttjamaican instead",
                      DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)


def date_argument(string):
    """
    Validate and coerce a date argument.

    This function is designed be used as the ``type`` parameter when calling
    ``ArgumentParser.add_argument()``, e.g.::

       parser = ArgumentParser()
       parser.add_argument('--date', type=date_argument)
    """
    try:
        date = datetime.datetime.strptime(string, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError("Date must be in YYYY-MM-DD format")
    return date


def dict_argument(string):
    """
    Coerce the given string to a Python dictionary.  The string is assumed to
    be JSON-encoded; this function merely invokes ``json.loads()`` on it.

    This function is designed be used as the ``type`` parameter when calling
    ``ArgumentParser.add_argument()``, e.g.::

       parser = ArgumentParser()
       parser.add_argument('--date', type=dict_argument)
    """
    try:
        return json.loads(string)
    except json.decoder.JSONDecodeError:
        raise argparse.ArgumentTypeError("Argument must be valid JSON-encoded string")


def list_argument(string):
    """
    Coerce the given string to a list of strings, splitting on whitespace
    and/or commas.

    This function is designed be used as the ``type`` parameter when calling
    ``ArgumentParser.add_argument()``, e.g.::

       parser = ArgumentParser()
       parser.add_argument('--things', type=list_argument)
    """
    return parse_list(string)


class RattailCommand(WuttaCommand):
    """
    The primary command for Rattail.

    This inherits from
    :class:`wuttjamaican:wuttjamaican.commands.base.Command` so see
    those docs for more info.

    Custom apps based on Rattail will probably want to make and
    register their own ``Command`` class derived from this one.  Again
    see upstream docs for more details.

    Rattail extends the upstream class by adding the following:
    """
    name = 'rattail'
    version = __version__
    description = "Rattail Software Framework"

    @property
    def db_config_section(self):
        """
        Name of section in config file which should have database connection
        info.  This defaults to ``'rattail.db'`` but may be overridden so the
        command framework can sit in front of a non-Rattail database if needed.

        This is used to auto-configure a "default" database engine for the app,
        when any command is invoked.
        """
        # TODO: surely this can be more dynamic? or is it really being used?
        return 'rattail.db'

    @property
    def db_session_factory(self):
        """
        Returns a reference to the configured session factory.

        This is a compatibility wrapper around
        :meth:`rattail.app.AppHandler.make_session()`.  New code
        should use that instead; this may eventually be removed.
        """
        return self.config.get_app().make_session

    @property
    def db_model(self):
        """
        Returns a reference to configured model module.

        This is a compatibility wrapper around
        :meth:`rattail.config.RattailConfig.get_model()`.  New
        code should use that instead; this may eventually be removed.
        """
        return self.config.get_model()

    def iter_subcommands(self):
        """
        Returns a generator for the subcommands, sorted by name.

        This should probably not be used; instead see upstream
        :meth:`wuttjamaican:wuttjamaican.commands.base.Command.sorted_subcommands()`.
        """
        for subcmd in self.sorted_subcommands():
            yield subcmd

    def add_args(self):
        """
        Configure args for the main command arg parser.

        Rattail extends the upstream
        :meth:`~wuttjamaican:wuttjamaican.commands.base.Command.add_args()`
        by adding various command line args which have traditionally
        been available for it.  Some of these may disappear some day
        but no changes are planned just yet.
        """
        super().add_args()
        parser = self.parser

        # TODO: i think these aren't really being used in practice..?
        parser.add_argument('-n', '--no-init', action='store_true', default=False)
        parser.add_argument('--no-extend-config', dest='extend_config', action='store_false')

        parser.add_argument('--verbose', action='store_true')
        parser.add_argument('--progress-socket',
                            help="Optional socket (e.g. localhost:8487) to which progress info should be written.")
        parser.add_argument('--runas', '-R', metavar='USERNAME',
                            help="Optional username to impersonate when running the command.  "
                            "This is only relevant for / used by certain commands.")

        # data versioning
        parser.add_argument('--versioning', action='store_true',
                            help="Force *enable* of data versioning.  If set, then --no-versioning "
                            "cannot also be set.  If neither is set, config will determine whether "
                            "or not data versioning should be enabled.")
        parser.add_argument('--no-versioning', action='store_true',
                            help="Force *disable* of data versioning.  If set, then --versioning "
                            "cannot also be set.  If neither is set, config will determine whether "
                            "or not data versioning should be enabled.")

    def make_config(self, args):
        """
        Make the config object in preparation for running a subcommand.

        See also upstream
        :meth:`~wuttjamaican:wuttjamaican.commands.base.Command.make_config()`
        but for now, Rattail overrides this completely, mostly for the
        sake of versioning setup.
        """
        # TODO: can we make better args so this is handled by argparse somehow?
        if args.versioning and args.no_versioning:
            self.stderr.write("Cannot pass both --versioning and --no-versioning\n")
            sys.exit(1)

        # if args say not to "init" then we make a sort of empty config
        if args.no_init:
            config = make_config([], extend=False, versioning=False)

        else: # otherwise we make a proper config, and maybe turn on versioning
            logging.basicConfig()
            config = make_config(args.config_paths, plus_files=args.plus_config_paths,
                                 extend=args.extend_config, versioning=False)
            if args.versioning:
                configure_versioning(config, force=True)
            elif not args.no_versioning:
                configure_versioning(config)

        # import our primary data model now, just in case it hasn't fully been
        # imported yet.  this it to be sure association proxies and the like
        # are fully wired up in the case of extensions
        # TODO: what about web apps etc.? i guess i was only having the problem
        # for some importers, e.g. basic CORE API -> Rattail w/ the schema
        # extensions in place from rattail-corepos
        try:
            config.get_model()
        except ImportError:
            pass

        return config

    def prep_subcommand(self, subcmd, args):
        """
        Rattail overrides this method to apply some of the global args
        directly to the subcommand object.

        See also upstream
        :meth:`~wuttjamaican:wuttjamaican.commands.base.Command.prep_subcommand()`.
        """
        # figure out if/how subcommand should show progress
        subcmd.show_progress = args.progress
        subcmd.progress = None
        if subcmd.show_progress:
            if args.progress_socket:
                host, port = args.progress_socket.split(':')
                subcmd.progress = SocketProgress(host, int(port))
            else:
                subcmd.progress = ConsoleProgress

        # maybe should be verbose
        subcmd.verbose = args.verbose

        # TODO: make this default to something from config?
        subcmd.runas_username = args.runas or None


# TODO: deprecate / remove this?
Command = RattailCommand


class RattailSubcommand(WuttaSubcommand):
    """
    Base class for subcommands.

    This inherits from :class:`wuttjamaican.commands.base.Subcommand`
    so see those docs for more info.

    Rattail extends the subcommand to include:

    .. attribute:: runas_username

       Username (:attr:`~rattail.db.model.users.User.username`)
       corresponding to the :class:`~rattail.db.model.users.User`
       which the command should "run as" - i.e.  for sake of version
       history etc.

    .. attribute:: show_progress

       Boolean indicating whether progress should be shown for the
       subcommand.

    .. attribute:: progress

       Optional factory to be used when creating progress objects.
       This is ``None`` by default but if :attr:`show_progress` is
       enabled, then :class:`~rattail.progress.ConsoleProgress` is the
       default factory.

    .. attribute:: verbose

       Flag indicating the subcommand should be free to print
       arbitrary messages to
       :attr:`~wuttjamaican:wuttjamaican.commands.base.Subcommand.stdout`.
    """
    runas_username = None
    show_progress = False
    progress = None
    verbose = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: deprecate / remove this
        self.parent = self.command

    def add_args(self):
        """
        This is the "same" as upstream
        :meth:`wuttjamaican:wuttjamaican.commands.base.Subcommand.add_args()`
        except Rattail must customize this to also invoke its
        deprecated method, :meth:`add_parser_args()`.
        """
        super().add_args()
        self.add_parser_args(self.parser)

    def add_parser_args(self, parser):
        """
        This method is deprecated and will eventually be removed;
        please define :meth:`add_args()` instead.
        """

    @property
    def model(self):
        return self.parent.db_model

    def make_session(self):
        session = self.parent.db_session_factory()
        user = self.get_runas_user(session=session)
        if user:
            session.set_continuum_user(user)
        return session

    def finalize_session(self, *args, **kwargs):
        """
        Wrap up the given session, per the given arguments.  This is meant to
        provide a simple convenience, for commands which must do work within a
        DB session, but would like to support a "dry run" mode.
        """
        from rattail.db.util import finalize_session
        return finalize_session(*args, **kwargs)

    def get_runas_user(self, session=None, username=None):
        """
        Convenience method to get the "runas" User object for the
        current command.

        Uses :meth:`rattail.app.AppHandler.get_runas_user()` under the
        hood, but the ``--runas`` command line param provides the default
        username.
        """
        if not username:
            username = getattr(self, 'runas_username', None)
        return self.app.get_runas_user(session=session, username=username)

    def progress_loop(self, func, items, factory=None, **kwargs):
        return self.app.progress_loop(func, items, factory or self.progress, **kwargs)

    # TODO: deprecate / remove this
    def get_pip_path(self):
        return os.path.join(sys.prefix, 'bin', 'pip')

    def require_prompt_toolkit(self):
        from rattail.commands.util import require_prompt_toolkit
        return require_prompt_toolkit(self.config)

    def require_rich(self):
        from rattail.commands.util import require_rich
        return require_rich(self.config)

    def rprint(self, *args, **kwargs):
        from rattail.commands.util import rprint
        return rprint(*args, **kwargs)

    def basic_prompt(self, *args, **kwargs):
        from rattail.commands.util import basic_prompt
        return basic_prompt(*args, **kwargs)


# TODO: deprecate / remove this?
Subcommand = RattailSubcommand


def main(*args):
    """
    The primary entry point for the Rattail command system.
    """
    if args:
        args = list(args)
    else:
        args = sys.argv[1:]

    cmd = Command()
    cmd.run(*args)
