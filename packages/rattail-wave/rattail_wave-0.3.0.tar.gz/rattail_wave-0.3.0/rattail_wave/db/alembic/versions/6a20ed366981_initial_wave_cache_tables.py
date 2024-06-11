# -*- coding: utf-8; -*-
"""initial Wave cache tables

Revision ID: 6a20ed366981
Revises: 7d009a925f21
Create Date: 2022-09-02 13:27:36.945137

"""

# revision identifiers, used by Alembic.
revision = '6a20ed366981'
down_revision = None
branch_labels = ('rattail_wave',)
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    ##############################
    # cache tables
    ##############################

    # wave_cache_customer
    op.create_table('wave_cache_customer',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.String(length=100), nullable=False),
                    sa.Column('internal_id', sa.String(length=100), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=True),
                    sa.Column('is_archived', sa.Boolean(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('id', name='wave_cache_customer_uq_id')
    )
    op.create_table('wave_cache_customer_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('id', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('internal_id', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('name', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('email', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('is_archived', sa.Boolean(), autoincrement=False, nullable=True),
                    sa.Column('created_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('modified_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_wave_cache_customer_version_end_transaction_id'), 'wave_cache_customer_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_wave_cache_customer_version_operation_type'), 'wave_cache_customer_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_wave_cache_customer_version_transaction_id'), 'wave_cache_customer_version', ['transaction_id'], unique=False)

    # wave_cache_invoice
    op.create_table('wave_cache_invoice',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.String(length=100), nullable=False),
                    sa.Column('internal_id', sa.String(length=100), nullable=True),
                    sa.Column('customer_id', sa.String(length=100), nullable=False),
                    sa.Column('status', sa.String(length=10), nullable=False),
                    sa.Column('title', sa.String(length=255), nullable=False),
                    sa.Column('subhead', sa.String(length=255), nullable=True),
                    sa.Column('invoice_number', sa.String(length=10), nullable=False),
                    sa.Column('invoice_date', sa.Date(), nullable=False),
                    sa.Column('due_date', sa.Date(), nullable=False),
                    sa.Column('amount_due', sa.Numeric(precision=9, scale=2), nullable=False),
                    sa.Column('amount_paid', sa.Numeric(precision=9, scale=2), nullable=False),
                    sa.Column('tax_total', sa.Numeric(precision=9, scale=2), nullable=False),
                    sa.Column('total', sa.Numeric(precision=9, scale=2), nullable=False),
                    sa.Column('discount_total', sa.Numeric(precision=9, scale=2), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['customer_id'], ['wave_cache_customer.id'], name='wave_cache_invoice_fk_customer'),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('id', name='wave_cache_invoice_uq_id')
    )
    op.create_table('wave_cache_invoice_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('id', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('internal_id', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('customer_id', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('status', sa.String(length=10), autoincrement=False, nullable=True),
                    sa.Column('title', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('subhead', sa.String(length=255), autoincrement=False, nullable=True),
                    sa.Column('invoice_number', sa.String(length=10), autoincrement=False, nullable=True),
                    sa.Column('invoice_date', sa.Date(), autoincrement=False, nullable=True),
                    sa.Column('due_date', sa.Date(), autoincrement=False, nullable=True),
                    sa.Column('amount_due', sa.Numeric(precision=9, scale=2), autoincrement=False, nullable=True),
                    sa.Column('amount_paid', sa.Numeric(precision=9, scale=2), autoincrement=False, nullable=True),
                    sa.Column('tax_total', sa.Numeric(precision=9, scale=2), autoincrement=False, nullable=True),
                    sa.Column('total', sa.Numeric(precision=9, scale=2), autoincrement=False, nullable=True),
                    sa.Column('discount_total', sa.Numeric(precision=9, scale=2), autoincrement=False, nullable=True),
                    sa.Column('created_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('modified_at', sa.DateTime(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_wave_cache_invoice_version_end_transaction_id'), 'wave_cache_invoice_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_wave_cache_invoice_version_operation_type'), 'wave_cache_invoice_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_wave_cache_invoice_version_transaction_id'), 'wave_cache_invoice_version', ['transaction_id'], unique=False)

    ##############################
    # integration tables
    ##############################

    # wave_customer
    op.create_table('wave_customer',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('wave_id', sa.String(length=100), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['customer.uuid'], name='wave_customer_fk_customer'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('wave_customer_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('wave_id', sa.String(length=100), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_wave_customer_version_end_transaction_id'), 'wave_customer_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_wave_customer_version_operation_type'), 'wave_customer_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_wave_customer_version_transaction_id'), 'wave_customer_version', ['transaction_id'], unique=False)


def downgrade():

    ##############################
    # integration tables
    ##############################

    # wave_customer
    op.drop_index(op.f('ix_wave_customer_version_transaction_id'), table_name='wave_customer_version')
    op.drop_index(op.f('ix_wave_customer_version_operation_type'), table_name='wave_customer_version')
    op.drop_index(op.f('ix_wave_customer_version_end_transaction_id'), table_name='wave_customer_version')
    op.drop_table('wave_customer_version')
    op.drop_table('wave_customer')

    ##############################
    # cache tables
    ##############################

    # wave_cache_invoice
    op.drop_index(op.f('ix_wave_cache_invoice_version_transaction_id'), table_name='wave_cache_invoice_version')
    op.drop_index(op.f('ix_wave_cache_invoice_version_operation_type'), table_name='wave_cache_invoice_version')
    op.drop_index(op.f('ix_wave_cache_invoice_version_end_transaction_id'), table_name='wave_cache_invoice_version')
    op.drop_table('wave_cache_invoice_version')
    op.drop_table('wave_cache_invoice')

    # wave_cache_customer
    op.drop_index(op.f('ix_wave_cache_customer_version_transaction_id'), table_name='wave_cache_customer_version')
    op.drop_index(op.f('ix_wave_cache_customer_version_operation_type'), table_name='wave_cache_customer_version')
    op.drop_index(op.f('ix_wave_cache_customer_version_end_transaction_id'), table_name='wave_cache_customer_version')
    op.drop_table('wave_cache_customer_version')
    op.drop_table('wave_cache_customer')
