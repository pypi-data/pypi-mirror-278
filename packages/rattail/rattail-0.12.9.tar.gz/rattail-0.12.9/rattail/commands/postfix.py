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
Commands relating to Postfix
"""

import re
import sys
import subprocess
import logging
from pathlib import Path
from typing import List

import typer
from typing_extensions import Annotated

from .base import rattail_typer, Subcommand


log = logging.getLogger(__name__)


@rattail_typer.command()
def postfix_summary(
        ctx: typer.Context,
        email: Annotated[
            bool,
            typer.Option('--email',
                         help="Email the summary instead of displaying it.")] = False,
        problems_only: Annotated[
            bool,
            typer.Option('--problems-only',
                         help="Only show summary if it contains problems.")] = False,
        yesterday: Annotated[
            bool,
            typer.Option('--yesterday',
                         help="Show summary for previous day only.")] = False,
        logfile: Annotated[
            List[Path],
            # nb. we say the file(s) must exist, but not necessariy be
            # readable by current user, since ultimately this runs
            # `sudo pflogsumm` so read access is not a problem
            typer.Option(exists=True,
                         readable=False,
                         help="Path(s) to mail log file(s)")] = ['/var/log/mail.log'],
):
    """
    Generate (and maybe email) a Postfix log summary
    """
    config = ctx.parent.rattail_config
    do_summary(config, ctx.params)


class PostfixSummary(Subcommand):
    """
    Generate (and maybe email) a Postfix log summary
    """
    name = 'postfix-summary'
    description = __doc__.strip()

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--email', action='store_true', default=False,
                            help="Email the summary instead of displaying it.")

        parser.add_argument('--problems-only', action='store_true',
                            help="Only show summary if it contains problems.")

        parser.add_argument('--yesterday', action='store_true',
                            help="Show summary for previous day only.")

        parser.add_argument('logfile', nargs='*', default=['/var/log/mail.log'],
                            help="Path(s) to mail log file(s)")

    def run(self, args):
        params = dict(args._get_kwargs())
        do_dummary(self.config, params)


def do_summary(config, params):
    app = config.get_app()

    # TODO: any way to get around using 'sudo' here?
    cmd = ['sudo', 'pflogsumm', '--problems-first']
    if params['yesterday']:
        cmd.extend(['-d', 'yesterday'])
    cmd.extend(params['logfile'])

    # run cmd
    log.debug("running command: %s", cmd)
    output = subprocess.check_output(cmd).decode('utf_8')

    # parse problem counts
    problems = {}
    pattern = re.compile(r'^ +(\d)   (deferred|bounced|rejected|reject warnings|held|discarded)\b')
    for line in output.split('\n'):
        match = pattern.match(line)
        if match:
            problem = match.group(2)
            if problem in problems:
                log.warning("extra line matches '%s' pattern: %s", problem, line)
            problems[problem] = int(match.group(1))

    log.info("postfix summary contained %s problems",
             sum(problems.values()))

    # bail if caller only wants to see problems and we have none
    if params['problems_only']:
        if not any(problems.values()):
            return

    # just display the summary unless we're to email it
    if params['email']:
        app.send_email('postfix_summary', {
            'output': output,
            'problems': problems,
        })
    else:
        sys.stdout.write(output)
