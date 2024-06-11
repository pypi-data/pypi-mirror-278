# -*- coding: utf-8; -*-
"""rename cache tables

Revision ID: 53c066772ad5
Revises: f2a1650e7fbc
Create Date: 2023-10-04 15:19:03.857323

"""

# revision identifiers, used by Alembic.
revision = '53c066772ad5'
down_revision = 'f2a1650e7fbc'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    ##############################
    # drop all constraints
    ##############################

    # harvest_time_entry
    op.drop_constraint('harvest_time_entry_fk_user', 'harvest_time_entry', type_='foreignkey')
    op.drop_constraint('harvest_time_entry_fk_client', 'harvest_time_entry', type_='foreignkey')
    op.drop_constraint('harvest_time_entry_fk_project', 'harvest_time_entry', type_='foreignkey')
    op.drop_constraint('harvest_time_entry_fk_task', 'harvest_time_entry', type_='foreignkey')
    op.drop_constraint('harvest_time_entry_uq_id', 'harvest_time_entry', type_='unique')

    # harvest_task
    op.drop_constraint('harvest_task_uq_id', 'harvest_task', type_='unique')

    # harvest_project
    op.drop_constraint('harvest_project_fk_client', 'harvest_project', type_='foreignkey')
    op.drop_constraint('harvest_project_uq_id', 'harvest_project', type_='unique')

    # harvest_client
    op.drop_constraint('harvest_client_uq_id', 'harvest_client', type_='unique')

    # harvest_user
    op.drop_constraint('harvest_user_fk_person', 'harvest_user', type_='foreignkey')
    op.drop_constraint('harvest_user_uq_id', 'harvest_user', type_='unique')

    ##############################
    # rename all tables
    ##############################

    op.rename_table('harvest_user', 'harvest_cache_user')
    op.rename_table('harvest_user_version', 'harvest_cache_user_version')
    op.rename_table('harvest_client', 'harvest_cache_client')
    op.rename_table('harvest_client_version', 'harvest_cache_client_version')
    op.rename_table('harvest_project', 'harvest_cache_project')
    op.rename_table('harvest_project_version', 'harvest_cache_project_version')
    op.rename_table('harvest_task', 'harvest_cache_task')
    op.rename_table('harvest_task_version', 'harvest_cache_task_version')
    op.rename_table('harvest_time_entry', 'harvest_cache_time_entry')
    op.rename_table('harvest_time_entry_version', 'harvest_cache_time_entry_version')

    ##############################
    # re-create all constraints
    ##############################

    # harvest_cache_user
    op.create_foreign_key('harvest_cache_user_fk_person',
                          'harvest_cache_user', 'person',
                          ['person_uuid'], ['uuid'])
    op.create_unique_constraint('harvest_cache_user_uq_id', 'harvest_cache_user', ['id'])

    # harvest_cache_client
    op.create_unique_constraint('harvest_cache_client_uq_id', 'harvest_cache_client', ['id'])

    # harvest_cache_project
    op.create_foreign_key('harvest_cache_project_fk_client',
                          'harvest_cache_project', 'harvest_cache_client',
                          ['client_id'], ['id'])
    op.create_unique_constraint('harvest_cache_project_uq_id', 'harvest_cache_project', ['id'])

    # harvest_cache_task
    op.create_unique_constraint('harvest_cache_task_uq_id', 'harvest_cache_task', ['id'])

    # harvest_cache_time_entry
    op.create_foreign_key('harvest_cache_time_entry_fk_user',
                          'harvest_cache_time_entry', 'harvest_cache_user',
                          ['user_id'], ['id'])
    op.create_foreign_key('harvest_cache_time_entry_fk_client',
                          'harvest_cache_time_entry', 'harvest_cache_client',
                          ['client_id'], ['id'])
    op.create_foreign_key('harvest_cache_time_entry_fk_project',
                          'harvest_cache_time_entry', 'harvest_cache_project',
                          ['project_id'], ['id'])
    op.create_foreign_key('harvest_cache_time_entry_fk_task',
                          'harvest_cache_time_entry', 'harvest_cache_task',
                          ['task_id'], ['id'])
    op.create_unique_constraint('harvest_cache_time_entry_uq_id', 'harvest_cache_time_entry', ['id'])


