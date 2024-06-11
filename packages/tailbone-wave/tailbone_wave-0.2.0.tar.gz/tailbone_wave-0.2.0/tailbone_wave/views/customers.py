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
Customer views, w/ Wave integration
"""

from rattail_wave.config import get_wave_url

from webhelpers2.html import tags

from tailbone.views import ViewSupplement


class CustomerViewSupplement(ViewSupplement):
    """
    Customer view supplement for Wave integration
    """
    route_prefix = 'customers'

    labels = {
        'wave_id': "Wave ID",
    }

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.WaveCustomer)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('wave_id', model.WaveCustomer.wave_id)
        g.set_sorter('wave_id', model.WaveCustomer.wave_id)

    def configure_form(self, f):
        f.append('wave_id')
        f.set_required('wave_id', False)

    def get_xref_buttons(self, customer):
        model = self.model

        # wave proper
        if customer.wave_id:
            wave_customer = self.Session.query(model.WaveCacheCustomer)\
                                        .filter(model.WaveCacheCustomer.id == customer.wave_id)\
                                        .first()
            if wave_customer:
                url = get_wave_url(self.rattail_config)
                if url:
                    url = '{}/customers/{}/view'.format(
                        url, wave_customer.internal_id)
                    return [{'url': url, 'text': "View in Wave"}]

    def get_xref_links(self, customer):
        model = self.model

        # wave cache
        if customer.wave_id:
            wave_customer = self.Session.query(model.WaveCacheCustomer)\
                                        .filter(model.WaveCacheCustomer.id == customer.wave_id)\
                                        .first()
            if wave_customer:
                url = self.request.route_url('wave.customers.view',
                                             uuid=wave_customer.uuid)
                return [tags.link_to("View the Wave Cache record", url)]

    def get_version_child_classes(self):
        model = self.model
        return [model.WaveCustomer]


def includeme(config):
    CustomerViewSupplement.defaults(config)
