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
Common menus for Harvest
"""


def make_harvest_menu(request):
    url = request.route_url

    harvest_menu = {
        'title': "Harvest",
        'type': 'menu',
        'items': [
            {
                'title': "Users",
                'url': url('harvest.users'),
                'perm': 'harvest.users.list',
            },
            {
                'title': "Clients",
                'url': url('harvest.clients'),
                'perm': 'harvest.clients.list',
            },
            {
                'title': "Projects",
                'url': url('harvest.projects'),
                'perm': 'harvest.projects.list',
            },
            {
                'title': "Tasks",
                'url': url('harvest.tasks'),
                'perm': 'harvest.tasks.list',
            },
            {
                'title': "Time Entries",
                'url': url('harvest.time_entries'),
                'perm': 'harvest.time_entries.list',
            },
        ],
    }

    harvest_url = request.rattail_config.get('harvest', 'url')
    if harvest_url:
        harvest_menu['items'].insert(
            0, {
                'title': "Go to Harvest",
                'url': harvest_url,
                'target': '_blank',
            })
        harvest_menu['items'].insert(
            1, {'type': 'sep'})

    return harvest_menu
