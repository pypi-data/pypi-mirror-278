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
Rattail -> WooCommerce importing
"""

from collections import OrderedDict

from rattail import importing
from rattail.db import model
from rattail_woocommerce.db.model import WooCacheProduct
from rattail_woocommerce.woocommerce import importing as woocommerce_importing


class FromRattailToWooCommerce(importing.FromRattailHandler):
    """
    Rattail -> WooCommerce import handler
    """
    local_title = "WooCommerce"
    direction = 'export'

    # necessary to save new WooCacheProduct records along the way
    # (since they really are created immediately in Woo via API)
    commit_host_partial = True

    @property
    def host_title(self):
        return self.config.app_title(default="Rattail")

    def get_importers(self):
        importers = OrderedDict()
        importers['Product'] = ProductImporter
        return importers


class FromRattail(importing.FromSQLAlchemy):
    """
    Base class for WooCommerce -> Rattail importers
    """


class ProductImporter(FromRattail, woocommerce_importing.model.ProductImporter):
    """
    Product data importer
    """
    host_model_class = model.Product
    key = 'id'
    supported_fields = [
        'id',
        'name',
        'sku',
        'regular_price',
        'sale_price',
        'date_on_sale_from_gmt',
        'date_on_sale_to_gmt',
    ]

    def setup(self):
        super(ProductImporter, self).setup()
        self.init_woo_id_counter()
        self.establish_cache_importer()

    def datasync_setup(self):
        super(ProductImporter, self).datasync_setup()
        self.init_woo_id_counter()
        self.establish_cache_importer()

    def init_woo_id_counter(self):
        self.next_woo_id = 1

    def establish_cache_importer(self):
        from rattail_woocommerce.importing.woocommerce import WooCacheProductImporter

        # we'll use this importer to update our local cache
        self.cache_importer = WooCacheProductImporter(config=self.config)
        self.cache_importer.session = self.host_session

    def normalize_host_object(self, product):

        woo_id = product.woocommerce_id
        if not woo_id:
            # note, we set to negative to ensure it won't exist but is unique.
            # but we will not actually try to push this value to Woo
            woo_id = -self.next_woo_id
            self.next_woo_id += 1

        regular_price = ''
        if product.regular_price and product.regular_price.price:
            regular_price = '{:0.2f}'.format(product.regular_price.price)

        sale_price = ''
        if product.sale_price and product.sale_price.price:
            sale_price = '{:0.2f}'.format(product.sale_price.price)

        date_on_sale_from_gmt = '1900-01-01T00:00:00'
        if product.sale_price and product.sale_price.starts:
            dt = localtime(self.config, product.sale_price.starts,
                           from_utc=True, zoneinfo=False)
            date_on_sale_from_gmt = dt.isoformat()

        date_on_sale_to_gmt = '1900-01-01T00:00:00'
        if product.sale_price and product.sale_price.starts:
            dt = localtime(self.config, product.sale_price.starts,
                           from_utc=True, zoneinfo=False)
            date_on_sale_to_gmt = dt.isoformat()

        return {
            'id': woo_id,
            'name': (product.description or '').strip().replace('&', '&amp;') or 'Product',
            'sku': product.item_id,
            'regular_price': regular_price,
            'sale_price': sale_price,
            'date_on_sale_from_gmt': date_on_sale_from_gmt,
            'date_on_sale_to_gmt': date_on_sale_to_gmt,
        }

    def create_object(self, key, host_data):

        # push create to API as normal
        api_product = super(ProductImporter, self).create_object(key, host_data)

        # also create local cache record, if running in datasync
        if self.batch_size == 1: # datasync
            self.update_woocache(api_product)

        return api_product

    def update_object(self, api_product, host_data, local_data=None, **kwargs):

        # push update to API as normal
        api_product = super(ProductImporter, self).update_object(api_product, host_data,
                                                                 local_data=local_data,
                                                                 **kwargs)

        # also update local cache record, if running in datasync
        if self.batch_size == 1:
            self.update_woocache(api_product)

        return api_product

    def post_products_batch(self):

        # first post batch to API as normal
        response = super(ProductImporter, self).post_products_batch()
        data = response.json()

        def create_cache(api_product, i):
            self.update_woocache(api_product)

        self.progress_loop(create_cache, data.get('create', []),
                           message="Updating cache for created items")
        self.host_session.flush()

        def update_cache(api_product, i):
            # re-fetch the api_product to make sure we have right info.  for
            # some reason at least one field is represented differently, when
            # we fetch the record vs. how it appears in the batch response.
            api_product = self.api.get('products/{}'.format(api_product['id']))\
                                  .json()
            self.update_woocache(api_product)

        self.progress_loop(update_cache, data.get('update', []),
                           message="Updating cache for updated items")
        self.host_session.flush()

        return response

    def update_woocache(self, api_product):

        # normalize data and process importer update
        normal = self.cache_importer.normalize_host_object(api_product)
        key = self.cache_importer.get_key(normal)
        cache_product = self.cache_importer.get_local_object(key)
        if cache_product:
            cache_normal = self.cache_importer.normalize_local_object(cache_product)
            cache_product = self.cache_importer.update_object(
                cache_product, normal, local_data=cache_normal)
        else:
            cache_product = self.cache_importer.create_object(key, normal)

        # update cached woo_id too, if we can
        self.host_session.flush()
        if cache_product and cache_product.product:
            product = cache_product.product
            if product.woocommerce_id != api_product['id']:
                product.woocommerce_id = api_product['id']
