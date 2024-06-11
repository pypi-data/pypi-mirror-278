# -*- coding: utf-8; -*-
"""initial Harvest tables

Revision ID: d59ce24c2f9f
Revises: d8b0ba4fa795
Create Date: 2022-01-29 11:54:34.940773

"""

# revision identifiers, used by Alembic.
revision = 'd59ce24c2f9f'
down_revision = None
branch_labels = ('rattail_harvest',)
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # harvest_user
    op.create_table('harvest_user',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('first_name', sa.String(length=255), nullable=True),
                    sa.Column('last_name', sa.String(length=255), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=True),
                    sa.Column('telephone', sa.String(length=255), nullable=True),
                    sa.Column('timezone', sa.String(length=255), nullable=True),
                    sa.Column('has_access_to_all_future_projects', sa.Boolean(), nullable=True),
                    sa.Column('is_contractor', sa.Boolean(), nullable=True),
                    sa.Column('is_admin', sa.Boolean(), nullable=True),
                    sa.Column('is_project_manager', sa.Boolean(), nullable=True),
                    sa.Column('can_see_rates', sa.Boolean(), nullable=True),
                    sa.Column('can_create_projects', sa.Boolean(), nullable=True),
                    sa.Column('can_create_invoices', sa.Boolean(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.Column('weekly_capacity', sa.Integer(), nullable=True),
                    sa.Column('default_hourly_rate', sa.Numeric(precision=6, scale=2), nullable=True),
                    sa.Column('cost_rate', sa.Numeric(precision=6, scale=2), nullable=True),
                    sa.Column('avatar_url', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('id', name='harvest_user_uq_id')
    )
    op.create_table('harvest_user_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('first_name', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('last_name', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('name', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('email', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('telephone', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('timezone', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('has_access_to_all_future_projects', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('is_contractor', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('is_admin', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('is_project_manager', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('can_see_rates', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('can_create_projects', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('can_create_invoices', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('is_active', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('weekly_capacity', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('default_hourly_rate', sa.Numeric(precision=6, scale=2), autoincrement=False, nullable=True),
                    sa.Column('cost_rate', sa.Numeric(precision=6, scale=2), autoincrement=False, nullable=True),
                    sa.Column('avatar_url', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('created_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('updated_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_harvest_user_version_end_transaction_id'), 'harvest_user_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_harvest_user_version_operation_type'), 'harvest_user_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_harvest_user_version_transaction_id'), 'harvest_user_version', ['transaction_id'], unique=False)

    # harvest_client
    op.create_table('harvest_client',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.Column('address', sa.String(length=255), nullable=True),
                    sa.Column('currency', sa.String(length=100), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('id', name='harvest_client_uq_id')
    )
    op.create_table('harvest_client_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('name', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('is_active', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('address', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('currency', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('created_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('updated_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_harvest_client_version_end_transaction_id'), 'harvest_client_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_harvest_client_version_operation_type'), 'harvest_client_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_harvest_client_version_transaction_id'), 'harvest_client_version', ['transaction_id'], unique=False)

    # harvest_project
    op.create_table('harvest_project',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('client_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('code', sa.String(length=100), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.Column('is_billable', sa.Boolean(), nullable=True),
                    sa.Column('is_fixed_fee', sa.Boolean(), nullable=True),
                    sa.Column('bill_by', sa.String(length=100), nullable=True),
                    sa.Column('hourly_rate', sa.Numeric(precision=6, scale=2), nullable=True),
                    sa.Column('budget', sa.Numeric(precision=6, scale=2), nullable=True),
                    sa.Column('budget_by', sa.String(length=100), nullable=True),
                    sa.Column('budget_is_monthly', sa.Boolean(), nullable=True),
                    sa.Column('notify_when_over_budget', sa.Boolean(), nullable=True),
                    sa.Column('over_budget_notification_percentage', sa.Numeric(precision=6, scale=2), nullable=True),
                    sa.Column('over_budget_notification_date', sa.Date(), nullable=True),
                    sa.Column('show_budget_to_all', sa.Boolean(), nullable=True),
                    sa.Column('cost_budget', sa.Numeric(precision=9, scale=2), nullable=True),
                    sa.Column('cost_budget_include_expenses', sa.Boolean(), nullable=True),
                    sa.Column('fee', sa.Numeric(precision=8, scale=2), nullable=True),
                    sa.Column('notes', sa.Text(), nullable=True),
                    sa.Column('starts_on', sa.Date(), nullable=True),
                    sa.Column('ends_on', sa.Date(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['client_id'], ['harvest_client.id'], name='harvest_project_fk_client'),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('id', name='harvest_project_uq_id')
    )
    op.create_table('harvest_project_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('client_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('name', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('code', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('is_active', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('is_billable', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('is_fixed_fee', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('bill_by', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('hourly_rate', sa.Numeric(precision=6, scale=2), autoincrement=False, nullable=True),
                    sa.Column('budget', sa.Numeric(precision=6, scale=2), autoincrement=False, nullable=True),
                    sa.Column('budget_by', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('budget_is_monthly', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('notify_when_over_budget', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('over_budget_notification_percentage', sa.Numeric(precision=6, scale=2), autoincrement=False, nullable=True),
                    sa.Column('show_budget_to_all', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('cost_budget', sa.Numeric(precision=9, scale=2), autoincrement=False, nullable=True),
                    sa.Column('cost_budget_include_expenses', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('fee', sa.Numeric(precision=8, scale=2), autoincrement=False, nullable=True),
                    sa.Column('notes', sa.Text(), autoincrement=False, nullable=True),
                    sa.Column('starts_on', sa.Date(), autoincrement=False, nullable=True),
                    sa.Column('ends_on', sa.Date(), autoincrement=False, nullable=True),
                    sa.Column('created_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('updated_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_harvest_project_version_end_transaction_id'), 'harvest_project_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_harvest_project_version_operation_type'), 'harvest_project_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_harvest_project_version_transaction_id'), 'harvest_project_version', ['transaction_id'], unique=False)

    # harvest_task
    op.create_table('harvest_task',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('billable_by_default', sa.Boolean(), nullable=True),
                    sa.Column('default_hourly_rate', sa.Numeric(precision=6, scale=2), nullable=True),
                    sa.Column('is_default', sa.Boolean(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('id', name='harvest_task_uq_id')
    )
    op.create_table('harvest_task_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('name', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('billable_by_default', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('default_hourly_rate', sa.Numeric(precision=6, scale=2), autoincrement=False, nullable=True),
                    sa.Column('is_default', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('is_active', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('created_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('updated_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_harvest_task_version_end_transaction_id'), 'harvest_task_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_harvest_task_version_operation_type'), 'harvest_task_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_harvest_task_version_transaction_id'), 'harvest_task_version', ['transaction_id'], unique=False)

    # harvest_time_entry
    op.create_table('harvest_time_entry',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('spent_date', sa.Date(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('client_id', sa.Integer(), nullable=True),
                    sa.Column('project_id', sa.Integer(), nullable=True),
                    sa.Column('task_id', sa.Integer(), nullable=True),
                    sa.Column('invoice_id', sa.Integer(), nullable=True),
                    sa.Column('hours', sa.Numeric(precision=6, scale=2), nullable=True),
                    sa.Column('notes', sa.Text(), nullable=True),
                    sa.Column('is_locked', sa.Boolean(), nullable=True),
                    sa.Column('locked_reason', sa.String(length=255), nullable=True),
                    sa.Column('is_closed', sa.Boolean(), nullable=True),
                    sa.Column('is_billed', sa.Boolean(), nullable=True),
                    sa.Column('timer_started_at', sa.DateTime(), nullable=True),
                    sa.Column('started_time', sa.DateTime(), nullable=True),
                    sa.Column('ended_time', sa.DateTime(), nullable=True),
                    sa.Column('is_running', sa.Boolean(), nullable=True),
                    sa.Column('billable', sa.Boolean(), nullable=True),
                    sa.Column('budgeted', sa.Boolean(), nullable=True),
                    sa.Column('billable_rate', sa.Numeric(precision=6, scale=2), nullable=True),
                    sa.Column('cost_rate', sa.Numeric(precision=6, scale=2), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['client_id'], ['harvest_client.id'], name='harvest_time_entry_fk_client'),
                    sa.ForeignKeyConstraint(['project_id'], ['harvest_project.id'], name='harvest_time_entry_fk_project'),
                    sa.ForeignKeyConstraint(['task_id'], ['harvest_task.id'], name='harvest_time_entry_fk_task'),
                    sa.ForeignKeyConstraint(['user_id'], ['harvest_user.id'], name='harvest_time_entry_fk_user'),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('id', name='harvest_time_entry_uq_id')
    )
    op.create_table('harvest_time_entry_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('spent_date', sa.Date(), autoincrement=False, nullable=True),
                    sa.Column('user_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('client_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('project_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('task_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('invoice_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('hours', sa.Numeric(precision=6, scale=2), autoincrement=False, nullable=True),
                    sa.Column('notes', sa.Text(), autoincrement=False, nullable=True),
                    sa.Column('is_locked', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('locked_reason', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('is_closed', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('is_billed', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('timer_started_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('started_time', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('ended_time', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('is_running', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('billable', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('budgeted', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('billable_rate', sa.Numeric(precision=6, scale=2), autoincrement=False, nullable=True),
                    sa.Column('cost_rate', sa.Numeric(precision=6, scale=2), autoincrement=False, nullable=True),
                    sa.Column('created_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('updated_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_harvest_time_entry_version_end_transaction_id'), 'harvest_time_entry_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_harvest_time_entry_version_operation_type'), 'harvest_time_entry_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_harvest_time_entry_version_transaction_id'), 'harvest_time_entry_version', ['transaction_id'], unique=False)


def downgrade():

    # harvest_time_entry
    op.drop_index(op.f('ix_harvest_time_entry_version_transaction_id'), table_name='harvest_time_entry_version')
    op.drop_index(op.f('ix_harvest_time_entry_version_operation_type'), table_name='harvest_time_entry_version')
    op.drop_index(op.f('ix_harvest_time_entry_version_end_transaction_id'), table_name='harvest_time_entry_version')
    op.drop_table('harvest_time_entry_version')
    op.drop_table('harvest_time_entry')

    # harvest_task
    op.drop_index(op.f('ix_harvest_task_version_transaction_id'), table_name='harvest_task_version')
    op.drop_index(op.f('ix_harvest_task_version_operation_type'), table_name='harvest_task_version')
    op.drop_index(op.f('ix_harvest_task_version_end_transaction_id'), table_name='harvest_task_version')
    op.drop_table('harvest_task_version')
    op.drop_table('harvest_task')

    # harvest_project
    op.drop_index(op.f('ix_harvest_project_version_transaction_id'), table_name='harvest_project_version')
    op.drop_index(op.f('ix_harvest_project_version_operation_type'), table_name='harvest_project_version')
    op.drop_index(op.f('ix_harvest_project_version_end_transaction_id'), table_name='harvest_project_version')
    op.drop_table('harvest_project_version')
    op.drop_table('harvest_project')

    # harvest_client
    op.drop_index(op.f('ix_harvest_client_version_transaction_id'), table_name='harvest_client_version')
    op.drop_index(op.f('ix_harvest_client_version_operation_type'), table_name='harvest_client_version')
    op.drop_index(op.f('ix_harvest_client_version_end_transaction_id'), table_name='harvest_client_version')
    op.drop_table('harvest_client_version')
    op.drop_table('harvest_client')

    # harvest_user
    op.drop_index(op.f('ix_harvest_user_version_transaction_id'), table_name='harvest_user_version')
    op.drop_index(op.f('ix_harvest_user_version_operation_type'), table_name='harvest_user_version')
    op.drop_index(op.f('ix_harvest_user_version_end_transaction_id'), table_name='harvest_user_version')
    op.drop_table('harvest_user_version')
    op.drop_table('harvest_user')
