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
WooCommerce product views
"""

from rattail_woocommerce.db.model import WooCacheProduct

from webhelpers2.html import HTML, tags

from tailbone.views import MasterView


class WooCacheProductView(MasterView):
    """
    WooCommerce Product views
    """
    model_class = WooCacheProduct
    url_prefix = '/woocommerce/products'
    route_prefix = 'woocommerce.products'
    creatable = False
    editable = False
    deletable = False
    has_versions = True

    labels = {
        'id': "ID",
        'sku': "SKU",
        'parent_id': "Parent ID",
        'price_html': "Price HTML",
        'date_created_gmt': "Date Created GMT",
        'date_modified_gmt': "Date Modified GMT",
        'date_on_sale_from_gmt': "Date On Sale From GMT",
        'date_on_sale_to_gmt': "Date On Sale To GMT",
    }

    grid_columns = [
        'id',
        'sku',
        'name',
        'price_html',
        'on_sale',
        'purchasable',
        'status',
        'date_modified',
    ]

    form_fields = [
        'id',
        'product',
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

    def configure_grid(self, g):
        super(WooCacheProductView, self).configure_grid(g)

        g.filters['sku'].default_active = True
        g.filters['sku'].default_verb = 'contains'

        g.filters['name'].default_active = True
        g.filters['name'].default_verb = 'contains'

        g.set_sort_defaults('sku')

        g.set_renderer('price_html', self.render_html)
        g.set_label('price_html', "Price")
        g.filters['price_html'].label = "Price HTML"

        g.set_link('id')
        g.set_link('sku')
        g.set_link('name')

    def configure_form(self, f):
        super(WooCacheProductView, self).configure_form(f)

        f.set_renderer('product', self.render_product)
        f.set_renderer('permalink', self.render_url)
        f.set_renderer('price_html', self.render_html)

        f.set_renderer('date_created_gmt', self.render_as_is)
        f.set_renderer('date_modified_gmt', self.render_as_is)
        f.set_renderer('date_on_sale_from_gmt', self.render_as_is)
        f.set_renderer('date_on_sale_to_gmt', self.render_as_is)


def includeme(config):
    WooCacheProductView.defaults(config)
