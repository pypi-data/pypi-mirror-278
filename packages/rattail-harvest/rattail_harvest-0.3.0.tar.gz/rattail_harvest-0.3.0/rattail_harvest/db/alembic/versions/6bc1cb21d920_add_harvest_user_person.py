# -*- coding: utf-8; -*-
"""add harvest_user.person

Revision ID: 6bc1cb21d920
Revises: 5505c0e60d28
Create Date: 2022-01-30 16:49:32.271745

"""

# revision identifiers, used by Alembic.
revision = '6bc1cb21d920'
down_revision = '5505c0e60d28'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # harvest_user
    op.add_column('harvest_user', sa.Column('person_uuid', sa.String(length=32), nullable=True))
    op.create_foreign_key('harvest_user_fk_person', 'harvest_user', 'person', ['person_uuid'], ['uuid'])
    op.add_column('harvest_user_version', sa.Column('person_uuid', sa.String(length=32), autoincrement=False, nullable=True))


def downgrade():

    # harvest_user
    op.drop_column('harvest_user_version', 'person_uuid')
    op.drop_constraint('harvest_user_fk_person', 'harvest_user', type_='foreignkey')
    op.drop_column('harvest_user', 'person_uuid')
