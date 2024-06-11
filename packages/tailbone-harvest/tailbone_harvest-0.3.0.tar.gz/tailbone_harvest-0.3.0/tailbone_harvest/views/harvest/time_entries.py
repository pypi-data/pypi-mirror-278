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
Harvest Time Entry views
"""

from rattail_harvest.db.model import HarvestCacheTimeEntry
from rattail_harvest.harvest.config import get_harvest_url

from .master import HarvestMasterView


class HarvestCacheTimeEntryView(HarvestMasterView):
    """
    Master view for Harvest Time Entries
    """
    model_class = HarvestCacheTimeEntry
    url_prefix = '/harvest/time-entries'
    route_prefix = 'harvest.time_entries'

    grid_columns = [
        'id',
        'spent_date',
        'user',
        'client',
        'project',
        'task',
        'hours',
        'notes',
    ]

    def configure_grid(self, g):
        super().configure_grid(g)

        g.set_type('hours', 'duration_hours')

        g.set_sort_defaults('spent_date', 'desc')

        g.set_link('id')
        g.set_link('user')
        g.set_link('client')
        g.set_link('notes')

    def configure_form(self, f):
        super().configure_form(f)

        # make sure id is first field
        f.remove('id')
        f.insert(0, 'id')

        # user
        f.remove('user_id')
        f.set_renderer('user', self.render_harvest_user)

        # client
        f.remove('client_id')
        f.set_renderer('client', self.render_harvest_client)

        # project
        f.remove('project_id')
        f.set_renderer('project', self.render_harvest_project)

        # task
        f.remove('task_id')
        f.set_renderer('task', self.render_harvest_task)

        # hours
        f.set_renderer('hours', self.render_hours)

        f.set_type('notes', 'text')

        f.set_type('billable_rate', 'currency')
        f.set_type('cost_rate', 'currency')

    def render_hours(self, entry, field):
        hours = getattr(entry, field)
        app = self.get_rattail_app()
        duration = app.render_duration(hours=hours)
        return f"{hours} ({duration})"

    def get_xref_buttons(self, entry):
        buttons = super().get_xref_buttons(entry)
        model = self.model

        # harvest
        url = get_harvest_url(self.rattail_config)
        if url:
            url = '{}/time/day/{}/{}'.format(
                url,
                entry.spent_date.strftime('%Y/%m/%d'),
                entry.user_id)
            buttons.append(self.make_xref_button(url=url,
                                                 text="View in Harvest"))

        return buttons

    def import_from_harvest(self):
        app = self.get_rattail_app()
        handler = app.get_import_handler('to_rattail.from_harvest.import', require=True)
        importer = handler.get_importer('HarvestCacheTimeEntry')
        importer.session = self.Session()
        importer.setup()

        cache_entry = self.get_instance()
        if self.oneoff_import(importer, local_object=cache_entry):
            self.request.session.flash(f"{self.get_model_title()} has been "
                                       f"(re-)imported from Harvest: {cache_entry}")
        else:
            self.request.session.flash("Import failed!", 'error')

        return self.redirect(self.get_action_url('view', cache_entry))

    @classmethod
    def defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        instance_url_prefix = cls.get_instance_url_prefix()
        permission_prefix = cls.get_permission_prefix()
        model_title = cls.get_model_title()

        # normal defaults
        cls._defaults(config)

        # import from harvest
        config.add_tailbone_permission(permission_prefix,
                                       f'{permission_prefix}.import_from_harvest',
                                       f"Re-Import {model_title} from Harvest")
        config.add_route(f'{route_prefix}.import_from_harvest',
                         f'{instance_url_prefix}/import-from-harvest',
                         request_method='POST')
        config.add_view(cls, attr='import_from_harvest',
                        route_name=f'{route_prefix}.import_from_harvest',
                        permission=f'{permission_prefix}.import_from_harvest')


def defaults(config, **kwargs):
    base = globals()

    HarvestCacheTimeEntryView = kwargs.get('HarvestCacheTimeEntryView', base['HarvestCacheTimeEntryView'])
    HarvestCacheTimeEntryView.defaults(config)


def includeme(config):
    defaults(config)
