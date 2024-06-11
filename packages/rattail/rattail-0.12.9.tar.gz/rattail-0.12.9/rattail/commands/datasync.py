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
Console Commands
"""

import sys
import time
import datetime
import logging
from enum import Enum
from pathlib import Path

import typer
from typing_extensions import Annotated

from .base import rattail_typer, Subcommand


log = logging.getLogger(__name__)


class ServiceAction(str, Enum):
    start = 'start'
    stop = 'stop'
    check_queue = 'check-queue'
    check_watchers = 'check-watchers'
    collectd = 'collectd'
    wait = 'wait'
    remove_settings = 'remove-settings'


@rattail_typer.command()
def datasync(
        ctx: typer.Context,
        action: Annotated[
            ServiceAction,
            typer.Argument(help="Action to perform for the service.")] = ...,
        pidfile: Annotated[
            Path,
            typer.Option('--pidfile', '-p',
                         help="Path to PID file.")] = '/var/run/rattail/datasync.pid',
        daemonize: Annotated[
            bool,
            typer.Option(help="DEPRECATED")] = False,
        timeout: Annotated[
            int,
            typer.Option('--timeout', '-T',
                         help="Optional timeout (in minutes) for use with the 'wait' "
                         "or 'check' actions.  If specified for 'wait', the waiting "
                         "will stop after the given number of minutes and exit with a "
                         "nonzero code to indicate failure.  If specified for 'check', "
                         "the command will perform some health check based on the given "
                         "timeout, and exit with nonzero code if the check fails.")] = 0,
        collectd_plugin: Annotated[
            str,
            typer.Option(help="The `plugin-instance` part of the 'Identifier' "
                         "to be passed to collectd via PUTVAL entries.")] = 'datasync',
):
    """
    Manage the data sync daemon
    """
    from rattail.datasync.daemon import DataSyncDaemon

    config = ctx.parent.rattail_config

    if action == 'wait':
        do_wait(config, timeout)

    elif action == 'check':
        do_check_queue(config, timeout)

    elif action == 'check-queue':
        do_check_queue(config, timeout)

    elif action == 'check-watchers':
        do_check_watchers(config, timeout)

    elif action == 'collectd':
        do_collectd(config, collectd_plugin)

    elif action == 'remove-settings':
        do_remove_settings(config)

    else: # manage the daemon
        daemon = DataSyncDaemon(pidfile, config=config)
        if action == 'stop':
            daemon.stop()
        else: # start
            try:
                daemon.start(daemonize=False)
            except KeyboardInterrupt:
                sys.stderr.write("Interrupted.\n")


class DataSync(Subcommand):
    """
    Manage the data sync daemon
    """
    name = 'datasync'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        subparsers = parser.add_subparsers(title='subcommands')

        start = subparsers.add_parser('start', help="Start service")
        start.set_defaults(subcommand='start')

        stop = subparsers.add_parser('stop', help="Stop service")
        stop.set_defaults(subcommand='stop')

        check = subparsers.add_parser('check', help="(DEPRECATED) Check for stale (lingering) changes in queue")
        check.set_defaults(subcommand='check')

        check_queue = subparsers.add_parser('check-queue', help="Check for stale (lingering) changes in queue")
        check_queue.set_defaults(subcommand='check-queue')

        check_watchers = subparsers.add_parser('check-watchers', help="Check for dead watcher threads")
        check_watchers.set_defaults(subcommand='check-watchers')

        collectd = subparsers.add_parser('collectd', help="Output statistics for collectd")
        collectd.set_defaults(subcommand='collectd')

        wait = subparsers.add_parser('wait', help="Wait for changes to be processed")
        wait.set_defaults(subcommand='wait')

        remove_settings = subparsers.add_parser(
            'remove-settings',
            help="Remove all datasync settings from the DB")
        remove_settings.set_defaults(subcommand='remove-settings')

        parser.add_argument('-p', '--pidfile', metavar='PATH', default='/var/run/rattail/datasync.pid',
                            help="Path to PID file.")
        parser.add_argument('--daemonize', action='store_true',
                            help="DEPRECATED")
        parser.add_argument('--no-daemonize',
                            '-D', '--do-not-daemonize',
                            action='store_false', dest='daemonize',
                            help="DEPRECATED")
        parser.add_argument('-T', '--timeout', metavar='MINUTES', type=int, default=0,
                            help="Optional timeout (in minutes) for use with the 'wait' or 'check' commands.  "
                            "If specified for 'wait', the waiting still stop after the given number of minutes "
                            "and exit with a nonzero code to indicate failure.  If specified for 'check', the "
                            "command will perform some health check based on the given timeout, and exit with "
                            "nonzero code if the check fails.")

        parser.add_argument('--collectd-plugin', default='datasync',
                            help="The `plugin-instance` part of the 'Identifier' "
                            "to be passed to collectd via PUTVAL entries.")

    def run(self, args):
        from rattail.datasync.daemon import DataSyncDaemon

        self.datasync_handler = self.app.get_datasync_handler()

        if args.subcommand == 'wait':
            do_wait(self.config, args.timeout)

        elif args.subcommand == 'check':
            do_check_queue(self.config, args.timeout)

        elif args.subcommand == 'check-queue':
            do_check_queue(self.config, args.timeout)

        elif args.subcommand == 'check-watchers':
            do_check_watchers(self.config, args.timeout)

        elif args.subcommand == 'collectd':
            do_collectd(self.config, args.collectd_plugin)

        elif args.subcommand == 'remove-settings':
            do_remove_settings(self.config)

        else: # manage the daemon
            daemon = DataSyncDaemon(args.pidfile, config=self.config)
            if args.subcommand == 'stop':
                daemon.stop()
            else: # start
                try:
                    daemon.start(daemonize=False)
                except KeyboardInterrupt:
                    self.stderr.write("Interrupted.\n")


def do_check_queue(config, timeout):
    """
    Perform general queue / health check for datasync.
    """
    app = config.get_app()
    model = app.model
    session = app.make_session()

    # looking for changes which have been around for "timeout" minutes
    timeout = timeout or 90
    cutoff = app.make_utc() - datetime.timedelta(seconds=60 * timeout)
    changes = session.query(model.DataSyncChange)\
                     .filter(model.DataSyncChange.obtained < cutoff)\
                     .count()
    session.close()

    # if we found stale changes, then "fail" - otherwise we'll "succeed"
    if changes:
        # TODO: should log set of unique payload types, for troubleshooting
        log.debug("found %s changes, in queue for %s minutes", changes, timeout)
        sys.stderr.write("Found {} changes, in queue for {} minutes\n".format(changes, timeout))
        sys.exit(1)

    log.info("found no changes in queue for %s minutes", timeout)


def do_check_watchers(config, timeout):
    """
    Perform general health check for datasync watcher threads.
    """
    app = config.get_app()
    datasync = app.get_datasync_handler()
    profiles = datasync.get_configured_profiles()
    session = app.make_session()

    # cutoff is "timeout" minutes before "now"
    timeout = timeout or 15
    cutoff = app.make_utc() - datetime.timedelta(seconds=60 * timeout)

    dead = []
    for key in profiles:

        # looking for watcher "last run" time older than "timeout" minutes
        lastrun = datasync.get_watcher_lastrun(
            key, tzinfo=False, session=session)
        if lastrun and lastrun < cutoff:
            dead.append(key)

    session.close()

    # if we found dead watchers, then "fail" - otherwise we'll "succeed"
    if dead:
        sys.stderr.write("Found {} watcher threads dead for {} minutes: {}\n".format(len(dead), timeout, ', '.join(dead)))
        sys.exit(1)

    log.info("found no watcher threads dead for %s minutes", timeout)


def do_collectd(config, plugin):
    """
    Output statistics for collectd
    """
    app = config.get_app()
    datasync = app.get_datasync_handler()
    profiles = datasync.get_configured_profiles()
    session = app.make_session()
    model = app.model

    # current time (sanity check)
    now = app.localtime()
    collectd_putval(config, plugin, 'gauge-current_time',
                    now.timestamp(), now=now)

    # iterate watcher profiles
    for key in profiles:

        # last run for watcher
        lastrun = datasync.get_watcher_lastrun(
            key, local=True, tzinfo=True, session=session)
        collectd_putval(config, plugin, f'gauge-{key}_watcher_lastrun',
                        lastrun.timestamp(), now=now)

        # seconds since last run
        collectd_putval(config, plugin, f'gauge-{key}_watcher_seconds_since_lastrun',
                        now.timestamp() - lastrun.timestamp(), now=now)

    # now inspect the change queue..

    # total changes in queue
    total = session.query(model.DataSyncChange).count()
    collectd_putval(config, plugin, 'gauge-queue_changes_total',
                    total, now=now)

    # stale changes in queue
    timeout = config.getint('rattail.datasync',
                            'collectd.changes_stale_timeout',
                            default=15) # minutes
    cutoff = app.make_utc() - datetime.timedelta(seconds=60 * timeout)
    stale = session.query(model.DataSyncChange)\
                   .filter(model.DataSyncChange.obtained < cutoff)\
                   .count()
    collectd_putval(config, plugin, 'gauge-queue_changes_stale',
                    stale, now=now)
    collectd_putval(config, plugin, 'gauge-queue_changes_stale_timeout',
                    timeout, now=now)

    session.close()


def collectd_putval(config, plugin, data_type, value,
                    hostname=None, interval=None, now=None):
    app = config.get_app()
    if not hostname:
        hostname = app.get_collectd_hostname()

    if not interval:
        interval = app.get_collectd_interval()
    if interval:
        interval = ' interval={}'.format(interval)
    else:
        interval = ''

    if now:
        value = '{}:{}'.format(now.timestamp(), value)
    else:
        value = 'N:{}'.format(value)

    msg = 'PUTVAL {}/{}/{}{} {}\n'.format(
        hostname,
        plugin,
        data_type,
        interval,
        value)

    sys.stdout.write(msg)


def do_remove_settings(config):
    """
    Remove all datasync settings from the DB
    """
    from rattail.datasync.util import purge_datasync_settings

    app = config.get_app()
    session = app.make_session()
    purge_datasync_settings(config, session)
    session.commit()
    session.close()


def do_wait(config, timeout):
    app = config.get_app()
    model = app.model
    session = app.make_session()
    started = app.make_utc()
    log.debug("will wait for current change queue to clear")
    last_logged = started

    changes = session.query(model.DataSyncChange)
    count = changes.count()
    log.debug("there are %d changes in the queue", count)
    while count:
        try:
            now = app.make_utc()

            if timeout and (now - started).seconds >= (timeout * 60):
                log.warning("datasync wait timed out after %d minutes, with %d changes in queue",
                            timeout, count)
                sys.exit(1)

            if (now - last_logged).seconds >= 60:
                log.debug("still waiting, %d changes in the datasync queue", count)
                last_logged = now

            time.sleep(1)
            count = changes.count()

        except KeyboardInterrupt:
            sys.stderr.write("Waiting cancelled by user\n")
            session.close()
            sys.exit(1)

    session.close()
    log.debug("all datasync changes have been processed")
