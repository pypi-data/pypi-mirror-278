# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
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
Harvest Web API
"""

import requests


class HarvestWebAPI(object):
    """
    Generic web API object.
    """

    def __init__(self, base_url=None, access_token=None, account_id=None,
                 user_agent=None):
        self.base_url = base_url or 'https://api.harvestapp.com/v2/'
        self.base_url = self.base_url.rstrip('/')
        self.access_token = access_token
        self.account_id = account_id
        self.user_agent = user_agent
        if not self.user_agent:
            raise ValueError("Must provide `user_agent` when creating API instance")

    def _request(self, request_method, api_method, params=None):
        """
        Perform a request for the given API method, and return the response.
        """
        api_method = api_method.lstrip('/')
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Harvest-Account-Id': self.account_id,
            'User-Agent': self.user_agent,
        }
        if request_method == 'GET':
            response = requests.get('{}/{}'.format(self.base_url, api_method),
                                    headers=headers, params=params)
        elif request_method == 'POST':
            response = requests.post('{}/{}'.format(self.base_url, api_method),
                                     headers=headers, params=params)
        elif request_method == 'PATCH':
            response = requests.patch('{}/{}'.format(self.base_url, api_method),
                                      headers=headers, params=params)
        elif request_method == 'DELETE':
            response = requests.delete('{}/{}'.format(self.base_url, api_method),
                                      headers=headers, params=params)
        else:
            raise NotImplementedError("unknown request method: {}".format(
                request_method))
        response.raise_for_status()
        return response

    def get(self, api_method, params=None):
        """
        Perform a GET request for the given API method, and return the response.
        """
        return self._request('GET', api_method, params=params)

    def post(self, api_method, params=None):
        """
        Perform a POST request for the given API method, and return the response.
        """
        return self._request('POST', api_method, params=params)

    def patch(self, api_method, params=None):
        """
        Perform a PATCH request for the given API method, and return the response.
        """
        return self._request('PATCH', api_method, params=params)

    def delete(self, api_method, params=None):
        """
        Perform a DELETE request for the given API method, and return the response.
        """
        return self._request('DELETE', api_method, params=params)

    def get_company(self):
        """
        Retrieves the company for the currently authenticated user.

        https://help.getharvest.com/api-v2/company-api/company/company/#retrieve-a-company
        """
        response = self.get('/company')
        return response.json()

    def get_users(self, **kwargs):
        """
        Retrieve all users.  Any kwargs are passed on as URL query
        string parameters.

        https://help.getharvest.com/api-v2/users-api/users/users/#list-all-users
        """
        response = self.get('/users', params=kwargs)
        return response.json()

    def get_clients(self, **kwargs):
        """
        Retrieve all clients.  Any kwargs are passed on as URL query string
        parameters.

        https://help.getharvest.com/api-v2/clients-api/clients/clients/#list-all-clients
        """
        response = self.get('/clients', params=kwargs)
        return response.json()

    def get_projects(self, **kwargs):
        """
        Retrieve all projects.  Any kwargs are passed on as URL query string
        parameters.

        https://help.getharvest.com/api-v2/projects-api/projects/projects/#list-all-projects
        """
        response = self.get('/projects', params=kwargs)
        data = response.json()
        projects = data['projects']
        while data['next_page']:

            kw = dict(kwargs)
            kw['page'] = data['next_page']
            response = self.get('/projects', params=kw)
            data = response.json()
            projects.extend(data['projects'])

        return projects

    def get_tasks(self, **kwargs):
        """
        Retrieve all tasks.  Any kwargs are passed on as URL query string
        parameters.

        https://help.getharvest.com/api-v2/tasks-api/tasks/tasks/#list-all-tasks
        """
        response = self.get('/tasks', params=kwargs)
        return response.json()

    def get_time_entries(self, **kwargs):
        """
        List all time entries.  Any kwargs are passed on as URL query string
        parameters.

        https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#list-all-time-entries
        """
        response = self.get('/time_entries', params=kwargs)
        data = response.json()
        entries = data['time_entries']
        while data['next_page']:

            kw = dict(kwargs)
            kw['page'] = data['next_page']
            response = self.get('/time_entries', params=kw)
            data = response.json()
            entries.extend(data['time_entries'])

        return entries

    def get_time_entry(self, time_entry_id):
        """
        Retrieve a time entry.

        https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#retrieve-a-time-entry
        """
        try:
            response = self.get('/time_entries/{}'.format(time_entry_id))
        except requests.exceptions.HTTPError as error:
            if error.response.status_code != 404:
                raise
        else:
            return response.json()

    def create_time_entry(self, **kwargs):
        """
        Create a new time entry.  All kwargs are passed on as POST parameters.

        https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#create-a-time-entry-via-duration
        https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#create-a-time-entry-via-start-and-end-time
        """
        required = ('project_id', 'task_id', 'spent_date')
        for key in required:
            if key not in kwargs or not kwargs[key]:
                raise ValueError("must provide all of: {}".format(', '.join(required)))
        response = self.post('/time_entries', params=kwargs)
        return response.json()

    # TODO: deprecate / remove this
    put_time_entry = create_time_entry

    def stop_time_entry(self, time_entry_id):
        """
        Stop a running time entry.

        https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#stop-a-running-time-entry
        """
        response = self.patch('/time_entries/{}/stop'.format(time_entry_id))
        return response.json()

    def update_time_entry(self, time_entry_id, **kwargs):
        """
        Update a time entry.

        https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#update-a-time-entry
        """
        response = self.patch('/time_entries/{}'.format(time_entry_id), params=kwargs)
        return response.json()

    def delete_time_entry(self, time_entry_id, **kwargs):
        """
        Delete a time entry.

        https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#delete-a-time-entry
        """
        self.delete('/time_entries/{}'.format(time_entry_id), params=kwargs)


def make_harvest_webapi(config):
    access_token = config.require('harvest', 'api.access_token')
    account_id = config.require('harvest', 'api.account_id')
    user_agent = config.require('harvest', 'api.user_agent')
    return HarvestWebAPI(access_token=access_token,
                         account_id=account_id,
                         user_agent=user_agent)
