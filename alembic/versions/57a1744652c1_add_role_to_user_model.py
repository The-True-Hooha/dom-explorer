"""add role to user model

Revision ID: 57a1744652c1
Revises: 
Create Date: 2024-09-18 11:58:37.479300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57a1744652c1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sub_domain', sa.Column('name', sa.String(), nullable=True))
    op.drop_column('sub_domain', 'ctId')
    op.drop_column('sub_domain', 'issueName')
    op.add_column('user', sa.Column('role', sa.Enum('user', 'admin', 'support', 'other', name='roleenum'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    op.add_column('sub_domain', sa.Column('issueName', sa.VARCHAR(), nullable=True))
    op.add_column('sub_domain', sa.Column('ctId', sa.VARCHAR(), nullable=True))
    op.drop_column('sub_domain', 'name')
    # ### end Alembic commands ###
