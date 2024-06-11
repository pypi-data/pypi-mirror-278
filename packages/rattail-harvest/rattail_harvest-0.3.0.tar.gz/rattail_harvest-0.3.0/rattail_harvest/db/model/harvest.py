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
Harvest "cache" data models
"""

import warnings

import sqlalchemy as sa
from sqlalchemy import orm

from rattail.db import model
from rattail.db.util import normalize_full_name


class HarvestCacheUser(model.Base):
    """
    Represents a user record in Harvest.

    https://help.getharvest.com/api-v2/users-api/users/users/#the-user-object
    """
    __tablename__ = 'harvest_cache_user'
    __table_args__ = (
        sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid'],
                                name='harvest_cache_user_fk_person'),
        sa.UniqueConstraint('id', name='harvest_cache_user_uq_id'),
    )
    __versioned__ = {}

    uuid = model.uuid_column()

    id = sa.Column(sa.BigInteger(), nullable=False)

    first_name = sa.Column(sa.String(length=255), nullable=True)

    last_name = sa.Column(sa.String(length=255), nullable=True)

    name = sa.Column(sa.String(length=255), nullable=True)

    email = sa.Column(sa.String(length=255), nullable=True)

    telephone = sa.Column(sa.String(length=255), nullable=True)

    timezone = sa.Column(sa.String(length=255), nullable=True)

    has_access_to_all_future_projects = sa.Column(sa.Boolean(), nullable=True)

    is_contractor = sa.Column(sa.Boolean(), nullable=True)

    is_admin = sa.Column(sa.Boolean(), nullable=True)

    is_project_manager = sa.Column(sa.Boolean(), nullable=True)

    can_see_rates = sa.Column(sa.Boolean(), nullable=True)

    can_create_projects = sa.Column(sa.Boolean(), nullable=True)

    can_create_invoices = sa.Column(sa.Boolean(), nullable=True)

    is_active = sa.Column(sa.Boolean(), nullable=True)

    weekly_capacity = sa.Column(sa.Integer(), nullable=True)

    default_hourly_rate = sa.Column(sa.Numeric(precision=6, scale=2), nullable=True)

    cost_rate = sa.Column(sa.Numeric(precision=6, scale=2), nullable=True)

    # TODO
    # roles = sa.Column(sa.Text(), nullable=True)

    avatar_url = sa.Column(sa.String(length=255), nullable=True)

    created_at = sa.Column(sa.DateTime(), nullable=True)

    updated_at = sa.Column(sa.DateTime(), nullable=True)

    person_uuid = sa.Column(sa.String(length=32), nullable=True)
    person = orm.relationship(
        model.Person,
        doc="""
        Reference to the person associated with this Harvest user.
        """,
        backref=orm.backref(
            'harvest_users',
            doc="""
            List of all Harvest user accounts for the person.
            """)
    )

    def __str__(self):
        return normalize_full_name(self.first_name, self.last_name)


class HarvestCacheClient(model.Base):
    """
    Represents a client record in Harvest.

    https://help.getharvest.com/api-v2/clients-api/clients/clients/#the-client-object
    """
    __tablename__ = 'harvest_cache_client'
    __table_args__ = (
        sa.UniqueConstraint('id', name='harvest_cache_client_uq_id'),
    )
    __versioned__ = {}

    uuid = model.uuid_column()

    id = sa.Column(sa.BigInteger(), nullable=False)

    name = sa.Column(sa.String(length=255), nullable=True)

    is_active = sa.Column(sa.Boolean(), nullable=True)

    address = sa.Column(sa.String(length=255), nullable=True)

    currency = sa.Column(sa.String(length=100), nullable=True)

    created_at = sa.Column(sa.DateTime(), nullable=True)

    updated_at = sa.Column(sa.DateTime(), nullable=True)

    def __str__(self):
        return self.name or ''


class HarvestCacheProject(model.Base):
    """
    Represents a project record in Harvest.

    https://help.getharvest.com/api-v2/projects-api/projects/projects/#the-project-object
    """
    __tablename__ = 'harvest_cache_project'
    __table_args__ = (
        sa.UniqueConstraint('id', name='harvest_cache_project_uq_id'),
        sa.ForeignKeyConstraint(['client_id'], ['harvest_cache_client.id'],
                                name='harvest_cache_project_fk_client'),
    )
    __versioned__ = {'exclude': ['over_budget_notification_date']}

    uuid = model.uuid_column()

    id = sa.Column(sa.BigInteger(), nullable=False)

    client_id = sa.Column(sa.BigInteger(), nullable=True) # TODO: should not allow null?
    client = orm.relationship(HarvestCacheClient, backref=orm.backref('projects'))

    name = sa.Column(sa.String(length=255), nullable=True)

    code = sa.Column(sa.String(length=100), nullable=True)

    is_active = sa.Column(sa.Boolean(), nullable=True)

    is_billable = sa.Column(sa.Boolean(), nullable=True)

    is_fixed_fee = sa.Column(sa.Boolean(), nullable=True)

    bill_by = sa.Column(sa.String(length=100), nullable=True)

    hourly_rate = sa.Column(sa.Numeric(precision=6, scale=2), nullable=True)

    budget = sa.Column(sa.Numeric(precision=6, scale=2), nullable=True)

    budget_by = sa.Column(sa.String(length=100), nullable=True)

    budget_is_monthly = sa.Column(sa.Boolean(), nullable=True)

    notify_when_over_budget = sa.Column(sa.Boolean(), nullable=True)

    over_budget_notification_percentage = sa.Column(sa.Numeric(precision=6, scale=2), nullable=True)

    over_budget_notification_date = sa.Column(sa.Date(), nullable=True)

    show_budget_to_all = sa.Column(sa.Boolean(), nullable=True)

    cost_budget = sa.Column(sa.Numeric(precision=9, scale=2), nullable=True)

    cost_budget_include_expenses = sa.Column(sa.Boolean(), nullable=True)

    fee = sa.Column(sa.Numeric(precision=8, scale=2), nullable=True)

    notes = sa.Column(sa.Text(), nullable=True)

    starts_on = sa.Column(sa.Date(), nullable=True)

    ends_on = sa.Column(sa.Date(), nullable=True)

    created_at = sa.Column(sa.DateTime(), nullable=True)

    updated_at = sa.Column(sa.DateTime(), nullable=True)

    deleted = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating the record has been deleted in Harvest.
    """)

    def __str__(self):
        return self.name or ''


