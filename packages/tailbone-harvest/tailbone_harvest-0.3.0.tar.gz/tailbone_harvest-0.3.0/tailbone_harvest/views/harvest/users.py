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
Harvest User views
"""

from rattail_harvest.db.model import HarvestCacheUser
from rattail_harvest.harvest.config import get_harvest_url

import colander

from tailbone import forms
from .master import HarvestMasterView


class HarvestCacheUserView(HarvestMasterView):
    """
    Master view for Harvest Users
    """
    model_class = HarvestCacheUser
    url_prefix = '/harvest/users'
    route_prefix = 'harvest.users'

    labels = {
        'avatar_url': "Avatar URL",
    }

    grid_columns = [
        'id',
        'first_name',
        'last_name',
        'email',
        'telephone',
        'timezone',
        'is_admin',
    ]

    def configure_grid(self, g):
        super().configure_grid(g)
        model = self.model

        g.set_joiner('person_name', lambda q: q.outerjoin(model.Person))
        g.set_filter('person_name', model.Person.display_name)

        g.set_sort_defaults('first_name')

        g.set_link('id')
        g.set_link('first_name')
        g.set_link('last_name')
        g.set_link('email')

    def configure_form(self, f):
        super().configure_form(f)
        model = self.model
        user = f.model_instance

        # person
        f.set_renderer('person', self.render_person)
        if self.creating or self.editing:
            if 'person' in f.fields:
                f.remove('person_uuid')
                f.replace('person', 'person_uuid')
                person_display = ""
                if self.request.method == 'POST':
                    if self.request.POST.get('person_uuid'):
                        person = self.Session.get(model.Person,
                                                  self.request.POST['person_uuid'])
                        if person:
                            person_display = str(person)
                elif self.editing:
                    person_display = str(user.person or '')
                people_url = self.request.route_url('people.autocomplete')
                f.set_widget('person_uuid', forms.widgets.JQueryAutocompleteWidget(
                    field_display=person_display, service_url=people_url))
                f.set_validator('person_uuid', self.valid_person)
                f.set_label('person_uuid', "Person")
        else:
            f.remove('person_uuid')

        f.set_type('weekly_capacity', 'duration')

        f.set_type('default_hourly_rate', 'currency')
        f.set_type('cost_rate', 'currency')

        f.set_renderer('avatar_url', self.render_url)

        # timestamps
        if self.creating or self.editing:
            f.remove('created_at')
            f.remove('updated_at')

        # time_entries
        # TODO: should add this as child rows/grid instead
        f.remove('time_entries')

    def valid_person(self, node, value):
        model = self.model
        if value:
            person = self.Session.get(model.Person, value)
            if not person:
                raise colander.Invalid(node, "Person not found (you must *select* a record)")

    def get_xref_buttons(self, user):
        buttons = super().get_xref_buttons(user)
        model = self.model

        # harvest proper
        url = get_harvest_url(self.rattail_config)
        if url:
            url = '{}/team'.format(url)
            buttons.append(self.make_xref_button(url=url, text="View in Harvest"))

        return buttons


def defaults(config, **kwargs):
    base = globals()

    HarvestCacheUserView = kwargs.get('HarvestCacheUserView', base['HarvestCacheUserView'])
    HarvestCacheUserView.defaults(config)


def includeme(config):
    defaults(config)
