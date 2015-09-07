# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import sqlalchemy as sql
from keystone.common import sql as k_sql


def upgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine

#     region_table = sql.Table(
#         'tenants',
#         meta,
#         sql.Column('id', sql.String(64), primary_key=True),
#         sql.Column('name', sql.String(128), nullable=True),
#         sql.Column('authz', sql.String(64), nullable=True),
#         sql.Column('admin', sql.String(64), nullable=True),
#
#         mysql_engine='InnoDB',
#         mysql_charset='utf8')
#     region_table.create(migrate_engine, checkfirst=True)
#

def downgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine
#
#     table = sql.Table('tenants', meta, autoload=True)
#     table.drop(migrate_engine, checkfirst=True)
