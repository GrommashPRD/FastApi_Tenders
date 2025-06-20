"""Create users table

Revision ID: 5290dc2dfbf1
Revises: d05a042ab4da
Create Date: 2025-06-20 13:16:11.886523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5290dc2dfbf1'
down_revision: Union[str, None] = 'd05a042ab4da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bids',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'PUBLISHED', 'CANCELED', 'ACCEPTED', 'REJECTED', name='bidstatus'), nullable=True),
    sa.Column('tender_id', sa.UUID(), nullable=False),
    sa.Column('organization_id', sa.String(), nullable=True),
    sa.Column('creator_username', sa.String(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('votes', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tender_id'], ['tenders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('bid_decisions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('bid_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'PUBLISHED', 'CANCELED', 'ACCEPTED', 'REJECTED', name='bidstatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['bid_id'], ['bids.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bid_version',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('bid_id', sa.UUID(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['bid_id'], ['bids.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedback_bid',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('bid_id', sa.UUID(), nullable=False),
    sa.Column('feedback', sa.String(), nullable=False),
    sa.Column('feedback_by', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['bid_id'], ['bids.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback_bid')
    op.drop_table('bid_version')
    op.drop_table('bid_decisions')
    op.drop_table('bids')
    # ### end Alembic commands ###
