# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
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
Rattail -> Rattail "versions" data import
"""

from rattail.importing import versions as base
from rattail_woocommerce.db import model


class WooVersionMixin(object):
    """
    Add default registration of custom importers
    """

    def add_woocommerce_importers(self, importers):
        importers['WooProductExtension'] = WooProductExtensionImporter
        importers['WooCacheProduct'] = WooCacheProductImporter
        return importers


class WooProductExtensionImporter(base.VersionImporter):
    host_model_class = model.WooProductExtension

class WooCacheProductImporter(base.VersionImporter):
    host_model_class = model.WooCacheProduct
