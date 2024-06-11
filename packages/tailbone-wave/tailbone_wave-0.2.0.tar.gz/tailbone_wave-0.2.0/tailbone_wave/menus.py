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
Common menus for Wave
"""

from rattail_wave.config import get_wave_url


def make_wave_menu(request):
    url = request.route_url

    wave_menu = {
        'title': "Wave",
        'type': 'menu',
        'items': [
            {
                'title': "Customers",
                'route': 'wave.customers',
                'perm': 'wave.customers.list',
            },
            {
                'title': "Invoices",
                'route': 'wave.invoices',
                'perm': 'wave.invoices.list',
            },
        ],
    }

    wave_url = get_wave_url(request.rattail_config)
    if wave_url:
        wave_menu['items'].insert(
            0, {
                'title': "Go to Wave",
                'url': '{}/dashboard/'.format(wave_url),
                'target': '_blank',
            })
        wave_menu['items'].insert(
            1, {'type': 'sep'})

    return wave_menu