class HarvestCacheTask(model.Base):
    """
    Represents a task record in Harvest.

    https://help.getharvest.com/api-v2/tasks-api/tasks/tasks/#the-task-object
    """
    __tablename__ = 'harvest_cache_task'
    __table_args__ = (
        sa.UniqueConstraint('id', name='harvest_cache_task_uq_id'),
    )
    __versioned__ = {}

    uuid = model.uuid_column()

    id = sa.Column(sa.BigInteger(), nullable=False)

    name = sa.Column(sa.String(length=255), nullable=True)

    billable_by_default = sa.Column(sa.Boolean(), nullable=True)

    default_hourly_rate = sa.Column(sa.Numeric(precision=6, scale=2), nullable=True)

    is_default = sa.Column(sa.Boolean(), nullable=True)

    is_active = sa.Column(sa.Boolean(), nullable=True)

    created_at = sa.Column(sa.DateTime(), nullable=True)

    updated_at = sa.Column(sa.DateTime(), nullable=True)

    def __str__(self):
        return self.name or ''


class HarvestCacheTimeEntry(model.Base):
    """
    Represents a time entry record in Harvest.

    https://help.getharvest.com/api-v2/timesheets-api/timesheets/time-entries/#the-time-entry-object
    """
    __tablename__ = 'harvest_cache_time_entry'
    __table_args__ = (
        sa.UniqueConstraint('id', name='harvest_cache_time_entry_uq_id'),
        sa.ForeignKeyConstraint(['user_id'], ['harvest_cache_user.id'],
                                name='harvest_cache_time_entry_fk_user'),
        sa.ForeignKeyConstraint(['client_id'], ['harvest_cache_client.id'],
                                name='harvest_cache_time_entry_fk_client'),
        sa.ForeignKeyConstraint(['project_id'], ['harvest_cache_project.id'],
                                name='harvest_cache_time_entry_fk_project'),
        sa.ForeignKeyConstraint(['task_id'], ['harvest_cache_task.id'],
                                name='harvest_cache_time_entry_fk_task'),
    )
    __versioned__ = {}
    model_title_plural = "Harvest Time Entries"

    uuid = model.uuid_column()

    id = sa.Column(sa.BigInteger(), nullable=False)

    spent_date = sa.Column(sa.Date(), nullable=True)

    user_id = sa.Column(sa.BigInteger(), nullable=True)
    user = orm.relationship(HarvestCacheUser, backref=orm.backref('time_entries'))

    client_id = sa.Column(sa.BigInteger(), nullable=True)
    client = orm.relationship(HarvestCacheClient, backref=orm.backref('time_entries'))

    project_id = sa.Column(sa.BigInteger(), nullable=True)
    project = orm.relationship(HarvestCacheProject, backref=orm.backref('time_entries'))

    task_id = sa.Column(sa.BigInteger(), nullable=True)
    task = orm.relationship(HarvestCacheTask, backref=orm.backref('time_entries'))

    invoice_id = sa.Column(sa.BigInteger(), nullable=True)

    hours = sa.Column(sa.Numeric(precision=6, scale=2), nullable=True)

    notes = sa.Column(sa.Text(), nullable=True)

    is_locked = sa.Column(sa.Boolean(), nullable=True)

    locked_reason = sa.Column(sa.String(length=255), nullable=True)

    is_closed = sa.Column(sa.Boolean(), nullable=True)

    is_billed = sa.Column(sa.Boolean(), nullable=True)

    timer_started_at = sa.Column(sa.DateTime(), nullable=True)

    started_time = sa.Column(sa.DateTime(), nullable=True)

    ended_time = sa.Column(sa.DateTime(), nullable=True)

    is_running = sa.Column(sa.Boolean(), nullable=True)

    billable = sa.Column(sa.Boolean(), nullable=True)

    budgeted = sa.Column(sa.Boolean(), nullable=True)

    billable_rate = sa.Column(sa.Numeric(precision=6, scale=2), nullable=True)

    cost_rate = sa.Column(sa.Numeric(precision=6, scale=2), nullable=True)

    created_at = sa.Column(sa.DateTime(), nullable=True)

    updated_at = sa.Column(sa.DateTime(), nullable=True)

    def __str__(self):
        return str(self.spent_date or '')
