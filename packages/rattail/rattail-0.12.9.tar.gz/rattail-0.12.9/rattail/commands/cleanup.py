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
Cleanup commands
"""

import typer
from typing_extensions import Annotated

from .base import rattail_typer, Subcommand, date_argument


@rattail_typer.command()
def cleanup(
        ctx: typer.Context,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through motions and log actions but do not "
                         "actually commit the results.")] = False,
):
    """
    Cleanup by removing older data etc.
    """
    from rattail.db.util import finalize_session

    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    app = config.get_app()
    handler = app.get_cleanup_handler()
    session = app.make_session()
    handler.cleanup_everything(session, dry_run=dry_run, progress=progress)
    finalize_session(session, dry_run=dry_run)


class Cleanup(Subcommand):
    """
    Cleanup by removing older data etc.
    """
    name = 'cleanup'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help="Go through motions and log actions but do not "
                            "actually commit the results.")

    def run(self, args):
        self.cleanup_handler = self.app.get_cleanup_handler()
        session = self.make_session()
        self.cleanup_handler.cleanup_everything(session,
                                                dry_run=args.dry_run,
                                                progress=self.progress)
        self.finalize_session(session, dry_run=args.dry_run)
