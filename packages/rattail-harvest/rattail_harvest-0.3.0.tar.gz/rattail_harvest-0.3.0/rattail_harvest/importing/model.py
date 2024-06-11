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
rattail-harvest model importers
"""

import logging

from rattail.importing.model import ToRattail
from rattail_harvest.db import model


log = logging.getLogger(__name__)


##############################
# harvest cache models
##############################

class HarvestCacheUserImporter(ToRattail):
    model_class = model.HarvestCacheUser

class HarvestCacheClientImporter(ToRattail):
    model_class = model.HarvestCacheClient

class HarvestCacheProjectImporter(ToRattail):
    model_class = model.HarvestCacheProject

class HarvestCacheTaskImporter(ToRattail):
    model_class = model.HarvestCacheTask

class HarvestCacheTimeEntryImporter(ToRattail):
    model_class = model.HarvestCacheTimeEntry

    # flags to auto-create records for "unknown" references
    auto_create_unknown_project = True

    # flags to log warning vs. debug for "unknown" references
    warn_for_unknown_project = True

    def setup(self):
        super().setup()
        model = self.model

        if 'project_id' in self.fields:
            self.harvest_projects_by_id = self.app.cache_model(
                self.session, model.HarvestCacheProject, key='id')

    def cache_query(self):
        query = super().cache_query()

        if self.start_date:
            query = query.filter(self.model_class.spent_date >= self.start_date)
        if self.end_date:
            query = query.filter(self.model_class.spent_date <= self.end_date)

        return query

    def get_harvest_project(self, project_id):
        if hasattr(self, 'harvest_projects_by_id'):
            return self.harvest_projects_by_id.get(project_id)

        model = self.model
        return self.session.query(model.HarvestCacheProject)\
                           .filter(model.HarvestCacheProject.id == project_id)\
                           .first()

    def update_object(self, entry, data, local_data=None):
        entry = super().update_object(entry, data, local_data)
        model = self.model

        if 'project_id' in self.fields:
            project_id = data['project_id']
            project = self.get_harvest_project(project_id)
            if not project:
                logger = log.warning if self.warn_for_unknown_project else log.debug
                logger("unknown project id %s for time entry id %s: %s",
                       project_id, entry.id, entry)
                if self.auto_create_unknown_project:
                    project = model.HarvestCacheProject()
                    project.id = project_id
                    project.name = "(unknown)"
                    self.session.add(project)
                    if hasattr(self, 'harvest_projects_by_id'):
                        self.harvest_projects_by_id[project_id] = project
                elif entry.project_id:
                    entry.project_id = None

        return entry
