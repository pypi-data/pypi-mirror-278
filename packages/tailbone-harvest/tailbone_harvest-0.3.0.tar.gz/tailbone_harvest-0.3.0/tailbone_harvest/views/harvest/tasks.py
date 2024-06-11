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
Harvest Task views
"""

from rattail_harvest.db.model import HarvestCacheTask
from rattail_harvest.harvest.config import get_harvest_url

from .master import HarvestMasterView


class HarvestCacheTaskView(HarvestMasterView):
    """
    Master view for Harvest Tasks
    """
    model_class = HarvestCacheTask
    url_prefix = '/harvest/tasks'
    route_prefix = 'harvest.tasks'

    grid_columns = [
        'id',
        'name',
        'billable_by_default',
        'default_hourly_rate',
        'is_default',
        'is_active',
    ]

    def configure_grid(self, g):
        super().configure_grid(g)

        g.set_sort_defaults('name')

        g.set_link('id')
        g.set_link('name')

    def configure_form(self, f):
        super().configure_form(f)

        # time_entries
        f.remove_field('time_entries')

    def get_xref_buttons(self, task):
        buttons = super().get_xref_buttons(task)
        model = self.model

        # harvest
        url = get_harvest_url(self.rattail_config)
        if url:
            url = '{}/tasks'.format(url)
            buttons.append(self.make_xref_button(url=url,
                                                 text="View in Harvest"))

        return buttons


def defaults(config, **kwargs):
    base = globals()

    HarvestCacheTaskView = kwargs.get('HarvestCacheTaskView', base['HarvestCacheTaskView'])
    HarvestCacheTaskView.defaults(config)


def includeme(config):
    defaults(config)
