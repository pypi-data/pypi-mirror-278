# -*- coding: utf-8; -*-
"""add project.deleted

Revision ID: 5505c0e60d28
Revises: d59ce24c2f9f
Create Date: 2022-01-30 12:08:04.338229

"""

# revision identifiers, used by Alembic.
revision = '5505c0e60d28'
down_revision = 'd59ce24c2f9f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # harvest_project
    op.add_column('harvest_project', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('harvest_project_version', sa.Column('deleted', sa.Boolean(), autoincrement=False, nullable=True))


def downgrade():

    # harvest_project
    op.drop_column('harvest_project_version', 'deleted')
    op.drop_column('harvest_project', 'deleted')
