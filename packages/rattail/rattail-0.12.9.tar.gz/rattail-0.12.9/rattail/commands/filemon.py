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
``rattail filemon`` command
"""

import sys
from enum import Enum
from pathlib import Path

import typer
from typing_extensions import Annotated

from .base import rattail_typer, Subcommand


class ServiceAction(str, Enum):
    start = 'start'
    stop = 'stop'
    install = 'install'
    debug = 'debug'
    uninstall = 'uninstall'


@rattail_typer.command()
def filemon(
        ctx: typer.Context,
        action: Annotated[
            ServiceAction,
            typer.Argument(help="Action to perform for the service.  Note that only "
                           "start/stop are used on Linux; the rest are Windows-only.")] = ...,
        pidfile: Annotated[
            Path,
            typer.Option('--pidfile', '-p',
                         help="Path to PID file.  (Only used on Linux.)")] = None,
        daemonize: Annotated[
            bool,
            typer.Option(help="DEPRECATED")] = False,
        username: Annotated[
            str,
            typer.Option(help="User account under which the service should run.  "
                         "(Only used on Windows.)")] = None,
        auto_start: Annotated[
            bool,
            typer.Option('--auto-start', '-a',
                         help="Configure service to start automatically.  "
                         "(Only used on Windows.)")] = False,
):
    """
    Manage the file monitor daemon
    """
    config = ctx.parent.rattail_config

    if sys.platform in ('linux', 'linux2'):
        from rattail.filemon import linux as filemon

        if action == 'start':
            filemon.start_daemon(config, pidfile)

        elif action == 'stop':
            filemon.stop_daemon(config, pidfile)

    elif sys.platform == 'win32': # pragma no cover
        run_win32(ctx.params)

    else:
        sys.stderr.write(f"File monitor is not supported on platform: {sys.platform}\n")
        sys.exit(1)


class FileMonitorCommand(Subcommand):
    """
    Interacts with the file monitor service; called as ``rattail filemon``.
    This command expects a subcommand; one of the following:

    * ``rattail filemon start``
    * ``rattail filemon stop``

    On Windows platforms, the following additional subcommands are available:

    * ``rattail filemon install``
    * ``rattail filemon uninstall`` (or ``rattail filemon remove``)

    .. note::
       The Windows Vista family of operating systems requires you to launch
       ``cmd.exe`` as an Administrator in order to have sufficient rights to
       run the above commands.

    .. See :doc:`howto.use_filemon` for more information.
    """
    name = 'filemon'
    description = "Manage the file monitor daemon"

    def add_parser_args(self, parser):
        subparsers = parser.add_subparsers(title='subcommands')

        start = subparsers.add_parser('start', help="Start service")
        start.set_defaults(subcommand='start')
        stop = subparsers.add_parser('stop', help="Stop service")
        stop.set_defaults(subcommand='stop')

        if sys.platform in ('linux', 'linux2'):
            parser.add_argument('-p', '--pidfile',
                                help="Path to PID file.", metavar='PATH')
            parser.add_argument('--daemonize', action='store_true',
                                help="DEPRECATED")
            parser.add_argument('--no-daemonize',
                                '-D', '--do-not-daemonize',
                                action='store_false', dest='daemonize',
                                help="DEPRECATED")

        elif sys.platform == 'win32': # pragma no cover

            install = subparsers.add_parser('install', help="Install service")
            install.set_defaults(subcommand='install')
            install.add_argument('-a', '--auto-start', action='store_true',
                                 help="Configure service to start automatically.")
            install.add_argument('-U', '--username',
                                 help="User account under which the service should run.")

            remove = subparsers.add_parser('remove', help="Uninstall (remove) service")
            remove.set_defaults(subcommand='remove')

            uninstall = subparsers.add_parser('uninstall', help="Uninstall (remove) service")
            uninstall.set_defaults(subcommand='remove')

            debug = subparsers.add_parser('debug', help="Run service in debug mode")
            debug.set_defaults(subcommand='debug')

    def run(self, args):
        if sys.platform in ('linux', 'linux2'):
            from rattail.filemon import linux as filemon

            if args.subcommand == 'start':
                filemon.start_daemon(self.config, args.pidfile)

            elif args.subcommand == 'stop':
                filemon.stop_daemon(self.config, args.pidfile)

        elif sys.platform == 'win32': # pragma no cover
            params = dict(args._get_kwargs())
            params['action'] = args.subcommand
            run_win32(params)

        else:
            self.stderr.write("File monitor is not supported on platform: {0}\n".format(sys.platform))
            sys.exit(1)


def run_win32(params): # pragma no cover
    from rattail.win32 import require_elevation
    from rattail.win32 import service
    from rattail.win32 import users
    from rattail.filemon import win32 as filemon

    require_elevation()

    options = []
    if params['action'] == 'install':

        username = params['username']
        if username:
            if '\\' in username:
                server, username = username.split('\\')
            else:
                server = socket.gethostname()
            if not users.user_exists(username, server):
                sys.stderr.write("User does not exist: {0}\\{1}\n".format(server, username))
                sys.exit(1)

            password = ''
            while password == '':
                password = getpass(str("Password for service user: ")).strip()
            options.extend(['--username', r'{0}\{1}'.format(server, username)])
            options.extend(['--password', password])

        if params['auto_start']:
            options.extend(['--startup', 'auto'])

    service.execute_service_command(filemon, params['action'], *options)

    # If installing with custom user, grant "logon as service" right.
    if params['action'] == 'install' and params['username']:
        users.allow_logon_as_service(username)

    # TODO: Figure out if the following is even required, or if instead we
    # should just be passing '--startup delayed' to begin with?

    # If installing auto-start service on Windows 7, we should update
    # its startup type to be "Automatic (Delayed Start)".
    # TODO: Improve this check to include Vista?
    if params['action'] == 'install' and params['auto_start']:
        if platform.release() == '7':
            name = filemon.RattailFileMonitor._svc_name_
            service.delayed_auto_start_service(name)
