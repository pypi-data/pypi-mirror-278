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
Rattail Commands
"""

import typer
from typing_extensions import Annotated

from corepos.enum import CoreDbType

from rattail.commands import rattail_typer
from rattail.commands.typer import importer_command, file_importer_command, typer_get_runas_user
from rattail.commands.importing import (ImportSubcommand, ImportFileSubcommand,
                                        ImportCommandHandler)


@rattail_typer.command()
@file_importer_command
def corepos_import_square(
        ctx: typer.Context,
        **kwargs
):
    """
    Import transaction data from Square into CORE
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_corepos_db_office_trans.from_square_csv.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@importer_command
def export_corepos(
        ctx: typer.Context,
        **kwargs
):
    """
    Export data from Rattail to CORE-POS
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_corepos_api.from_rattail.export')
    kwargs['user'] = typer_get_runas_user(ctx)
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@importer_command
def import_corepos_api(
        ctx: typer.Context,
        **kwargs
):
    """
    Import data from a CORE POS API
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_corepos_api.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@importer_command
def import_corepos_db(
        ctx: typer.Context,
        corepos_dbtype: Annotated[
            CoreDbType,
            typer.Option(help="Type of CORE-POS DB engine to be used as data host.  "
                         "This determines which config section is used with regard "
                         "to the --corepos-dbkey arg.")] = 'office_op',
        corepos_dbkey: Annotated[
            str,
            typer.Option(help="Config key for CORE POS database engine to be used as "
                         "the \"host\", i.e. the source of the data to be imported.  "
                         "This key must be defined in the [rattail_corepos.db] section "
                         "of your config file.")] = 'default',
        **kwargs
):
    """
    Import data from a CORE POS database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_corepos_db_office_op.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {
        'corepos_dbtype': corepos_dbtype,
        'corepos_dbkey': corepos_dbkey,
    }
    handler.run(kwargs, progress=progress)


class ExportCore(ImportSubcommand):
    """
    Export data from Rattail to CORE-POS
    """
    name = 'export-corepos'
    description = __doc__.strip()
    handler_key = 'to_corepos_api.from_rattail.export'


class ImportCOREPOSAPI(ImportSubcommand):
    """
    Import data from a CORE POS API
    """
    name = 'import-corepos-api'
    description = __doc__.strip()
    handler_key = 'to_rattail.from_corepos_api.import'


class ImportCOREPOSDB(ImportSubcommand):
    """
    Import data from a CORE POS database
    """
    name = 'import-corepos-db'
    description = __doc__.strip()
    handler_key = 'to_rattail.from_corepos_db_office_op.import'

    def add_parser_args(self, parser):
        super().add_parser_args(parser)

        parser.add_argument('--corepos-dbtype', metavar='TYPE', default='office_op',
                            choices=['office_op', 'office_trans'],
                            help="Config *type* for CORE-POS database engine to be used as "
                            "host.  Default type is 'office_op' - this determines which "
                            "config section is used with regard to the --corepos-dbkey arg.")

        parser.add_argument('--corepos-dbkey', metavar='KEY', default='default',
                            help="Config key for CORE POS database engine to be used as the \"host\", "
                            "i.e. the source of the data to be imported.  This key " "must be "
                            "defined in the [rattail_corepos.db] section of your config file.  "
                            "Defaults to 'default'.")

    def get_handler_kwargs(self, **kwargs):
        if 'args' in kwargs:
            kwargs['corepos_dbtype'] = kwargs['args'].corepos_dbtype
            kwargs['corepos_dbkey'] = kwargs['args'].corepos_dbkey
        return kwargs


class CoreImportSquare(ImportFileSubcommand):
    """
    Import transaction data from Square into CORE
    """
    name = 'corepos-import-square'
    description = __doc__.strip()
    handler_key = 'to_corepos_db_office_trans.from_square_csv.import'
