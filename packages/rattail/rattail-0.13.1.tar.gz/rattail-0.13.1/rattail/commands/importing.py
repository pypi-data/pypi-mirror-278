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
Importing Commands
"""

import datetime
import sys
import logging

import typer
from typing_extensions import Annotated
from wuttjamaican.util import parse_list

from rattail.app import GenericHandler
from .base import rattail_typer, Subcommand, date_argument
from .typer import (typer_get_runas_user, importer_command,
                    file_importer_command, file_exporter_command)


log = logging.getLogger(__name__)


class ImportCommandHandler(GenericHandler):
    """
    Responsible for handling import/export command line runs.
    """

    def __init__(self, config, import_handler_key=None, import_handler_spec=None, **kwargs):
        super().__init__(config, **kwargs)

        if not import_handler_key and not import_handler_spec:
            raise ValueError("must provide either import_handler_key or import_handler_spec")

        self.import_handler_key = import_handler_key
        self.import_handler_spec = import_handler_spec

    def run(self, params, progress=None):

        if params['list_all_models']:
            self.list_all_models(params)
            return

        if params['list_default_models']:
            self.list_default_models(params)
            return

        handler = self.get_handler(params)
        models = params['models'] or handler.get_default_keys()
        log.debug("using handler: %s", handler)
        log.debug("importing models: %s", models)
        log.debug("params are: %s", params)

        kwargs = {
            'warnings': params['warnings'],
            'fields': parse_list(params['fields']),
            'exclude_fields': parse_list(params['exclude_fields']),
            'fuzzy_fields': parse_list(params['fuzzy_fields']),
            'fuzz_factor': params['fuzz_factor'],
            'create': params['create'],
            'max_create': params['max_create'],
            'update': params['update'],
            'max_update': params['max_update'],
            'delete': params['delete'],
            'max_delete': params['max_delete'],
            'max_total': params['max_total'],
            'start_date': params['start_date'],
            'end_date': params['end_date'],
            'progress': progress,
        }

        # ensure we have dates here, not datetime
        if kwargs['start_date'] and isinstance(kwargs['start_date'], datetime.datetime):
            kwargs['start_date'] = kwargs['start_date'].date()
        if kwargs['end_date'] and isinstance(kwargs['end_date'], datetime.datetime):
            kwargs['end_date'] = kwargs['end_date'].date()

        if params['make_batches']:
            kwargs.update({
                'runas_user': params['user'],
            })
            handler.make_batches(*models, **kwargs)
        else:
            kwargs.update({
                'key_fields': parse_list(params['key']) if params['key'] else None,
                'dry_run': params['dry_run'],
            })
            handler.import_data(*models, **kwargs)

        # TODO: should this logging happen elsewhere / be customizable?
        if params['dry_run']:
            log.info("dry run, so transaction was rolled back")
        else:
            log.info("transaction was committed")

    def get_handler_factory(self, params, **kwargs):
        """
        Should return an ImportHandler factory (e.g. class) which will
        later be called to create a handler instance.
        """
        # use explicit spec if one was provided
        if self.import_handler_spec:
            return self.app.load_object(self.import_handler_spec)

        # otherwise lookup the handler based on key
        # nb. normal logic returns an instance but we want its class
        handler = self.app.get_import_handler(self.import_handler_key, require=True)
        return type(handler)

    def get_handler(self, params, **kwargs):
        """
        Returns a handler instance to be used by the command.
        """
        factory = self.get_handler_factory(params)
        user = params['user']
        if user:
            kwargs.setdefault('runas_user', user)
            kwargs.setdefault('runas_username', user.username)
        kwargs.setdefault('dry_run', params['dry_run'])
        kwargs.setdefault('collect_changes_for_processing', params['collect_changes'])
        kwargs.setdefault('batch_size', params['batch_size'])
        if params['max_diffs']:
            kwargs.setdefault('diff_max_display', params['max_diffs'])
        if params.get('handler_kwargs'):
            kwargs.update(params['handler_kwargs'])
        return factory(self.config, **kwargs)

    def list_all_models(self, params):
        handler = self.get_handler(params)
        if not handler:
            sys.stderr.write("no handler configured!\n")
            if self.import_handler_key:
                sys.stderr.write(f"handler key is: {self.import_handler_key}\n")
            sys.exit(1)
        sys.stdout.write("ALL MODELS:\n")
        sys.stdout.write("==============================\n")
        defaults = handler.get_default_keys()
        for key in handler.get_importer_keys():
            sys.stdout.write(key)
            if key in defaults:
                sys.stdout.write(" (*)")
            sys.stdout.write("\n")
        sys.stdout.write("==============================\n")
        sys.stdout.write("(*) means also default\n")

    def list_default_models(self, params):
        handler = self.get_handler(params)
        sys.stdout.write("DEFAULT MODELS:\n")
        sys.stdout.write("==============================\n")
        for key in handler.get_default_keys():
            sys.stdout.write(f"{key}\n")


@rattail_typer.command()
@file_exporter_command
def export_csv(
        ctx: typer.Context,
        **kwargs
):
    """
    Export data from Rattail to CSV file(s)
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_csv.from_rattail.export')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'output_dir': kwargs['output_dir']}
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@importer_command
def export_rattail(
        ctx: typer.Context,
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for database engine to be used as the \"target\" "
                         "Rattail system, i.e. where data will be exported.  This key must "
                         "be defined in the [rattail.db] section of your config file.")] = 'host',
        **kwargs
):
    """
    Export data to another Rattail database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_rattail.export')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'dbkey': dbkey}
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@file_importer_command
def import_csv(
        ctx: typer.Context,
        **kwargs
):
    """
    Import data from CSV file(s) to Rattail database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_csv.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'input_dir': kwargs['input_dir']}
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@file_importer_command
def import_ifps(
        ctx: typer.Context,
        **kwargs
):
    """
    Import data from IFPS file(s) to Rattail database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_ifps.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'input_dir': kwargs['input_dir']}
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@importer_command
def import_rattail(
        ctx: typer.Context,
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for database engine to be used as the Rattail "
                         "\"host\", i.e. the source of the data to be imported.  This key "
                         "must be defined in the [rattail.db] section of your config file.  "
                         "Defaults to 'host'.")] = 'host',
        **kwargs
):
    """
    Import data from another Rattail database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_rattail.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'dbkey': dbkey}
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@importer_command
def import_versions(
        ctx: typer.Context,
        comment: Annotated[
            str,
            typer.Option('--comment', '-m',
                         help="Comment to be recorded with the transaction."
                         )] = "import catch-up versions",
        **kwargs
):
    """
    Make initial versioned records for data models
    """
    config = ctx.parent.rattail_config

    if not config.versioning_has_been_enabled:
        sys.stderr.write("Continuum versioning is not enabled, "
                         "per config and/or command line args\n")
        sys.exit(1)

    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail_versions.from_rattail.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'comment': comment}
    handler.run(kwargs, progress=progress)


