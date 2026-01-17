"""Create phone number for User column

Revision ID: 56c5478f35eb
Revises: f80fa8d66374
Create Date: 2026-01-17 10:16:58.570136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56c5478f35eb'
down_revision: Union[str, Sequence[str], None] = 'f80fa8d66374'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
