"""add output field to result

Revision ID: f7ef5f4d0d96
Revises: 39f5ba7540ce
Create Date: 2025-07-06 17:24:50.022748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7ef5f4d0d96'
down_revision: Union[str, None] = '39f5ba7540ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('output', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('results', 'output')
    # ### end Alembic commands ###
