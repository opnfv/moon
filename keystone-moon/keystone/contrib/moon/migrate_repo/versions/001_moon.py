# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import sqlalchemy as sql
from keystone.common import sql as k_sql


def upgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine

    intra_extension_table = sql.Table(
        'intra_extensions',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('intra_extension', k_sql.JsonBlob(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    intra_extension_table.create(migrate_engine, checkfirst=True)

    tenant_table = sql.Table(
        'tenants',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('tenant', k_sql.JsonBlob(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    tenant_table.create(migrate_engine, checkfirst=True)

    subject_categories_table = sql.Table(
        'subject_categories',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('subject_category', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_categories_table.create(migrate_engine, checkfirst=True)

    object_categories_table = sql.Table(
        'object_categories',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('object_category', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_categories_table.create(migrate_engine, checkfirst=True)

    action_categories_table = sql.Table(
        'action_categories',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('action_category', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_categories_table.create(migrate_engine, checkfirst=True)

    subjects_table = sql.Table(
        'subjects',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('subject', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subjects_table.create(migrate_engine, checkfirst=True)

    objects_table = sql.Table(
        'objects',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('object', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    objects_table.create(migrate_engine, checkfirst=True)

    actions_table = sql.Table(
        'actions',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('action', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    actions_table.create(migrate_engine, checkfirst=True)

    subject_scopes_table = sql.Table(
        'subject_scopes',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('subject_scope', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        sql.Column('subject_category_id', sql.ForeignKey("subject_categories.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_scopes_table.create(migrate_engine, checkfirst=True)

    object_scopes_table = sql.Table(
        'object_scopes',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('object_scope', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        sql.Column('object_category_id', sql.ForeignKey("object_categories.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_scopes_table.create(migrate_engine, checkfirst=True)

    action_scopes_table = sql.Table(
        'action_scopes',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('action_scope', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        sql.Column('action_category_id', sql.ForeignKey("action_categories.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_scopes_table.create(migrate_engine, checkfirst=True)

    subject_assignments_table = sql.Table(
        'subject_assignments',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('subject_assignment', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        sql.Column('subject_id', sql.ForeignKey("subjects.id"), nullable=False),
        sql.Column('subject_category_id', sql.ForeignKey("subject_categories.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_assignments_table.create(migrate_engine, checkfirst=True)

    object_assignments_table = sql.Table(
        'object_assignments',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('object_assignment', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        sql.Column('object_id', sql.ForeignKey("objects.id"), nullable=False),
        sql.Column('object_category_id', sql.ForeignKey("object_categories.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_assignments_table.create(migrate_engine, checkfirst=True)

    action_assignments_table = sql.Table(
        'action_assignments',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('action_assignment', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        sql.Column('action_id', sql.ForeignKey("actions.id"), nullable=False),
        sql.Column('action_category_id', sql.ForeignKey("action_categories.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_assignments_table.create(migrate_engine, checkfirst=True)

    sub_meta_rules_table = sql.Table(
        'sub_meta_rules',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('sub_meta_rule', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    sub_meta_rules_table.create(migrate_engine, checkfirst=True)

    rules_table = sql.Table(
        'rules',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('rule', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_id', sql.ForeignKey("intra_extensions.id"), nullable=False),
        sql.Column('sub_meta_rule_id', sql.ForeignKey("sub_meta_rules.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    rules_table.create(migrate_engine, checkfirst=True)


def downgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine

    for _table in (
        'rules',
        'sub_meta_rules',
        'action_assignments',
        'object_assignments',
        'subject_assignments',
        'action_scopes',
        'object_scopes',
        'subject_scopes',
        'actions',
        'objects',
        'subjects',
        'action_categories',
        'object_categories',
        'subject_categories',
        'tenants',
        'intra_extensions'
    ):
        try:
            table = sql.Table(_table, meta, autoload=True)
            table.drop(migrate_engine, checkfirst=True)
        except Exception as e:
            print(e.message)