class ImportSubcommand(Subcommand):
    """
    Base class for subcommands which use the (new) data importing system.
    """
    handler_key = None
    handler_spec = None

    def __init__(self, *args, **kwargs):
        if 'handler_spec' in kwargs:
            self.handler_spec = kwargs.pop('handler_spec')
        super().__init__(*args, **kwargs)

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        # model names (aka importer keys)
        doc = ("Which data models to import.  If you specify any, then only "
               "data for those models will be imported.  If you do not specify "
               "any, then all *default* models will be imported.")
        parser.add_argument('models', nargs='*', metavar='MODEL', help=doc)

        # list models
        parser.add_argument('--list-all-models', '-l', action='store_true',
                            help="List all available models and exit.")
        parser.add_argument('--list-default-models', action='store_true',
                            help="List the default models and exit.")

        # make batches
        parser.add_argument('--make-batches', action='store_true',
                            help="If specified, make new Import / Export Batches instead of "
                            "performing an actual (possibly dry-run) import.")

        # key / fields / exclude
        parser.add_argument('--key', metavar='FIELDS',
                            help="List of fields which should be used as \"primary key\" for the import.")
        parser.add_argument('--fields',
                            help="List of fields which should be included in the import.  "
                            "If this parameter is specified, then any field not listed here, "
                            "would be *excluded* regardless of the --exclude-field parameter.")
        parser.add_argument('--exclude-fields',
                            help="List of fields which should be excluded from the import.  "
                            "Any field not listed here, would be included (or not) depending "
                            "on the --fields parameter and/or default importer behavior.")
        parser.add_argument('--fuzzy-fields',
                            help="List of fields for which diff comparison should "
                            "be \"fuzzy\".  This is intended for timestamps and similar "
                            "values which vary in granularity between systems.")
        parser.add_argument('--fuzz-factor', type=int, default=1,
                            help="Numeric value for use with --fuzzy-fields.  For "
                            "timestamp fields, this refers to the number of seconds "
                            "by which values are allowed to differ and still be "
                            "considered a match.  Default fuzz factor is 1.")

        # date ranges
        parser.add_argument('--start-date', type=date_argument, metavar='DATE',
                            help="Optional (inclusive) starting point for date range, by which host "
                            "data should be filtered.  Only used by certain importers.")
        parser.add_argument('--end-date', type=date_argument, metavar='DATE',
                            help="Optional (inclusive) ending point for date range, by which host "
                            "data should be filtered.  Only used by certain importers.")
        parser.add_argument('--year', type=int,
                            help="Optional year, by which data should be filtered.  Only used "
                            "by certain importers.")

        # allow create?
        parser.add_argument('--create', action='store_true', default=True,
                            help="Allow new records to be created during the import.")
        parser.add_argument('--no-create', action='store_false', dest='create',
                            help="Do not allow new records to be created during the import.")
        parser.add_argument('--max-create', type=int, metavar='COUNT',
                            help="Maximum number of records which may be created, after which a "
                            "given import task should stop.  Note that this applies on a per-model "
                            "basis and not overall.")

        # allow update?
        parser.add_argument('--update', action='store_true', default=True,
                            help="Allow existing records to be updated during the import.")
        parser.add_argument('--no-update', action='store_false', dest='update',
                            help="Do not allow existing records to be updated during the import.")
        parser.add_argument('--max-update', type=int, metavar='COUNT',
                            help="Maximum number of records which may be updated, after which a "
                            "given import task should stop.  Note that this applies on a per-model "
                            "basis and not overall.")

        # allow delete?
        parser.add_argument('--delete', action='store_true', default=False,
                            help="Allow records to be deleted during the import.")
        parser.add_argument('--no-delete', action='store_false', dest='delete',
                            help="Do not allow records to be deleted during the import.")
        parser.add_argument('--max-delete', type=int, metavar='COUNT',
                            help="Maximum number of records which may be deleted, after which a "
                            "given import task should stop.  Note that this applies on a per-model "
                            "basis and not overall.")

        # collect changes for processing
        parser.add_argument('--collect-changes', action='store_true', default=True,
                            help="Collect changes along the way, for processing "
                            "at the end of the run.  This is on by default as it "
                            "is required for reporting how many changes occurred, "
                            "as well as being used for diff warning emails.")
        parser.add_argument('--no-collect-changes', action='store_false', dest='collect_changes',
                            help="Do *not* collect changes for processing at the "
                            "end of the run.  The main reason for this flag is to "
                            "cut down on memory usage during the run, but it will "
                            "cause the final tally reporting not to work.")

        # max total changes, per model
        parser.add_argument('--max-total', type=int, metavar='COUNT',
                            help="Maximum number of *any* record changes which may occur, after which "
                            "a given import task should stop.  Note that this applies on a per-model "
                            "basis and not overall.")

        # TODO: deprecate --batch, replace with --batch-size ?
        # batch size
        parser.add_argument('--batch', type=int, dest='batch_size', metavar='SIZE', default=200,
                            help="Split work to be done into batches, with the specified number of "
                            "records in each batch.  Or, set this to 0 (zero) to disable batching. "
                            "Implementation for this may vary somewhat between importers; default "
                            "batch size is 200 records.")

        # treat changes as warnings?
        parser.add_argument('--warnings', '-W', action='store_true',
                            help="Set this flag if you expect a \"clean\" import, and wish for any "
                            "changes which do occur to be processed further and/or specially.  The "
                            "behavior of this flag is ultimately up to the import handler, but the "
                            "default is to send an email notification.")

        # max diffs per warning type
        parser.add_argument('--max-diffs', type=int, metavar='COUNT',
                            help="Maximum number of \"diffs\" to display per warning type, in a "
                            "warning email.  Only used if --warnings is in effect.")

        # dry run?
        parser.add_argument('--dry-run', action='store_true',
                            help="Go through the full motions and allow logging etc. to "
                            "occur, but rollback (abort) the transaction at the end.  "
                            "Note that this flag is ignored if --make-batches is specified.")

    def run(self, args):
        handler = ImportCommandHandler(self.config,
                                       import_handler_key=self.handler_key,
                                       import_handler_spec=self.handler_spec)
        params = dict(args._get_kwargs())
        params['user'] = self.get_runas_user()
        params['handler_kwargs'] = self.get_handler_kwargs(args=args)
        handler.run(params, progress=self.progress)

    def get_handler_kwargs(self, **kwargs):
        """
        Return a dict of kwargs to be passed to the handler factory.
        """
        return kwargs


