# -*- coding: utf-8; -*-
"""grow id fields

Revision ID: f2a1650e7fbc
Revises: 6bc1cb21d920
Create Date: 2023-08-08 10:53:56.013211

"""

# revision identifiers, used by Alembic.
revision = 'f2a1650e7fbc'
down_revision = '6bc1cb21d920'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types
from sqlalchemy.dialects import postgresql


def upgrade():

    # harvest_user
    op.alter_column('harvest_user', 'id', type_=sa.BigInteger())
    op.alter_column('harvest_user_version', 'id', type_=sa.BigInteger())

    # harvest_client
    op.alter_column('harvest_client', 'id', type_=sa.BigInteger())
    op.alter_column('harvest_client_version', 'id', type_=sa.BigInteger())

    # harvest_project
    op.alter_column('harvest_project', 'id', type_=sa.BigInteger())
    op.alter_column('harvest_project', 'client_id', type_=sa.BigInteger())
    op.alter_column('harvest_project_version', 'id', type_=sa.BigInteger())
    op.alter_column('harvest_project_version', 'client_id', type_=sa.BigInteger())

    # harvest_task
    op.alter_column('harvest_task', 'id', type_=sa.BigInteger())
    op.alter_column('harvest_task_version', 'id', type_=sa.BigInteger())

    # harvest_time_entry
    op.alter_column('harvest_time_entry', 'id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry', 'user_id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry', 'client_id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry', 'project_id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry', 'task_id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry', 'invoice_id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry_version', 'id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry_version', 'user_id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry_version', 'client_id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry_version', 'project_id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry_version', 'task_id', type_=sa.BigInteger())
    op.alter_column('harvest_time_entry_version', 'invoice_id', type_=sa.BigInteger())


def downgrade():

    # harvest_time_entry
    op.alter_column('harvest_time_entry_version', 'id', type_=sa.Integer())
    op.alter_column('harvest_time_entry_version', 'user_id', type_=sa.Integer())
    op.alter_column('harvest_time_entry_version', 'client_id', type_=sa.Integer())
    op.alter_column('harvest_time_entry_version', 'project_id', type_=sa.Integer())
    op.alter_column('harvest_time_entry_version', 'task_id', type_=sa.Integer())
    op.alter_column('harvest_time_entry_version', 'invoice_id', type_=sa.Integer())
    op.alter_column('harvest_time_entry', 'id', type_=sa.Integer())
    op.alter_column('harvest_time_entry', 'user_id', type_=sa.Integer())
    op.alter_column('harvest_time_entry', 'client_id', type_=sa.Integer())
    op.alter_column('harvest_time_entry', 'project_id', type_=sa.Integer())
    op.alter_column('harvest_time_entry', 'task_id', type_=sa.Integer())
    op.alter_column('harvest_time_entry', 'invoice_id', type_=sa.Integer())

    # harvest_task
    op.alter_column('harvest_task_version', 'id', type_=sa.Integer())
    op.alter_column('harvest_task', 'id', type_=sa.Integer())

    # harvest_project
    op.alter_column('harvest_project_version', 'id', type_=sa.Integer())
    op.alter_column('harvest_project_version', 'client_id', type_=sa.Integer())
    op.alter_column('harvest_project', 'id', type_=sa.Integer())
    op.alter_column('harvest_project', 'client_id', type_=sa.Integer())

    # harvest_client
    op.alter_column('harvest_client_version', 'id', type_=sa.Integer())
    op.alter_column('harvest_client', 'id', type_=sa.Integer())

    # harvest_user
    op.alter_column('harvest_user_version', 'id', type_=sa.Integer())
    op.alter_column('harvest_user', 'id', type_=sa.Integer())
