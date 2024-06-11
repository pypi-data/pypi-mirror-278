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

from rattail_wave.db.model import WaveCacheCustomer

from .master import WaveMasterView


class WaveCustomerView(WaveMasterView):
    """
    Master view for Wave Customers
    """
    model_class = WaveCacheCustomer
    url_prefix = '/wave/customers'
    route_prefix = 'wave.customers'

    labels = {
        'internal_id': "Internal ID",
    }

    grid_columns = [
        'name',
        'email',
        'is_archived',
        'modified_at',
    ]

    def configure_grid(self, g):
        super(WaveCustomerView, self).configure_grid(g)

        g.filters['name'].default_active = True
        g.filters['name'].default_verb = 'contains'

        g.set_sort_defaults('name')

        g.set_link('name')
        g.set_link('email')

    def configure_form(self, f):
        super(WaveCustomerView, self).configure_form(f)

        f.remove_field('invoices')


def defaults(config, **kwargs):
    base = globals()

    WaveCustomerView = kwargs.get('WaveCustomerView', base['WaveCustomerView'])
    WaveCustomerView.defaults(config)


def includeme(config):
    defaults(config)
