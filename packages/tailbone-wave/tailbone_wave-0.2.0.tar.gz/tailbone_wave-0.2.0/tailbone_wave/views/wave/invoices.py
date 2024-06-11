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
Wave Client views
"""

from rattail_wave.db.model import WaveCacheInvoice

from .master import WaveMasterView


class WaveInvoiceView(WaveMasterView):
    """
    Master view for Wave Invoices
    """
    model_class = WaveCacheInvoice
    url_prefix = '/wave/invoices'
    route_prefix = 'wave.invoices'

    grid_columns = [
        'title',
        'customer',
        'invoice_date',
        'total',
        'status',
        'modified_at',
    ]

    def configure_grid(self, g):
        super(WaveInvoiceView, self).configure_grid(g)
        model = self.model

        g.set_joiner('customer', lambda q: q.join(model.WaveCacheCustomer))
        g.set_sorter('customer', model.WaveCacheCustomer.name)
        g.set_filter('customer', model.WaveCacheCustomer.name,
                     label="Customer Name",
                     default_active=True, default_verb='contains')

        g.set_type('total', 'currency')

        g.set_sort_defaults('modified_at', 'desc')

        g.set_link('customer')
        g.set_link('invoice_date')


def defaults(config, **kwargs):
    base = globals()

    WaveInvoiceView = kwargs.get('WaveInvoiceView', base['WaveInvoiceView'])
    WaveInvoiceView.defaults(config)


def includeme(config):
    defaults(config)
