# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
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
WooCommerce model importers
"""

from woocommerce import API as WooAPI

from rattail import importing
from rattail_woocommerce.woocommerce.util import get_woocommerce_products


class ToWooCommerce(importing.Importer):
    pass


class ProductImporter(ToWooCommerce):
    """
    WooCommerce product data importer
    """
    model_name = 'Product'
    key = 'sku'
    supported_fields = [
        'id',
        'name',
        'slug',
        'permalink',
        'date_created',
        'date_created_gmt',
        'date_modified',
        'date_modified_gmt',
        'type',
        'status',
        'featured',
        'catalog_visibility',
        'description',
        'short_description',
        'sku',
        'price',
        'regular_price',
        'sale_price',
        'date_on_sale_from',
        'date_on_sale_from_gmt',
        'date_on_sale_to',
        'date_on_sale_to_gmt',
        'price_html',
        'on_sale',
        'purchasable',
        'total_sales',
        'tax_status',
        'tax_class',
        'manage_stock',
        'stock_quantity',
        'stock_status',
        'backorders',
        'backorders_allowed',
        'backordered',
        'sold_individually',
        'weight',
        'reviews_allowed',
        'parent_id',
        'purchase_note',
        'menu_order',
    ]

    caches_local_data = True

    # TODO: would be nice to just set this here, but command args will always
    # overwrite, b/c that defaults to 200 even when not specified by user
    #batch_size = 100

    def setup(self):
        super(ProductImporter, self).setup()
        self.establish_api()
        self.to_be_created = []
        self.to_be_updated = []

    def datasync_setup(self):
        super(ProductImporter, self).datasync_setup()
        self.establish_api()
        self.batch_size = 1

    def establish_api(self):
        kwargs = {
            'url': self.config.require('woocommerce', 'url'),
            'consumer_key': self.config.require('woocommerce', 'api_consumer_key'),
            'consumer_secret': self.config.require('woocommerce', 'api_consumer_secret'),
            'version': 'wc/v3',
            'timeout': 30,
        }
        self.api = WooAPI(**kwargs)

    def cache_local_data(self, host_data=None):
        """
        Fetch existing products from WooCommerce.
        """
        cache = {}
        for product in get_woocommerce_products(self.api):
            data = self.normalize_local_object(product)
            normal = self.normalize_cache_object(product, data)
            key = self.get_cache_key(product, normal)
            cache[key] = normal
        return cache

    def get_single_local_object(self, key):
        assert self.key == ('id',)
        woo_id = key[0]
        # note, we avoid negative id here b/c that trick is used elsewhere
        if woo_id > 0:
            response = self.api.get('products/{}'.format(key[0]))
            return response.json()

    def normalize_local_object(self, api_product):
        return dict(api_product)

    def create_object(self, key, host_data):
        data = dict(host_data)
        data.pop('id', None)

        if self.batch_size == 1: # datasync
            if self.dry_run:
                return data
            response = self.api.post('products', data)
            return response.json()

        # collect data to be posted later
        self.to_be_created.append(data)
        return data

    def update_object(self, api_product, host_data, local_data=None, all_fields=False):

        if self.batch_size == 1: # datasync
            if self.dry_run:
                return host_data
            response = self.api.post('products/{}'.format(api_product['id']), host_data)
            return response.json()

        # collect data to be posted later
        self.to_be_updated.append(host_data)
        return host_data

    def flush_create_update(self):
        if not self.dry_run and self.batch_size > 1: # not datasync
            self.post_products_batch()

    def post_products_batch(self):
        """
        Push pending create/update data batch to WooCommerce API.
        """
        assert not self.dry_run
        response = self.api.post('products/batch', {'create': self.to_be_created,
                                                    'update': self.to_be_updated})
        # clear the pending lists, since we've now pushed that data
        self.to_be_created = []
        self.to_be_updated = []
        return response

    def delete_object(self, api_product):
        if self.dry_run:
            return True

        raise NotImplementedError
