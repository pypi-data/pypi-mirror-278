# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Vendor data model extensions
"""

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm.collections import attribute_mapped_collection

from rattail.db import model


class QuickbooksVendor(model.Base):
    """
    Quickbooks extensions to core Vendor model
    """
    __tablename__ = 'quickbooks_vendor'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['vendor.uuid'],
                                name='quickbooks_vendor_fk_vendor'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)

    vendor = orm.relationship(
        model.Vendor,
        doc="""
        Vendor to which this extension record pertains.
        """,
        backref=orm.backref(
            '_quickbooks',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Quickbooks extension record for the vendor.
            """))

    quickbooks_name = sa.Column(sa.String(length=100), nullable=True, doc="""
    Quickbooks "name" for the vendor.
    """)

    quickbooks_bank_account = sa.Column(sa.String(length=100), nullable=True, doc="""
    Quickbooks "bank account" for the vendor.
    """)

    quickbooks_terms = sa.Column(sa.String(length=100), nullable=True, doc="""
    Quickbooks "terms" for the vendor.
    """)


QuickbooksVendor.make_proxy(model.Vendor, '_quickbooks', 'quickbooks_name')
QuickbooksVendor.make_proxy(model.Vendor, '_quickbooks', 'quickbooks_bank_account')
QuickbooksVendor.make_proxy(model.Vendor, '_quickbooks', 'quickbooks_terms')


class QuickbooksVendorBankAccount(model.Base):
    """
    Quickbooks bank account for vendor+store combo.
    """
    __tablename__ = 'quickbooks_vendor_bank_account'
    __table_args__ = (
        sa.ForeignKeyConstraint(['vendor_uuid'], ['vendor.uuid'],
                                name='quickbooks_vendor_bank_account_fk_vendor'),
        sa.ForeignKeyConstraint(['store_uuid'], ['store.uuid'],
                                name='quickbooks_vendor_bank_account_fk_store'),
    )
    __versioned__ = {}

    uuid = model.uuid_column()

    vendor_uuid = sa.Column(sa.String(length=32), nullable=False)
    vendor = orm.relationship(
        model.Vendor,
        doc="""
        Vendor to which this record pertains.
        """,
        backref=orm.backref(
            'quickbooks_bank_accounts',
            collection_class=attribute_mapped_collection('store_uuid'),
            cascade='all, delete-orphan',
            cascade_backrefs=False,
            doc="""
            Quickbooks bank account records.
            """))

    store_uuid = sa.Column(sa.String(length=32), nullable=False)
    store = orm.relationship(
        model.Store,
        doc="""
        Store to which this record pertains.
        """)

    account_number = sa.Column(sa.String(length=100), nullable=False, doc="""
    Quickbooks "bank account number" for the vendor+store combo.
    """)
