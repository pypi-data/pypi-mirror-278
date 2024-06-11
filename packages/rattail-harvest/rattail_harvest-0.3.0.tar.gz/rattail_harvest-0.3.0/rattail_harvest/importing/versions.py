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
Rattail -> Rattail "versions" data import
"""

from rattail.importing import versions as base


class HarvestVersionMixin(object):

    def add_harvest_importers(self, importers):
        importers['HarvestCacheUser'] = HarvestCacheUserImporter
        importers['HarvestCacheClient'] = HarvestCacheClientImporter
        importers['HarvestCacheProject'] = HarvestCacheProjectImporter
        importers['HarvestCacheTask'] = HarvestCacheTaskImporter
        importers['HarvestCacheTimeEntry'] = HarvestCacheTimeEntryImporter
        return importers


class HarvestCacheUserImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        return self.model.HarvestCacheUser


class HarvestCacheClientImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        return self.model.HarvestCacheClient


class HarvestCacheProjectImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        return self.model.HarvestCacheProject


class HarvestCacheTaskImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        return self.model.HarvestCacheTask


class HarvestCacheTimeEntryImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        return self.model.HarvestCacheTimeEntry
