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
WooCommerce -> Rattail data import
"""

import datetime
from collections import OrderedDict

from sqlalchemy import orm

from woocommerce import API as WooAPI

from rattail import importing
from rattail.core import get_uuid
from rattail.time import localtime, make_utc
from rattail_woocommerce import importing as rattail_woocommerce_importing
from rattail_woocommerce.woocommerce.util import get_woocommerce_products


class FromWooCommerceToRattail(importing.ToRattailHandler):
    """
    Handler for WooCommerce -> Rattail
    """
    host_title = "WooCommerce"

    def get_importers(self):
        importers = OrderedDict()
        importers['Product'] = ProductImporter
        importers['WooCacheProduct'] = WooCacheProductImporter
        return importers


class FromWooCommerce(importing.Importer):

    def setup(self):
        super(FromWooCommerce, self).setup()

        kwargs = {
            'url': self.config.require('woocommerce', 'url'),
            'consumer_key': self.config.require('woocommerce', 'api_consumer_key'),
            'consumer_secret': self.config.require('woocommerce', 'api_consumer_secret'),
            'version': 'wc/v3',
        }

        timeout = self.config.getint('woocommerce', 'api_timeout')
        if timeout:
            kwargs['timeout'] = timeout

        self.api = WooAPI(**kwargs)


class ProductImporter(FromWooCommerce, rattail_woocommerce_importing.model.ProductImporter):
    """
    Importer for product data from WooCommerce.
    """
    key = 'uuid'
    supported_fields = [
        'uuid',
        'woocommerce_id',
        'item_id',
        'description',
    ]

    def setup(self):
        super(ProductImporter, self).setup()
        model = self.model

        query = self.session.query(model.Product)\
                            .join(model.WooProductExtension)\
                            .options(orm.joinedload(model.Product._woocommerce))
        self.products_by_woo_id = self.cache_model(model.Product,
                                                   key='woocommerce_id',
                                                   query=query)

        query = self.session.query(model.Product)\
                            .filter(model.Product.item_id != None)
        self.products_by_item_id = self.cache_model(model.Product,
                                                    key='item_id',
                                                    query=query)

    def get_host_objects(self):
        return get_woocommerce_products(self.api)

    def find_rattail_product(self, api_product):
        product = self.get_product_by_woo_id(api_product['id'])
        if product:
            return product

        if api_product['sku']:
            return self.get_product_by_item_id(api_product['sku'])

    def get_product_by_woo_id(self, woo_id):
        if hasattr(self, 'products_by_woo_id'):
            return self.products_by_woo_id.get(woo_id)

        model = self.model
        try:
            return self.session.query(model.Product)\
                               .join(model.WooProductExtension)\
                               .filter(model.WooProductExtension.id == woo_id)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def get_product_by_item_id(self, item_id):
        if hasattr(self, 'products_by_item_id'):
            return self.products_by_item_id.get(item_id)

        model = self.model
        try:
            return self.session.query(model.Product)\
                               .filter(model.Product.item_id == item_id)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def normalize_host_object(self, api_product):
        product = self.find_rattail_product(api_product)
        if product:
            uuid = product.uuid
        else:
            uuid = get_uuid()

        return {
            'uuid': uuid,
            'woocommerce_id': api_product['id'],
            'item_id': api_product['sku'],
            'description': api_product['name'].replace('&amp;', '&'),
        }


class WooCacheProductImporter(FromWooCommerce, rattail_woocommerce_importing.model.WooCacheProductImporter):
    """
    WooCommerce Product -> WooCacheProduct
    """
    key = 'id'
    supported_fields = [
        'id',
        'product_uuid',
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

    # declare which fields are 'date' type, so can treat specially
    date_fields = [
        'date_created',
        'date_created_gmt',
        'date_modified',
        'date_modified_gmt',
        'date_on_sale_from',
        'date_on_sale_from_gmt',
        'date_on_sale_to',
        'date_on_sale_to_gmt',
    ]

    def setup(self):
        super(WooCacheProductImporter, self).setup()
        model = self.model

        query = self.session.query(model.Product)\
                            .filter(model.Product.item_id != None)
        self.products_by_item_id = self.cache_model(model.Product,
                                                    key='item_id', query=query)

        query = self.session.query(model.WooCacheProduct)\
                            .options(orm.joinedload(model.WooCacheProduct.product))
        self.woo_cache_by_id = self.cache_model(model.WooCacheProduct,
                                                key='id', query=query)

    def find_rattail_product(self, api_product):
        woo_product = self.get_woo_product_by_id(api_product['id'])
        if woo_product and woo_product.product:
            return woo_product.product

        return self.get_product_by_item_id(api_product['sku'])

    def get_woo_product_by_id(self, woo_id):
        if hasattr(self, 'woo_cache_by_id'):
            return self.woo_cache_by_id.get(woo_id)

        model = self.config.get_model()
        try:
            return self.session.query(model.WooCacheProduct)\
                               .filter(model.WooCacheProduct.id == woo_id)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def get_product_by_item_id(self, item_id):
        if hasattr(self, 'products_by_item_id'):
            return self.products_by_item_id.get(item_id)

        model = self.config.get_model()
        try:
            return self.session.query(model.Product)\
                               .filter(model.Product.item_id == item_id)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def get_host_objects(self):
        return get_woocommerce_products(self.api)

    def normalize_host_object(self, api_product):
        data = dict(api_product)

        product = self.find_rattail_product(api_product)
        data['product_uuid'] = product.uuid if product else None

        for field in self.date_fields:
            value = data[field]
            if value:
                value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
                if not field.endswith('_gmt'):
                    value = localtime(self.config, value)
                    value = make_utc(value)
                data[field] = value

        return data