def downgrade():

    ##############################
    # drop all constraints
    ##############################

    # harvest_cache_time_entry
    op.drop_constraint('harvest_cache_time_entry_fk_user', 'harvest_cache_time_entry', type_='foreignkey')
    op.drop_constraint('harvest_cache_time_entry_fk_client', 'harvest_cache_time_entry', type_='foreignkey')
    op.drop_constraint('harvest_cache_time_entry_fk_project', 'harvest_cache_time_entry', type_='foreignkey')
    op.drop_constraint('harvest_cache_time_entry_fk_task', 'harvest_cache_time_entry', type_='foreignkey')
    op.drop_constraint('harvest_cache_time_entry_uq_id', 'harvest_cache_time_entry', type_='unique')

    # harvest_cache_task
    op.drop_constraint('harvest_cache_task_uq_id', 'harvest_cache_task', type_='unique')

    # harvest_cache_project
    op.drop_constraint('harvest_cache_project_fk_client', 'harvest_cache_project', type_='foreignkey')
    op.drop_constraint('harvest_cache_project_uq_id', 'harvest_cache_project', type_='unique')

    # harvest_cache_client
    op.drop_constraint('harvest_cache_client_uq_id', 'harvest_cache_client', type_='unique')

    # harvest_cache_user
    op.drop_constraint('harvest_cache_user_fk_person', 'harvest_cache_user', type_='foreignkey')
    op.drop_constraint('harvest_cache_user_uq_id', 'harvest_cache_user', type_='unique')

    ##############################
    # rename all tables
    ##############################

    op.rename_table('harvest_cache_user', 'harvest_user')
    op.rename_table('harvest_cache_user_version', 'harvest_user_version')
    op.rename_table('harvest_cache_client', 'harvest_client')
    op.rename_table('harvest_cache_client_version', 'harvest_client_version')
    op.rename_table('harvest_cache_project', 'harvest_project')
    op.rename_table('harvest_cache_project_version', 'harvest_project_version')
    op.rename_table('harvest_cache_task', 'harvest_task')
    op.rename_table('harvest_cache_task_version', 'harvest_task_version')
    op.rename_table('harvest_cache_time_entry', 'harvest_time_entry')
    op.rename_table('harvest_cache_time_entry_version', 'harvest_time_entry_version')

    ##############################
    # re-create all constraints
    ##############################

    # harvest_user
    op.create_foreign_key('harvest_user_fk_person',
                          'harvest_user', 'person',
                          ['person_uuid'], ['uuid'])
    op.create_unique_constraint('harvest_user_uq_id', 'harvest_user', ['id'])

    # harvest_client
    op.create_unique_constraint('harvest_client_uq_id', 'harvest_client', ['id'])

    # harvest_project
    op.create_foreign_key('harvest_project_fk_client',
                          'harvest_project', 'harvest_client',
                          ['client_id'], ['id'])
    op.create_unique_constraint('harvest_project_uq_id', 'harvest_project', ['id'])

    # harvest_cache_task
    op.create_unique_constraint('harvest_task_uq_id', 'harvest_task', ['id'])

    # harvest_time_entry
    op.create_foreign_key('harvest_time_entry_fk_user',
                          'harvest_time_entry', 'harvest_user',
                          ['user_id'], ['id'])
    op.create_foreign_key('harvest_time_entry_fk_client',
                          'harvest_time_entry', 'harvest_client',
                          ['client_id'], ['id'])
    op.create_foreign_key('harvest_time_entry_fk_project',
                          'harvest_time_entry', 'harvest_project',
                          ['project_id'], ['id'])
    op.create_foreign_key('harvest_time_entry_fk_task',
                          'harvest_time_entry', 'harvest_task',
                          ['task_id'], ['id'])
    op.create_unique_constraint('harvest_time_entry_uq_id', 'harvest_time_entry', ['id'])
