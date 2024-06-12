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
Database schema extensions for WooCommerce integration
"""

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declared_attr

from rattail.db import model
from rattail.db.model.shopfoo import ShopfooProductBase


__all__ = [
    'WooProductExtension',
    'WooCacheProduct',
]


class WooProductExtension(model.Base):
    """
    WooCommerce-specific extension to Rattail Product
    """
    __tablename__ = 'woocommerce_product'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['product.uuid'],
                                name='woocommerce_product_fk_product'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    product = orm.relationship(
        model.Product,
        doc="""
        Reference to the actual product record, which this one extends.
        """,
        backref=orm.backref(
            '_woocommerce',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the WooCommerce extension record for this product.
            """))

    woocommerce_id = sa.Column(sa.Integer(), nullable=False, doc="""
    ``id`` value for the product, within WooCommerce.
    """)

    def __str__(self):
        return str(self.product)

WooProductExtension.make_proxy(model.Product, '_woocommerce', 'woocommerce_id')


class WooCacheProduct(ShopfooProductBase, model.Base):
    """
    Local cache table for WooCommerce Products

    https://woocommerce.github.io/woocommerce-rest-api-docs/#product-properties
    """
    __tablename__ = 'woocommerce_cache_product'
    model_title = "WooCommerce Product"

    @declared_attr
    def __table_args__(cls):
        return cls.__product_table_args__() + (
            sa.UniqueConstraint('id', name='woocommerce_cache_product_uq_id'),
        )

    __versioned__ = {
        'exclude': [
            'date_modified',
            'date_modified_gmt',
            'total_sales',
            'stock_quantity',
            'stock_status',
            'backordered',
        ]}

    id = sa.Column(sa.Integer(), nullable=False)

    name = sa.Column(sa.String(length=255), nullable=True)

    slug = sa.Column(sa.String(length=100), nullable=True)

    permalink = sa.Column(sa.String(length=255), nullable=True)

    date_created = sa.Column(sa.DateTime(), nullable=True)

    date_created_gmt = sa.Column(sa.DateTime(), nullable=True)

    date_modified = sa.Column(sa.DateTime(), nullable=True)

    date_modified_gmt = sa.Column(sa.DateTime(), nullable=True)

    type = sa.Column(sa.String(length=20), nullable=True)

    status = sa.Column(sa.String(length=20), nullable=True)

    featured = sa.Column(sa.Boolean(), nullable=True)

    catalog_visibility = sa.Column(sa.String(length=20), nullable=True)

    description = sa.Column(sa.String(length=255), nullable=True)

    short_description = sa.Column(sa.String(length=255), nullable=True)

    sku = sa.Column(sa.String(length=50), nullable=True)

    price = sa.Column(sa.String(length=20), nullable=True)

    regular_price = sa.Column(sa.String(length=20), nullable=True)

    sale_price = sa.Column(sa.String(length=20), nullable=True)

    date_on_sale_from = sa.Column(sa.DateTime(), nullable=True)

    date_on_sale_from_gmt = sa.Column(sa.DateTime(), nullable=True)

    date_on_sale_to = sa.Column(sa.DateTime(), nullable=True)

    date_on_sale_to_gmt = sa.Column(sa.DateTime(), nullable=True)

    price_html = sa.Column(sa.String(length=255), nullable=True)

    on_sale = sa.Column(sa.Boolean(), nullable=True)

    purchasable = sa.Column(sa.Boolean(), nullable=True)

    total_sales = sa.Column(sa.Integer(), nullable=True)

    tax_status = sa.Column(sa.String(length=20), nullable=True)

    tax_class = sa.Column(sa.String(length=50), nullable=True)

    manage_stock = sa.Column(sa.Boolean(), nullable=True)

    stock_quantity = sa.Column(sa.Integer(), nullable=True)

    stock_status = sa.Column(sa.String(length=20), nullable=True)

    backorders = sa.Column(sa.String(length=20), nullable=True)

    backorders_allowed = sa.Column(sa.Boolean(), nullable=True)

    backordered = sa.Column(sa.Boolean(), nullable=True)

    sold_individually = sa.Column(sa.Boolean(), nullable=True)

    weight = sa.Column(sa.String(length=20), nullable=True)

    reviews_allowed = sa.Column(sa.Boolean(), nullable=True)

    parent_id = sa.Column(sa.Integer(), nullable=True)

    purchase_note = sa.Column(sa.String(length=255), nullable=True)

    menu_order = sa.Column(sa.Integer(), nullable=True)

    def __str__(self):
        return self.name or ""
