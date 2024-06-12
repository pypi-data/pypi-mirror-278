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
Rattail/WooCommerce Config
"""


def woocommerce_url(config, require=False, **kwargs):
    """
    Returns the base URL for the WooCommerce website.  Note that this URL will
    *not* have a trailing slash.
    """
    args = ['woocommerce', 'url']
    if require:
        url = config.require(*args, **kwargs)
        return url.rstrip('/')
    else:
        url = config.get(*args, **kwargs)
        if url:
            return url.rstrip('/')


def woocommerce_admin_product_url(config, product_id, base_url=None,
                                  require=False):
    """
    Returns the WooCommerce Admin URL for the given product.
    """
    if not base_url:
        base_url = woocommerce_url(config, require=require)
    if base_url:
        return '{}/wp-admin/post.php?post={}&action=edit'.format(
            base_url, product_id)