# TODO: deprecate / remote this, use ImportFileSubcommand instead
class ImportFromCSV(ImportSubcommand):
    """
    Generic base class for commands which import from a CSV file.
    """

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--source-csv', metavar='PATH', required=True,
                            help="Path to CSV file to be used as data source.")


class ImportFileSubcommand(ImportSubcommand):
    """
    Base class for import commands which use data file(s) as source
    """

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--input-dir', metavar='PATH', required=True,
                            help="Directory from which input files should be read.  "
                            "Note that this is a *required* parameter.")

    def get_handler_kwargs(self, **kwargs):
        kwargs = super().get_handler_kwargs(**kwargs)

        if 'args' in kwargs:
            args = kwargs['args']
            kwargs['input_dir'] = args.input_dir

        return kwargs


class ImportCSV(ImportFileSubcommand):
    """
    Import data from CSV file(s) to Rattail database
    """
    name = 'import-csv'
    description = __doc__.strip()
    handler_key = 'to_rattail.from_csv.import'


class ImportIFPS(ImportFileSubcommand):
    """
    Import data from IFPS file(s) to Rattail database
    """
    name = 'import-ifps'
    description = __doc__.strip()
    handler_key = 'to_rattail.from_ifps.import'


class ExportFileSubcommand(ImportSubcommand):
    """
    Base class for export commands which target data file(s)
    """

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--output-dir', metavar='PATH', required=True,
                            help="Directory to which output files should be written.  "
                            "Note that this is a *required* parameter.")

    def get_handler_kwargs(self, **kwargs):
        kwargs = super().get_handler_kwargs(**kwargs)

        if 'args' in kwargs:
            args = kwargs['args']
            kwargs['output_dir'] = args.output_dir

        return kwargs


