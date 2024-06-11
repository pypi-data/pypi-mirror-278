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
Harvest -> Rattail "cache" data import
"""

import datetime
import decimal
import logging
from collections import OrderedDict

import sqlalchemy as sa

from rattail import importing
from rattail_harvest import importing as rattail_harvest_importing
from rattail_harvest.harvest.webapi import make_harvest_webapi


log = logging.getLogger(__name__)


class FromHarvestToRattail(importing.ToRattailHandler):
    """
    Import handler for data coming from the Harvest API
    """
    host_key = 'harvest'
    host_title = "Harvest (API)"
    generic_host_title = "Harvest (API)"

    def get_importers(self):
        importers = OrderedDict()
        importers['HarvestCacheUser'] = HarvestCacheUserImporter
        importers['HarvestCacheClient'] = HarvestCacheClientImporter
        importers['HarvestCacheProject'] = HarvestCacheProjectImporter
        importers['HarvestCacheTask'] = HarvestCacheTaskImporter
        importers['HarvestCacheTimeEntry'] = HarvestCacheTimeEntryImporter
        return importers


class FromHarvest(importing.Importer):
    """
    Base class for all Harvest importers
    """
    key = 'id'

    @property
    def supported_fields(self):
        fields = list(super(FromHarvest, self).supported_fields)
        fields.remove('uuid')
        return fields

    def setup(self):
        super(FromHarvest, self).setup()
        self.webapi = make_harvest_webapi(self.config)

    def time_from_harvest(self, value):
        # all harvest times appear to come as UTC, so no conversion needed
        value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        return value

    def normalize_host_object(self, obj):
        data = dict(obj)

        if 'created_at' in self.fields:
            data['created_at'] = self.time_from_harvest(data['created_at'])

        if 'updated_at' in self.fields:
            data['updated_at'] = self.time_from_harvest(data['updated_at'])

        return data


class HarvestCacheUserImporter(FromHarvest, rattail_harvest_importing.model.HarvestCacheUserImporter):
    """
    Import user data from Harvest
    """

    @property
    def supported_fields(self):
        fields = list(super().supported_fields)

        # this is for local tracking only; is not in harvest
        fields.remove('person_uuid')

        # this used to be in harvest i thought, but is no longer?
        fields.remove('name')

        return fields

    def get_host_objects(self):
        return self.webapi.get_users()['users']

    def normalize_host_object(self, user):
        data = super().normalize_host_object(user)
        if data:

            # TODO: for some reason the API used to include the these
            # fields, but no longer does as of 2022-11-11, so null is
            # kinda the only thing that makes sense now.  if possible,
            # should figure out "what changed" at Harvest, but maybe
            # these fields should just be removed from our cache
            # schema?
            data.setdefault('is_admin', None)
            data.setdefault('is_project_manager', None)
            data.setdefault('can_see_rates', None)
            data.setdefault('can_create_invoices', None)

            if data['telephone'] == '':
                data['telephone'] = None

            return data


class HarvestCacheClientImporter(FromHarvest, rattail_harvest_importing.model.HarvestCacheClientImporter):
    """
    Import client data from Harvest
    """

    def get_host_objects(self):
        return self.webapi.get_clients()['clients']


class HarvestCacheProjectImporter(FromHarvest, rattail_harvest_importing.model.HarvestCacheProjectImporter):
    """
    Import project data from Harvest
    """

    @property
    def supported_fields(self):
        fields = list(super().supported_fields)

        # this is for local tracking only; is not in harvest
        fields.remove('deleted')

        return fields

    def cache_query(self):
        model = self.model
        return self.session.query(model.HarvestCacheProject)\
                           .filter(sa.or_(
                               model.HarvestCacheProject.deleted == False,
                               model.HarvestCacheProject.deleted == None))

    def get_host_objects(self):
        return self.webapi.get_projects()

    def normalize_host_object(self, project):
        data = super().normalize_host_object(project)
        if not data:
            return

        data['client_id'] = project['client']['id']

        # cost_budget
        cost_budget = data['cost_budget']
        if cost_budget is not None:
            cost_budget = decimal.Decimal('{:0.2f}'.format(cost_budget))
            data['cost_budget'] = cost_budget

        # fee
        fee = data['fee']
        if fee is not None:
            fee = decimal.Decimal('{:0.2f}'.format(fee))
            data['fee'] = fee

        # starts_on
        starts_on = data['starts_on']
        if starts_on:
            starts_on = datetime.datetime.strptime(starts_on, '%Y-%m-%d')
            data['starts_on'] = starts_on.date()

        # ends_on
        ends_on = data['ends_on']
        if ends_on:
            ends_on = datetime.datetime.strptime(ends_on, '%Y-%m-%d')
            data['ends_on'] = ends_on.date()

        # over_budget_notification_date
        date = data['over_budget_notification_date']
        if date:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            data['over_budget_notification_date'] = date.date()

        return data

    def can_delete_object(self, project, data):
        return not project.deleted

    def delete_object(self, project):
        project.deleted = True
        return True


class HarvestCacheTaskImporter(FromHarvest, rattail_harvest_importing.model.HarvestCacheTaskImporter):
    """
    Import task data from Harvest
    """

    def get_host_objects(self):
        return self.webapi.get_tasks()['tasks']


class HarvestCacheTimeEntryImporter(FromHarvest, rattail_harvest_importing.model.HarvestCacheTimeEntryImporter):
    """
    Import time entry data from Harvest
    """

    def get_host_objects(self):
        kw = {}
        if self.start_date:
            kw['from'] = self.start_date
        if self.end_date:
            kw['to'] = self.end_date
        return self.webapi.get_time_entries(**kw)

    def get_single_host_object(self, key):
        assert len(self.key) == 1 and self.key[0] == 'id'
        entry_id = key[0]
        return self.webapi.get_time_entry(entry_id)

    def normalize_host_object(self, entry):
        data = super().normalize_host_object(entry)
        if not data:
            return

        if entry['is_running']:
            log.debug("Harvest time entry is still running: %s", entry)
            return

        data['user_id'] = entry['user']['id']
        data['client_id'] = entry['client']['id']
        data['task_id'] = entry['task']['id']
        data['invoice_id'] = entry['invoice']['id'] if entry['invoice'] else None

        # project_id
        if 'project_id' in self.fields:
            data['project_id'] = entry['project']['id']
            project = self.get_harvest_project(data['project_id'])
            if not project:
                logger = log.warning if self.warn_for_unknown_project else log.debug
                logger("time entry references non-existent project id %s: %s",
                       data['project_id'], entry)
                if not self.auto_create_unknown_project:
                    data['project_id'] = None

        # spent_date
        spent_date = data['spent_date']
        if spent_date:
            spent_date = datetime.datetime.strptime(spent_date, '%Y-%m-%d')
            data['spent_date'] = spent_date.date()

        # hours
        hours = data['hours']
        if hours is not None:
            hours = decimal.Decimal('{:0.2f}'.format(hours))
            data['hours'] = hours

        return data
