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
Harvest model importers
"""

from rattail import importing
from rattail_harvest.harvest.webapi import make_harvest_webapi


class ToHarvest(importing.Importer):

    def setup(self):
        super().setup()
        self.setup_webapi()

    def datasync_setup(self):
        super().datasync_setup()
        self.setup_webapi()

    def setup_webapi(self):
        self.webapi = make_harvest_webapi(self.config)


class TimeEntryImporter(ToHarvest):
    """
    Harvest time entry data importer.
    """
    model_name = 'TimeEntry'
    key = 'id'
    supported_fields = [
        'id',
        'user_id',
        'client_id',
        'project_id',
        'task_id',
        'spent_date',
        # 'started_time',
        # 'ended_time',
        'hours',
        'notes',
    ]
    caches_local_data = True

    def cache_local_data(self, host_data=None):
        """
        Fetch existing time entries from Harvest.
        """
        cache = {}

        # TODO: we try to avoid entries w/ timer still running here,
        # but for some reason they still come back, so double-check
        kw = {'is_running': False}
        if self.start_date:
            kw['from'] = self.start_date
        if self.end_date:
            kw['to'] = self.end_date
        entries = self.webapi.get_time_entries(**kw)
        for entry in entries:
            # double-check here
            if not entry['is_running']:
                data = self.normalize_local_object(entry)
                if data:
                    normal = self.normalize_cache_object(entry, data)
                    key = self.get_cache_key(entry, normal)
                    cache[key] = normal
        return cache

    def get_single_local_object(self, key):
        assert len(self.key) == 1 and self.key[0] == 'id'
        entry_id = key[0]
        if entry_id > 0:
            return self.webapi.get_time_entry(entry_id)

    def normalize_local_object(self, entry):
        data = {
            'id': entry['id'],
            'client_id': entry['client']['id'],
            'project_id': entry['project']['id'],
            'task_id': entry['task']['id'],
            'spent_date': entry['spent_date'],
            # 'started_time': entry['started_time'],
            # 'ended_time': entry['ended_time'],
            'hours': entry['hours'],
            'notes': entry['notes'],
        }

        if 'user_id' in self.fields:
            data['user_id'] = entry['user']['id']

        return data

    def get_next_harvest_id(self):
        if hasattr(self, 'next_harvest_id'):
            next_id = self.next_harvest_id
        else:
            next_id = 1
        self.next_harvest_id = next_id + 1
        return -next_id

    def create_object(self, key, host_data):
        if self.dry_run:
            # mock out return value
            result = dict(host_data)
            if 'user_id' in self.fields:
                result['user'] = {'id': result['user_id']}
            if 'client_id' in self.fields:
                result['client'] = {'id': result['client_id']}
            result['project'] = {'id': result['project_id']}
            result['task'] = {'id': result['task_id']}
            return result

        kwargs = {
            'client_id': host_data['client_id'],
            'project_id': host_data['project_id'],
            'task_id': host_data['task_id'],
            'spent_date': host_data['spent_date'],
            # 'started_time': host_data['started_time'],
            # 'ended_time': host_data['ended_time'],
            'hours': host_data['hours'],
            'notes': host_data['notes'],
        }
        if 'user_id' in self.fields:
            kwargs['user_id'] = host_data['user_id']
        entry = self.webapi.put_time_entry(**kwargs)
        return entry

    def update_object(self, entry, host_data, local_data=None, all_fields=False):
        if self.dry_run:
            return entry

        kwargs = {
            'project_id': host_data['project_id'],
            'task_id': host_data['task_id'],
            'spent_date': host_data['spent_date'],
            # 'started_time': host_data['started_time'],
            # 'ended_time': host_data['ended_time'],
            'hours': host_data['hours'],
            'notes': host_data['notes'],
        }

        return self.webapi.update_time_entry(entry['id'], **kwargs)

    def delete_object(self, entry):
        if self.dry_run:
            return True

        self.webapi.delete_time_entry(entry['id'])
        return True
