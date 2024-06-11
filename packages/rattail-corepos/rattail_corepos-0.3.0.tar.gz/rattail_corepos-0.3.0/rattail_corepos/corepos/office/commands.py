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
CORE Office commands
"""

import sys

import requests
from requests.auth import HTTPDigestAuth
import typer
from typing_extensions import Annotated

from corepos.enum import CoreDbType

from rattail.commands.typer import (make_typer, typer_eager_imports,
                                    importer_command, typer_get_runas_user,
                                    file_importer_command, file_exporter_command)
from rattail.commands.importing import ImportCommandHandler
from rattail.commands.util import rprint
from rattail_corepos.config import core_office_url
from rattail_corepos.corepos.office.util import get_fannie_config_value, get_blueline_template, make_blueline


core_office_typer = make_typer(
    name='core_office',
    help="core-office -- command line interface for CORE Office"
)


@core_office_typer.command()
def anonymize(
        ctx: typer.Context,
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for CORE POS database engine to be updated.  "
                         "This key must be [corepos.db.office_op] section of your "
                         "config file.")] = 'default',
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through the full motions and allow logging etc. to "
                         "occur, but rollback (abort) the transaction at the end.")] = False,
        force: Annotated[
            bool,
            typer.Option('--force', '-f',
                         help="Do not prompt for confirmation.")] = False,
):
    """
    Make anonymous (randomize) all customer names etc.
    """
    from .anonymize import Anonymizer

    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress

    if not force:
        rprint("\n[bold yellow]**WARNING** this will modify all customer (and similar) records![/bold yellow]")
        value = input("\nreally want to do this? [yN] ")
        if not value or not config.parse_bool(value):
            sys.stderr.write("user canceled\n")
            sys.exit(1)

    try:
        import names
    except ImportError:
        sys.stderr.write("must install the `names` package first!\n\n"
                         "\tpip install names\n")
        sys.exit(2)

    try:
        import us
    except ImportError:
        sys.stderr.write("must install the `us` package first!\n\n"
                         "\tpip install us\n")
        sys.exit(2)

    anonymizer = Anonymizer(config)
    anonymizer.anonymize_all(dbkey=dbkey, dry_run=dry_run,
                             progress=progress)


@core_office_typer.command()
@file_exporter_command
def export_csv(
        ctx: typer.Context,
        **kwargs
):
    """
    Export data from CORE to CSV file(s)
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_csv.from_corepos_db_office_op.export')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'output_dir': kwargs['output_dir']}
    handler.run(kwargs, progress=progress)


@core_office_typer.command()
def get_config_value(
        ctx: typer.Context,
        name: Annotated[
            str,
            typer.Argument(help="Name of the config value to get.  "
                           "Prefix of `FANNIE_` is not required.")] = ...,
):
    """
    Get a value from CORE Office `fannie/config.php`
    """
    config = ctx.parent.rattail_config
    value = get_fannie_config_value(config, name)
    sys.stdout.write(f"{value}\n")


@core_office_typer.command()
@file_importer_command
def import_csv(
        ctx: typer.Context,
        corepos_dbtype: Annotated[
            CoreDbType,
            typer.Option(help="Config *type* for CORE-POS database engine to which data "
                         "should be written.  This determines which config section is "
                         "used with regard to the --corepos-dbkey arg.")] = 'office_op',
        corepos_dbkey: Annotated[
            str,
            typer.Option(help="Config key for CORE-POS database engine to which data should "
                         "be written.  This key must be defined in the config section as "
                         "determined by the --corpos-dbtype arg.")] = 'default',
        **kwargs
):
    """
    Import data from CSV to a CORE Office DB
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_corepos_db_office_op.from_csv.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {
        'input_dir': kwargs['input_dir'],
        'corepos_dbtype': corepos_dbtype,
        'corepos_dbkey': corepos_dbkey,
    }
    handler.run(kwargs, progress=progress)


@core_office_typer.command()
@importer_command
def import_self(
        ctx: typer.Context,
        **kwargs
):
    """
    Import data from CORE Office ("op" DB) to "self"
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_self.from_corepos_db_office_op.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    handler.run(kwargs, progress=progress)


@core_office_typer.command()
def patch_customer_gaps(
        ctx: typer.Context,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Do not POST anything, but log members needing it.")] = False,
):
    """
    POST to the CORE API as needed, to patch gaps for customerID
    """
    from .patcher import CustomerGapPatcher

    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    patcher = CustomerGapPatcher(config)
    patcher.run(dry_run=dry_run, progress=progress)


@core_office_typer.command()
def ping_install(
        ctx: typer.Context,
):
    """
    Ping the /install URL in CORE Office (for DB setup)
    """
    config = ctx.parent.rattail_config
    url = core_office_url(config, require=True)
    url = f'{url}/install/'

    # TODO: hacky re-using credentials from API config..
    username = config.get('corepos.api', 'htdigest.username')
    password = config.get('corepos.api', 'htdigest.password')

    session = requests.Session()
    if username and password:
        session.auth = HTTPDigestAuth(username, password)

    response = session.get(url)
    response.raise_for_status()


# discover more commands
typer_eager_imports(core_office_typer)
