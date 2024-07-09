"""Initial migrations

Revision ID: 0d8761184f68
Revises: 
Create Date: 2024-07-09 07:11:17.587498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d8761184f68'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('card_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('user_type', sa.Enum('vendor', 'consumer', name='user_type_enum'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('card_id')
    )
    op.create_table('user_accounts',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('available_balance', sa.Numeric(precision=9, scale=2), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('payments',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('account_id', sa.String(), nullable=True),
    sa.Column('txn_id', sa.String(), nullable=True),
    sa.Column('receipt_no', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('amount', sa.Numeric(precision=9, scale=2), nullable=True),
    sa.Column('status', sa.Enum('pending', 'success', 'failed', name='status_enum'), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['user_accounts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('txn_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('user_accounts')
    op.drop_table('users')
    # ### end Alembic commands ###
