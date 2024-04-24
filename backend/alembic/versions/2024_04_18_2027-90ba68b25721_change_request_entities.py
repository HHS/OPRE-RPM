"""Change Request entities

Revision ID: 90ba68b25721
Revises: ff7132d9d0c0
Create Date: 2024-04-18 20:27:36.421458+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '90ba68b25721'
down_revision: Union[str, None] = 'ff7132d9d0c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('IN_REVIEW', 'APPROVED', 'REJECTED', name='changerequeststatus').create(op.get_bind())
    op.create_table('change_request_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('type', sa.String(), autoincrement=False, nullable=True),
    sa.Column('status', postgresql.ENUM('IN_REVIEW', 'APPROVED', 'REJECTED', name='changerequeststatus', create_type=False), autoincrement=False, nullable=True),
    sa.Column('requested_changes', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('reviewed_by_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('reviewed_on', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('created_by', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('updated_by', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('created_on', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('updated_on', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('agreement_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('budget_line_item_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    op.create_index(op.f('ix_change_request_version_end_transaction_id'), 'change_request_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_change_request_version_operation_type'), 'change_request_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_change_request_version_transaction_id'), 'change_request_version', ['transaction_id'], unique=False)
    op.create_table('change_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('status', postgresql.ENUM('IN_REVIEW', 'APPROVED', 'REJECTED', name='changerequeststatus', create_type=False), nullable=False),
    sa.Column('requested_changes', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('reviewed_by_id', sa.Integer(), nullable=True),
    sa.Column('reviewed_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('agreement_id', sa.Integer(), nullable=True),
    sa.Column('budget_line_item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['agreement_id'], ['agreement.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['budget_line_item_id'], ['budget_line_item.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['reviewed_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('change_request')
    op.drop_index(op.f('ix_change_request_version_transaction_id'), table_name='change_request_version')
    op.drop_index(op.f('ix_change_request_version_operation_type'), table_name='change_request_version')
    op.drop_index(op.f('ix_change_request_version_end_transaction_id'), table_name='change_request_version')
    op.drop_table('change_request_version')
    sa.Enum('IN_REVIEW', 'APPROVED', 'REJECTED', name='changerequeststatus').drop(op.get_bind())
    # ### end Alembic commands ###
