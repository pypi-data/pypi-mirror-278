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
Rattail Commands for MailChimp integration
"""

import typer

from rattail.commands import rattail_typer, ImportSubcommand
from rattail.commands.typer import importer_command, typer_get_runas_user
from rattail.commands.importing import ImportCommandHandler


@rattail_typer.command()
@importer_command
def import_mailchimp(
        ctx: typer.Context,
        **kwargs
):
    """
    Import data to Rattail, from MailChimp API
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_mailchimp.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    handler.run(kwargs, progress=progress)


class ImportMailChimp(ImportSubcommand):
    """
    Import data to Rattail, from MailChimp API
    """
    name = 'import-mailchimp'
    description = __doc__.strip()
    default_handler_spec = 'rattail_mailchimp.importing.mailchimp:FromMailChimpToRattail'

    def get_handler_factory(self, **kwargs):
        if self.config:
            spec = self.config.get('rattail.importing', 'mailchimp.handler',
                                   default=self.default_handler_spec)
        else:
            # just use default, for sake of cmd line help
            spec = self.default_handler_spec
        return self.app.load_object(spec)
