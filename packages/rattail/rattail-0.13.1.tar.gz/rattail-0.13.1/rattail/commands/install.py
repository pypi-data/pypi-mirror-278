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
Installer Commands
"""

import warnings

from rattail.commands import Subcommand
from rattail.mako import ResourceTemplateLookup


class InstallSubcommand(Subcommand):
    """
    Base class and default implementation for ``poser install``
    commands.  Note that there is no ``rattail install`` command.
    """
    name = 'install'
    install_handler_spec = 'rattail.install:InstallHandler'

    # nb. these must be explicitly set b/c config is not available
    # when running normally, e.g. `poser -n install`
    #app_title = "Poser"
    #app_package = 'poser'
    #app_eggname = 'Poser'
    #app_pypiname = 'Poser'

    def run(self, args):
        factory = self.app.load_object(self.install_handler_spec)
        handler = factory(self.config,
                          app_title=self.app_title,
                          app_package=self.app_package,
                          app_eggname=self.app_eggname,
                          app_pypiname=self.app_pypiname)
        handler.run()


class InstallerTemplateLookup(ResourceTemplateLookup):
    def __init__(self, *args, **kwargs):
        warnings.warn("InstallerTemplateLookup is deprecated; "
                      "please use ResourceTemplateLookup instead",
                      DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)
