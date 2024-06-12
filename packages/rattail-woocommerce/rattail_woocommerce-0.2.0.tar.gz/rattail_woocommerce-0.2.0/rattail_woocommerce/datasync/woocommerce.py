# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
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
DataSync for WooCommerce
"""

from rattail.datasync import FromRattailConsumer


class FromRattailToWooCommerce(FromRattailConsumer):
    """
    Rattail -> WooCommerce datasync consumer
    """
    handler_spec = 'rattail_woocommerce.woocommerce.importing.rattail:FromRattailToWooCommerce'

    def process_changes(self, session, changes):
        """
        Process all the given changes, coming from Rattail.
        """
        # tell session who is responsible here
        if self.runas_username:
            session.set_continuum_user(self.runas_username)

        # get all importers up to speed
        for importer in self.importers.values():
            importer.host_session = session
            importer.datasync_setup()

        # sync all Product changes
        types = [
            'Product',
            'ProductPrice',
        ]
        for change in [c for c in changes if c.payload_type in types]:
            product = self.get_product(session, change)
            if product:
                self.process_change(session, self.importers['Product'],
                                    host_object=product)

    def get_product(self, session, change):
        model = self.model

        if change.payload_type == 'Product':
            return session.get(model.Product, change.payload_key)

        if change.payload_type == 'ProductPrice':
            price = session.get(model.ProductPrice, change.payload_key)
            if price:
                return price.product
