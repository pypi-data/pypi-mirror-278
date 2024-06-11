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
CORE-POS commands
"""

import typer
from typing_extensions import Annotated

from rattail.commands.typer import make_typer, importer_command, typer_get_runas_user
from rattail.commands.importing import ImportCommandHandler



crepes_typer = make_typer(
    name='crepes',
    help="Crepes -- command line interface for CORE-POS"
)


@crepes_typer.command()
@importer_command
def export_core(
        ctx: typer.Context,
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for database engine to be used as the \"target\" "
                         "CORE DB, i.e. where data will be exported.  This key must be "
                         "defined in the [rattail_corepos.db] section of your config file.")] = 'host',
        **kwargs
):
    """
    Export data to another CORE database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_corepos_db_office_op.from_corepos_db_office_op.export')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'dbkey': dbkey}
    handler.run(kwargs, progress=progress)


@crepes_typer.command()
@importer_command
def import_core(
        ctx: typer.Context,
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for database engine to be used as the CORE "
                         "\"host\", i.e. the source of the data to be imported.  This key "
                         "must be defined in the [rattail_corepos.db] section of your "
                         "config file.")] = 'host',
        **kwargs
):
    """
    Import data from another CORE database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_corepos_db_office_op.from_corepos_db_office_op.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'dbkey': dbkey}
    handler.run(kwargs, progress=progress)
