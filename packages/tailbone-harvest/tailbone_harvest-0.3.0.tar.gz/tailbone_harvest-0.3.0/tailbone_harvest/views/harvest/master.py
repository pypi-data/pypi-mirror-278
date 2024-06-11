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
Harvest master view
"""

from rattail_harvest.db.model import HarvestCacheTimeEntry

from webhelpers2.html import tags

from tailbone.views import MasterView


class HarvestMasterView(MasterView):
    """
    Base class for Harvest master views
    """
    creatable = False
    touchable = True
    has_versions = True
    model_row_class = HarvestCacheTimeEntry

    labels = {
        'id': "ID",
        'user_id': "User ID",
        'client_id': "Client ID",
        'project_id': "Project ID",
        'task_id': "Task ID",
        'invoice_id': "Invoice ID",
    }

    row_labels = {
        'id': "ID",
    }

    def configure_form(self, f):
        super(HarvestMasterView, self).configure_form(f)
        f.remove('time_entries')

    def render_harvest_user(self, obj, field):
        user = getattr(obj, field)
        if user:
            text = str(user)
            url = self.request.route_url('harvest.users.view', uuid=user.uuid)
            return tags.link_to(text, url)

    def render_harvest_client(self, obj, field):
        client = getattr(obj, field)
        if client:
            text = str(client)
            url = self.request.route_url('harvest.clients.view', uuid=client.uuid)
            return tags.link_to(text, url)

    def render_harvest_project(self, obj, field):
        project = getattr(obj, field)
        if project:
            text = str(project)
            url = self.request.route_url('harvest.projects.view', uuid=project.uuid)
            return tags.link_to(text, url)

    def render_harvest_task(self, obj, field):
        task = getattr(obj, field)
        if task:
            text = str(task)
            url = self.request.route_url('harvest.tasks.view', uuid=task.uuid)
            return tags.link_to(text, url)

    def configure_row_grid(self, g):
        super(HarvestMasterView, self).configure_row_grid(g)
        g.set_sort_defaults('spent_date', 'desc')

    def row_view_action_url(self, entry, i):
        return self.request.route_url('harvest.time_entries.view', uuid=entry.uuid)