class ExportCSV(ExportFileSubcommand):
    """
    Export data from Rattail to CSV file(s)
    """
    name = 'export-csv'
    description = __doc__.strip()
    handler_key = 'to_csv.from_rattail.export'


class ExportRattail(ImportSubcommand):
    """
    Export data to another Rattail database
    """
    name = 'export-rattail'
    description = __doc__.strip()
    handler_key = 'to_rattail.from_rattail.export'
    default_dbkey = 'host'

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--dbkey', metavar='KEY', default=self.default_dbkey,
                            help="Config key for database engine to be used as the \"target\" "
                            "Rattail system, i.e. where data will be exported.  This key must "
                            "be defined in the [rattail.db] section of your config file.")

    def get_handler_kwargs(self, **kwargs):
        if 'args' in kwargs:
            kwargs['dbkey'] = kwargs['args'].dbkey
        return kwargs


class ImportToRattail(ImportSubcommand):
    """
    Generic base class for commands which import *to* a Rattail system.
    """


class ImportRattail(ImportToRattail):
    """
    Import data from another Rattail database
    """
    name = 'import-rattail'
    description = __doc__.strip()
    handler_key = 'to_rattail.from_rattail.import'
    accepts_dbkey_param = True

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        if self.accepts_dbkey_param:
            parser.add_argument('--dbkey', metavar='KEY', default='host',
                                help="Config key for database engine to be used as the Rattail "
                                "\"host\", i.e. the source of the data to be imported.  This key "
                                "must be defined in the [rattail.db] section of your config file.  "
                                "Defaults to 'host'.")

    def get_handler_kwargs(self, **kwargs):
        if self.accepts_dbkey_param:
            if 'args' in kwargs:
                kwargs['dbkey'] = kwargs['args'].dbkey
        return kwargs


# nb. this command is being phased out! no equivalent in typer
class ImportRattailBulk(ImportRattail):
    """
    Bulk-import data from another Rattail database
    """
    name = 'import-rattail-bulk'
    description = __doc__.strip()
    handler_key = 'to_rattail.from_rattail_bulk.import'


# nb. this command is being phased out! no equivalent in typer
class ImportSampleData(ImportToRattail):
    """
    Import sample data to a Rattail database
    """
    name = 'import-sample'
    description = __doc__.strip()
    handler_key = 'to_rattail.from_sample.import'


class ImportVersions(ImportRattail):
    """
    Make initial versioned records for data models
    """
    name = 'import-versions'
    description = __doc__.strip()
    handler_key = 'to_rattail_versions.from_rattail.import'
    accepts_dbkey_param = False
    default_comment = "import catch-up versions"

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--comment', '-m', type=str, default=self.default_comment,
                            help="Comment to be recorded with the transaction.  "
                            "Default is \"{}\".".format(self.default_comment))

    def get_handler_kwargs(self, **kwargs):
        if 'args' in kwargs:
            kwargs['comment'] = kwargs['args'].comment
        return kwargs

    def run(self, args):
        if not self.config.versioning_has_been_enabled:
            self.stderr.write("Continuum versioning is not enabled, "
                              "per config and/or command line args\n")
            sys.exit(1)
        super().run(args)
