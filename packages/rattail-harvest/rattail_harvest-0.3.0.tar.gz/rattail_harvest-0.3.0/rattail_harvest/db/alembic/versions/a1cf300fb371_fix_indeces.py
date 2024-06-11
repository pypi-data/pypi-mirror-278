# -*- coding: utf-8; -*-
"""fix indeces

Revision ID: a1cf300fb371
Revises: 53c066772ad5
Create Date: 2023-10-23 17:35:15.527740

"""

# revision identifiers, used by Alembic.
revision = 'a1cf300fb371'
down_revision = '53c066772ad5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # harvest_cache_user
    op.drop_index('ix_harvest_user_version_end_transaction_id', table_name='harvest_cache_user_version')
    op.drop_index('ix_harvest_user_version_operation_type', table_name='harvest_cache_user_version')
    op.drop_index('ix_harvest_user_version_transaction_id', table_name='harvest_cache_user_version')
    op.create_index(op.f('ix_harvest_cache_user_version_end_transaction_id'), 'harvest_cache_user_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_harvest_cache_user_version_operation_type'), 'harvest_cache_user_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_harvest_cache_user_version_transaction_id'), 'harvest_cache_user_version', ['transaction_id'], unique=False)

    # harvest_cache_client
    op.drop_index('ix_harvest_client_version_end_transaction_id', table_name='harvest_cache_client_version')
    op.drop_index('ix_harvest_client_version_operation_type', table_name='harvest_cache_client_version')
    op.drop_index('ix_harvest_client_version_transaction_id', table_name='harvest_cache_client_version')
    op.create_index(op.f('ix_harvest_cache_client_version_end_transaction_id'), 'harvest_cache_client_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_harvest_cache_client_version_operation_type'), 'harvest_cache_client_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_harvest_cache_client_version_transaction_id'), 'harvest_cache_client_version', ['transaction_id'], unique=False)

    # harvest_cache_project
    op.drop_index('ix_harvest_project_version_end_transaction_id', table_name='harvest_cache_project_version')
    op.drop_index('ix_harvest_project_version_operation_type', table_name='harvest_cache_project_version')
    op.drop_index('ix_harvest_project_version_transaction_id', table_name='harvest_cache_project_version')
    op.create_index(op.f('ix_harvest_cache_project_version_end_transaction_id'), 'harvest_cache_project_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_harvest_cache_project_version_operation_type'), 'harvest_cache_project_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_harvest_cache_project_version_transaction_id'), 'harvest_cache_project_version', ['transaction_id'], unique=False)

    # harvest_cache_task
    op.drop_index('ix_harvest_task_version_end_transaction_id', table_name='harvest_cache_task_version')
    op.drop_index('ix_harvest_task_version_operation_type', table_name='harvest_cache_task_version')
    op.drop_index('ix_harvest_task_version_transaction_id', table_name='harvest_cache_task_version')
    op.create_index(op.f('ix_harvest_cache_task_version_end_transaction_id'), 'harvest_cache_task_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_harvest_cache_task_version_operation_type'), 'harvest_cache_task_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_harvest_cache_task_version_transaction_id'), 'harvest_cache_task_version', ['transaction_id'], unique=False)

    # harvest_cache_time_entry
    op.drop_index('ix_harvest_time_entry_version_end_transaction_id', table_name='harvest_cache_time_entry_version')
    op.drop_index('ix_harvest_time_entry_version_operation_type', table_name='harvest_cache_time_entry_version')
    op.drop_index('ix_harvest_time_entry_version_transaction_id', table_name='harvest_cache_time_entry_version')
    op.create_index(op.f('ix_harvest_cache_time_entry_version_end_transaction_id'), 'harvest_cache_time_entry_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_harvest_cache_time_entry_version_operation_type'), 'harvest_cache_time_entry_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_harvest_cache_time_entry_version_transaction_id'), 'harvest_cache_time_entry_version', ['transaction_id'], unique=False)


