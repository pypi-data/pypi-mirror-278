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
Harvest Project views
"""

from rattail_harvest.db.model import HarvestCacheProject
from rattail_harvest.harvest.config import get_harvest_url

from .master import HarvestMasterView


class HarvestCacheProjectView(HarvestMasterView):
    """
    Master view for Harvest Projects
    """
    model_class = HarvestCacheProject
    url_prefix = '/harvest/projects'
    route_prefix = 'harvest.projects'

    has_rows = True

    grid_columns = [
        'id',
        'client',
        'name',
        'code',
        'is_active',
        'is_billable',
        'bill_by',
        'hourly_rate',
        'fee',
    ]

    row_grid_columns = [
        'id',
        'spent_date',
        'user',
        'client',
        'task',
        'hours',
    ]

    def configure_grid(self, g):
        super().configure_grid(g)
        model = self.model

        g.set_joiner('client', lambda q: q.outerjoin(model.HarvestCacheClient))
        g.set_sorter('client', model.HarvestCacheClient.name)
        g.set_filter('client', model.HarvestCacheClient.name, label="Client Name")
        g.filters['client'].default_active = True
        g.filters['client'].default_verb = 'contains'

        g.filters['is_active'].default_active = True
        g.filters['is_active'].default_verb = 'is_true'

        g.set_type('hourly_rate', 'currency')
        g.set_type('fee', 'currency')

        g.set_sort_defaults('client')

        g.set_filters_sequence([
            'id',
            'name',
            'client',
        ])

        g.set_link('id')
        g.set_link('client')
        g.set_link('name')
        g.set_link('code')

    def grid_extra_class(self, project, i):
        if not project.is_active:
            return 'warning'

    def configure_form(self, f):
        super().configure_form(f)

        f.set_type('hourly_rate', 'currency')

        if self.editing:
            f.remove('client')
            f.set_type('over_budget_notification_date', 'date_jquery')
            f.set_type('starts_on', 'date_jquery')
            f.set_type('ends_on', 'date_jquery')
            f.set_readonly('created_at')
            f.set_readonly('updated_at')

    def get_xref_buttons(self, project):
        buttons = super().get_xref_buttons(project)
        model = self.model

        # harvest
        url = get_harvest_url(self.rattail_config)
        if url:
            url = '{}/projects/{}'.format(url, project.id)
            buttons.append(self.make_xref_button(url=url,
                                                 text="View in Harvest"))

        return buttons

    def get_row_data(self, project):
        model = self.model
        return self.Session.query(model.HarvestCacheTimeEntry)\
                           .filter(model.HarvestCacheTimeEntry.project == project)

    def get_parent(self, entry):
        return entry.project


def defaults(config, **kwargs):
    base = globals()

    HarvestCacheProjectView = kwargs.get('HarvestCacheProjectView', base['HarvestCacheProjectView'])
    HarvestCacheProjectView.defaults(config)


def includeme(config):
    defaults(config)
