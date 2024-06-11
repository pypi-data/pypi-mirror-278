## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Rattail/${integration_name} commands
"""

from rattail import commands


class Export${integration_studly_prefix}(commands.ExportFileSubcommand):
    """
    Export data to ${integration_name}
    """
    name = 'export-${integration_pkgname}'
    description = __doc__.strip()
    handler_spec = '${pkg_name}.${integration_pkgname}.importing.rattail:FromRattailTo${integration_studly_prefix}'
