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
WooCommerce utilities
"""


def get_woocommerce_products(api):
    """
    Fetch and return all products from Woo API.
    """
    products = []
    page = 1
    while True:

        # TODO: 100 seems to be the max allowed per page?
        # although docs do not seem to mention a limit..
        # https://woocommerce.github.io/woocommerce-rest-api-docs/?python#list-all-products
        response = api.get('products', params={'per_page': 100,
                                               'page': page,
                                               'orderby': 'id',
                                               'order': 'asc'})

        products.extend(response.json())

        # TODO: this seems a bit hacky, is there a better way?
        link = response.headers.get('Link')
        if link and 'rel="next"' in link:
            page += 1
        else:
            break

    return products
