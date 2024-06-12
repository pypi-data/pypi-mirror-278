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
Product Views
"""

from sqlalchemy import orm

from rattail_woocommerce.config import woocommerce_admin_product_url

from webhelpers2.html import tags

from tailbone.views import ViewSupplement


class ProductViewSupplement(ViewSupplement):
    """
    Product view supplement for WooCommerce integration
    """
    route_prefix = 'products'

    labels = {
        'woocommerce_id': "WooCommerce ID",
    }

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.WooProductExtension)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('woocommerce_id', model.WooProductExtension.woocommerce_id)

    def configure_form(self, f):
        if not self.master.creating:
            f.append('woocommerce_id')

    def get_version_child_classes(self):
        model = self.model
        return [model.WooProductExtension]

    def get_panel_fields_main(self, product):
        return ['woocommerce_id']

    def get_xref_buttons(self, product):
        buttons = []

        woo_cached = self.get_woo_cached_product(product)
        if woo_cached:
            buttons.append({'url': woo_cached.permalink,
                            'text': "View in WooCommerce Store"})

        woo_id = woo_cached.id if woo_cached else product.woocommerce_id
        if woo_id:
            url = woocommerce_admin_product_url(self.rattail_config, woo_id)
            if url:
                buttons.append({'url': url,
                                'text': "View in WooCommerce Admin"})

        return buttons

    def get_xref_links(self, product):
        if product.woocommerce_cache_product:
            url = self.request.route_url('woocommerce.products.view',
                                         uuid=product.woocommerce_cache_product.uuid)
            return [tags.link_to("View WooCommerce Product", url)]

    def get_woo_cached_product(self, product):
        """
        Tries to identify the WooCacheProduct for the given Rattail Product.
        """
        model = self.model
        woo_cached = None

        if product.woocommerce_cache_product:
            # we have an official link between rattail and woo
            woo_cached = product.woocommerce_cache_product

        elif product.item_id:
            # try to find matching woo product, even though not linked
            try:
                woo_cached = self.Session.query(model.WooCacheProduct)\
                                         .filter(model.WooCacheProduct.sku == product.item_id)\
                                         .one()
            except orm.exc.NoResultFound:
                pass

        return woo_cached


def includeme(config):
    ProductViewSupplement.defaults(config)
