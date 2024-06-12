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
Rattail/WooCommerce Commands
"""

import typer

from rattail.commands import rattail_typer, ImportSubcommand
from rattail.commands.typer import importer_command, typer_get_runas_user
from rattail.commands.importing import ImportCommandHandler


@rattail_typer.command()
@importer_command
def export_woocommerce(
        ctx: typer.Context,
        **kwargs
):
    """
    Export data to WooCommerce
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config,
        import_handler_spec='rattail_woocommerce.woocommerce.importing.rattail:FromRattailToWooCommerce')
    kwargs['user'] = typer_get_runas_user(ctx)
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@importer_command
def import_woocommerce(
        ctx: typer.Context,
        **kwargs
):
    """
    Import data from WooCommerce
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config,
        import_handler_spec='rattail_woocommerce.importing.woocommerce:FromWooCommerceToRattail')
    kwargs['user'] = typer_get_runas_user(ctx)
    handler.run(kwargs, progress=progress)


class ExportWooCommerce(ImportSubcommand):
    """
    Export data to WooCommerce
    """
    name = 'export-woocommerce'
    description = __doc__.strip()
    handler_spec = 'rattail_woocommerce.woocommerce.importing.rattail:FromRattailToWooCommerce'


class ImportWooCommerce(ImportSubcommand):
    """
    Import data from WooCommerce
    """
    name = 'import-woocommerce'
    description = __doc__.strip()
    handler_spec = 'rattail_woocommerce.importing.woocommerce:FromWooCommerceToRattail'
