# -*- coding: utf-8 -*-
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
Rattail -> Rattail data import for Harvest integration
"""

from rattail.importing import rattail as base
from rattail_harvest import importing as rattail_harvest_importing


class FromRattailToRattailHarvestMixin(object):
    """
    Add default registration of custom importers
    """

    def add_harvest_importers(self, importers):
        importers['HarvestCacheUser'] = HarvestCacheUserImporter
        importers['HarvestCacheClient'] = HarvestCacheClientImporter
        importers['HarvestCacheProject'] = HarvestCacheProjectImporter
        importers['HarvestCacheTask'] = HarvestCacheTaskImporter
        importers['HarvestCacheTimeEntry'] = HarvestCacheTimeEntryImporter
        return importers


##############################
# harvest cache models
##############################

class HarvestCacheUserImporter(base.FromRattail, rattail_harvest_importing.model.HarvestCacheUserImporter):
    pass

class HarvestCacheClientImporter(base.FromRattail, rattail_harvest_importing.model.HarvestCacheClientImporter):
    pass

class HarvestCacheProjectImporter(base.FromRattail, rattail_harvest_importing.model.HarvestCacheProjectImporter):
    pass

class HarvestCacheTaskImporter(base.FromRattail, rattail_harvest_importing.model.HarvestCacheTaskImporter):
    pass

class HarvestCacheTimeEntryImporter(base.FromRattail, rattail_harvest_importing.model.HarvestCacheTimeEntryImporter):

    def query(self):
        query = super().query()

        if self.start_date:
            query = query.filter(self.model_class.spent_date >= self.start_date)
        if self.end_date:
            query = query.filter(self.model_class.spent_date <= self.end_date)

        return query
