# -*- coding: utf-8 -*-
"""initial WooCommerce-related tables

Revision ID: c0bcca7bd1f9
Revises: a3a6e2f7c9a5
Create Date: 2021-01-19 19:05:51.962092

"""

# revision identifiers, used by Alembic.
revision = 'c0bcca7bd1f9'
down_revision = None
branch_labels = ('rattail_woocommerce',)
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # woocommerce_product
    op.create_table('woocommerce_product',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('woocommerce_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['product.uuid'], name='woocommerce_product_fk_product'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('woocommerce_product_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('woocommerce_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_woocommerce_product_version_end_transaction_id'), 'woocommerce_product_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_woocommerce_product_version_operation_type'), 'woocommerce_product_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_woocommerce_product_version_transaction_id'), 'woocommerce_product_version', ['transaction_id'], unique=False)

    # woocommerce_cache_product
    op.create_table('woocommerce_cache_product',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('product_uuid', sa.String(length=32), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('slug', sa.String(length=100), nullable=True),
                    sa.Column('permalink', sa.String(length=255), nullable=True),
                    sa.Column('date_created', sa.DateTime(), nullable=True),
                    sa.Column('date_created_gmt', sa.DateTime(), nullable=True),
                    sa.Column('date_modified', sa.DateTime(), nullable=True),
                    sa.Column('date_modified_gmt', sa.DateTime(), nullable=True),
                    sa.Column('type', sa.String(length=20), nullable=True),
                    sa.Column('status', sa.String(length=20), nullable=True),
                    sa.Column('featured', sa.Boolean(), nullable=True),
                    sa.Column('catalog_visibility', sa.String(length=20), nullable=True),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('short_description', sa.String(length=255), nullable=True),
                    sa.Column('sku', sa.String(length=50), nullable=True),
                    sa.Column('price', sa.String(length=20), nullable=True),
                    sa.Column('regular_price', sa.String(length=20), nullable=True),
                    sa.Column('sale_price', sa.String(length=20), nullable=True),
                    sa.Column('date_on_sale_from', sa.DateTime(), nullable=True),
                    sa.Column('date_on_sale_from_gmt', sa.DateTime(), nullable=True),
                    sa.Column('date_on_sale_to', sa.DateTime(), nullable=True),
                    sa.Column('date_on_sale_to_gmt', sa.DateTime(), nullable=True),
                    sa.Column('price_html', sa.String(length=255), nullable=True),
                    sa.Column('on_sale', sa.Boolean(), nullable=True),
                    sa.Column('purchasable', sa.Boolean(), nullable=True),
                    sa.Column('total_sales', sa.Integer(), nullable=True),
                    sa.Column('tax_status', sa.String(length=20), nullable=True),
                    sa.Column('tax_class', sa.String(length=50), nullable=True),
                    sa.Column('manage_stock', sa.Boolean(), nullable=True),
                    sa.Column('stock_quantity', sa.Integer(), nullable=True),
                    sa.Column('stock_status', sa.String(length=20), nullable=True),
                    sa.Column('backorders', sa.String(length=20), nullable=True),
                    sa.Column('backorders_allowed', sa.Boolean(), nullable=True),
                    sa.Column('backordered', sa.Boolean(), nullable=True),
                    sa.Column('sold_individually', sa.Boolean(), nullable=True),
                    sa.Column('weight', sa.String(length=20), nullable=True),
                    sa.Column('reviews_allowed', sa.Boolean(), nullable=True),
                    sa.Column('parent_id', sa.Integer(), nullable=True),
                    sa.Column('purchase_note', sa.String(length=255), nullable=True),
                    sa.Column('menu_order', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['product_uuid'], ['product.uuid'], name='woocommerce_cache_product_fk_product'),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('id', name='woocommerce_cache_product_uq_id')
    )
    op.create_table('woocommerce_cache_product_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('product_uuid', sa.String(length=32), autoincrement=False, nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('name', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('slug', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('permalink', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('date_created', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('date_created_gmt', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('type', sa.String(length=20), autoincrement=False, nullable=True),
                    sa.Column('status', sa.String(length=20), autoincrement=False, nullable=True),
                    sa.Column('featured', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('catalog_visibility', sa.String(length=20), autoincrement=False, nullable=True),
                    sa.Column('description', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('short_description', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('sku', sa.String(length=50), autoincrement=False, nullable=True),
                    sa.Column('price', sa.String(length=20), autoincrement=False, nullable=True),
                    sa.Column('regular_price', sa.String(length=20), autoincrement=False, nullable=True),
                    sa.Column('sale_price', sa.String(length=20), autoincrement=False, nullable=True),
                    sa.Column('date_on_sale_from', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('date_on_sale_from_gmt', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('date_on_sale_to', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('date_on_sale_to_gmt', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('price_html', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('on_sale', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('purchasable', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('tax_status', sa.String(length=20), autoincrement=False, nullable=True),
                    sa.Column('tax_class', sa.String(length=50), autoincrement=False, nullable=True),
                    sa.Column('manage_stock', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('backorders', sa.String(length=20), autoincrement=False, nullable=True),
                    sa.Column('backorders_allowed', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('sold_individually', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('weight', sa.String(length=20), autoincrement=False, nullable=True),
                    sa.Column('reviews_allowed', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('parent_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('purchase_note', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('menu_order', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_woocommerce_cache_product_version_end_transaction_id'), 'woocommerce_cache_product_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_woocommerce_cache_product_version_operation_type'), 'woocommerce_cache_product_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_woocommerce_cache_product_version_transaction_id'), 'woocommerce_cache_product_version', ['transaction_id'], unique=False)


def downgrade():

    # woocommerce_cache_product
    op.drop_index(op.f('ix_woocommerce_cache_product_version_transaction_id'), table_name='woocommerce_cache_product_version')
    op.drop_index(op.f('ix_woocommerce_cache_product_version_operation_type'), table_name='woocommerce_cache_product_version')
    op.drop_index(op.f('ix_woocommerce_cache_product_version_end_transaction_id'), table_name='woocommerce_cache_product_version')
    op.drop_table('woocommerce_cache_product_version')
    op.drop_table('woocommerce_cache_product')

    # woocommerce_product
    op.drop_index(op.f('ix_woocommerce_product_version_transaction_id'), table_name='woocommerce_product_version')
    op.drop_index(op.f('ix_woocommerce_product_version_operation_type'), table_name='woocommerce_product_version')
    op.drop_index(op.f('ix_woocommerce_product_version_end_transaction_id'), table_name='woocommerce_product_version')
    op.drop_table('woocommerce_product_version')
    op.drop_table('woocommerce_product')