def downgrade():

    # harvest_cache_time_entry
    op.drop_index(op.f('ix_harvest_cache_time_entry_version_transaction_id'), table_name='harvest_cache_time_entry_version')
    op.drop_index(op.f('ix_harvest_cache_time_entry_version_operation_type'), table_name='harvest_cache_time_entry_version')
    op.drop_index(op.f('ix_harvest_cache_time_entry_version_end_transaction_id'), table_name='harvest_cache_time_entry_version')
    op.create_index('ix_harvest_time_entry_version_transaction_id', 'harvest_cache_time_entry_version', ['transaction_id'], unique=False)
    op.create_index('ix_harvest_time_entry_version_operation_type', 'harvest_cache_time_entry_version', ['operation_type'], unique=False)
    op.create_index('ix_harvest_time_entry_version_end_transaction_id', 'harvest_cache_time_entry_version', ['end_transaction_id'], unique=False)

    # harvest_cache_task
    op.drop_index(op.f('ix_harvest_cache_task_version_transaction_id'), table_name='harvest_cache_task_version')
    op.drop_index(op.f('ix_harvest_cache_task_version_operation_type'), table_name='harvest_cache_task_version')
    op.drop_index(op.f('ix_harvest_cache_task_version_end_transaction_id'), table_name='harvest_cache_task_version')
    op.create_index('ix_harvest_task_version_transaction_id', 'harvest_cache_task_version', ['transaction_id'], unique=False)
    op.create_index('ix_harvest_task_version_operation_type', 'harvest_cache_task_version', ['operation_type'], unique=False)
    op.create_index('ix_harvest_task_version_end_transaction_id', 'harvest_cache_task_version', ['end_transaction_id'], unique=False)

    # harvest_cache_project
    op.drop_index(op.f('ix_harvest_cache_project_version_transaction_id'), table_name='harvest_cache_project_version')
    op.drop_index(op.f('ix_harvest_cache_project_version_operation_type'), table_name='harvest_cache_project_version')
    op.drop_index(op.f('ix_harvest_cache_project_version_end_transaction_id'), table_name='harvest_cache_project_version')
    op.create_index('ix_harvest_project_version_transaction_id', 'harvest_cache_project_version', ['transaction_id'], unique=False)
    op.create_index('ix_harvest_project_version_operation_type', 'harvest_cache_project_version', ['operation_type'], unique=False)
    op.create_index('ix_harvest_project_version_end_transaction_id', 'harvest_cache_project_version', ['end_transaction_id'], unique=False)

    # harvest_cache_client
    op.drop_index(op.f('ix_harvest_cache_client_version_transaction_id'), table_name='harvest_cache_client_version')
    op.drop_index(op.f('ix_harvest_cache_client_version_operation_type'), table_name='harvest_cache_client_version')
    op.drop_index(op.f('ix_harvest_cache_client_version_end_transaction_id'), table_name='harvest_cache_client_version')
    op.create_index('ix_harvest_client_version_transaction_id', 'harvest_cache_client_version', ['transaction_id'], unique=False)
    op.create_index('ix_harvest_client_version_operation_type', 'harvest_cache_client_version', ['operation_type'], unique=False)
    op.create_index('ix_harvest_client_version_end_transaction_id', 'harvest_cache_client_version', ['end_transaction_id'], unique=False)

    # harvest_cache_user
    op.drop_index(op.f('ix_harvest_cache_user_version_transaction_id'), table_name='harvest_cache_user_version')
    op.drop_index(op.f('ix_harvest_cache_user_version_operation_type'), table_name='harvest_cache_user_version')
    op.drop_index(op.f('ix_harvest_cache_user_version_end_transaction_id'), table_name='harvest_cache_user_version')
    op.create_index('ix_harvest_user_version_transaction_id', 'harvest_cache_user_version', ['transaction_id'], unique=False)
    op.create_index('ix_harvest_user_version_operation_type', 'harvest_cache_user_version', ['operation_type'], unique=False)
    op.create_index('ix_harvest_user_version_end_transaction_id', 'harvest_cache_user_version', ['end_transaction_id'], unique=False)
