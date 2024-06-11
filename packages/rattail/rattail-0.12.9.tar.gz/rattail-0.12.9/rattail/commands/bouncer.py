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
``rattail bouncer`` command
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


@rattail_typer.command()
def bouncer(
        ctx: typer.Context,
        action: Annotated[
            ServiceAction,
            typer.Argument(help="Action to perform for the service.")] = ...,
        pidfile: Annotated[
            Path,
            typer.Option('--pidfile', '-p',
                         help="Path to PID file.")] = None,
        daemonize: Annotated[
            bool,
            typer.Option(help="DEPRECATED")] = False,
):
    """
    Manage the email bouncer daemon
    """
    from rattail.bouncer.daemon import BouncerDaemon

    config = ctx.parent.rattail_config
    daemon = BouncerDaemon(pidfile, config=config)
    if action == 'stop':
        daemon.stop()
    else: # start
        try:
            daemon.start(daemonize=False)
        except KeyboardInterrupt:
            sys.stderr.write("Interrupted.\n")


class EmailBouncer(Subcommand):
    """
    Interacts with the email bouncer daemon.  This command expects a
    subcommand; one of the following:

    * ``rattail bouncer start``
    * ``rattail bouncer stop``
    """
    name = 'bouncer'
    description = "Manage the email bouncer daemon"

    def add_parser_args(self, parser):
        subparsers = parser.add_subparsers(title='subcommands')

        start = subparsers.add_parser('start', help="Start service")
        start.set_defaults(subcommand='start')
        stop = subparsers.add_parser('stop', help="Stop service")
        stop.set_defaults(subcommand='stop')

        parser.add_argument('-p', '--pidfile', metavar='PATH', default='/var/run/rattail/bouncer.pid',
                            help="Path to PID file.")
        parser.add_argument('--daemonize', action='store_true',
                            help="DEPRECATED")
        parser.add_argument('--no-daemonize',
                            '-D', '--do-not-daemonize',
                            action='store_false', dest='daemonize',
                            help="DEPRECATED")

    def run(self, args):
        from rattail.bouncer.daemon import BouncerDaemon

        daemon = BouncerDaemon(args.pidfile, config=self.config)
        if args.subcommand == 'stop':
            daemon.stop()
        else: # start
            try:
                daemon.start(daemonize=False)
            except KeyboardInterrupt:
                self.stderr.write("Interrupted.\n")
