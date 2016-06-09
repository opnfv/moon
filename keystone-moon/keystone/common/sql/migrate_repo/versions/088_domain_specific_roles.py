# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import migrate
import sqlalchemy as sql


_ROLE_NAME_NEW_CONSTRAINT = 'ixu_role_name_domain_id'
_ROLE_TABLE_NAME = 'role'
_ROLE_NAME_COLUMN_NAME = 'name'
_DOMAIN_ID_COLUMN_NAME = 'domain_id'
_NULL_DOMAIN_ID = '<<null>>'


def upgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine

    role_table = sql.Table(_ROLE_TABLE_NAME, meta, autoload=True)
    domain_id = sql.Column(_DOMAIN_ID_COLUMN_NAME, sql.String(64),
                           nullable=False, server_default=_NULL_DOMAIN_ID)

    # NOTE(morganfainberg): the `role_name` unique constraint is not
    # guaranteed to be a fixed name, such as 'ixu_role_name`, so we need to
    # search for the correct constraint that only affects role_table.c.name
    # and drop that constraint.
    to_drop = None
    if migrate_engine.name == 'mysql':
        for c in role_table.indexes:
            if (c.unique and len(c.columns) == 1 and
                    _ROLE_NAME_COLUMN_NAME in c.columns):
                to_drop = c
                break
    else:
        for c in role_table.constraints:
            if len(c.columns) == 1 and _ROLE_NAME_COLUMN_NAME in c.columns:
                to_drop = c
                break

    if to_drop is not None:
        migrate.UniqueConstraint(role_table.c.name,
                                 name=to_drop.name).drop()

    # perform changes after constraint is dropped.
    if 'domain_id' not in role_table.columns:
        # Only create the column if it doesn't already exist.
        role_table.create_column(domain_id)

    migrate.UniqueConstraint(role_table.c.name,
                             role_table.c.domain_id,
                             name=_ROLE_NAME_NEW_CONSTRAINT).create()
