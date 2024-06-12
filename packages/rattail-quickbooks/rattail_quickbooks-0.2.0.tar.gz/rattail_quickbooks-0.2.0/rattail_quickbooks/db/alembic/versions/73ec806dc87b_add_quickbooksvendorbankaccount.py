# -*- coding: utf-8; -*-
"""add QuickbooksVendorBankAccount

Revision ID: 73ec806dc87b
Revises: 6a6791ac0961
Create Date: 2024-04-15 16:48:38.145370

"""

# revision identifiers, used by Alembic.
revision = '73ec806dc87b'
down_revision = '6a6791ac0961'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # quickbooks_vendor_bank_account
    op.create_table('quickbooks_vendor_bank_account',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('vendor_uuid', sa.String(length=32), nullable=False),
                    sa.Column('store_uuid', sa.String(length=32), nullable=False),
                    sa.Column('account_number', sa.String(length=100), nullable=False),
                    sa.ForeignKeyConstraint(['store_uuid'], ['store.uuid'], name='quickbooks_vendor_bank_account_fk_store'),
                    sa.ForeignKeyConstraint(['vendor_uuid'], ['vendor.uuid'], name='quickbooks_vendor_bank_account_fk_vendor'),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('quickbooks_vendor_bank_account_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('vendor_uuid', sa.String(length=32), autoincrement=False, nullable=True),
                    sa.Column('store_uuid', sa.String(length=32), autoincrement=False, nullable=True),
                    sa.Column('account_number', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_quickbooks_vendor_bank_account_version_end_transaction_id'), 'quickbooks_vendor_bank_account_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_quickbooks_vendor_bank_account_version_operation_type'), 'quickbooks_vendor_bank_account_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_quickbooks_vendor_bank_account_version_transaction_id'), 'quickbooks_vendor_bank_account_version', ['transaction_id'], unique=False)


def downgrade():

    # quickbooks_vendor_bank_account
    op.drop_index(op.f('ix_quickbooks_vendor_bank_account_version_transaction_id'), table_name='quickbooks_vendor_bank_account_version')
    op.drop_index(op.f('ix_quickbooks_vendor_bank_account_version_operation_type'), table_name='quickbooks_vendor_bank_account_version')
    op.drop_index(op.f('ix_quickbooks_vendor_bank_account_version_end_transaction_id'), table_name='quickbooks_vendor_bank_account_version')
    op.drop_table('quickbooks_vendor_bank_account_version')
    op.drop_table('quickbooks_vendor_bank_account')
