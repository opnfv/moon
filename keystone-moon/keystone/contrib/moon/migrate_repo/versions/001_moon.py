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
        'intra_extension',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(64), nullable=False),
        sql.Column('model', sql.String(64), nullable=True),
        sql.Column('description', sql.Text(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    intra_extension_table.create(migrate_engine, checkfirst=True)

    subjects_table = sql.Table(
        'subject',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('subjects', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subjects_table.create(migrate_engine, checkfirst=True)

    objects_table = sql.Table(
        'object',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('objects', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    objects_table.create(migrate_engine, checkfirst=True)

    actions_table = sql.Table(
        'action',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('actions', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    actions_table.create(migrate_engine, checkfirst=True)

    subject_categories_table = sql.Table(
        'subject_category',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('subject_categories', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_categories_table.create(migrate_engine, checkfirst=True)

    object_categories_table = sql.Table(
        'object_category',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('object_categories', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_categories_table.create(migrate_engine, checkfirst=True)

    action_categories_table = sql.Table(
        'action_category',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('action_categories', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_categories_table.create(migrate_engine, checkfirst=True)

    subject_category_values_table = sql.Table(
        'subject_category_scope',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('subject_category_scope', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_category_values_table.create(migrate_engine, checkfirst=True)

    object_category_values_table = sql.Table(
        'object_category_scope',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('object_category_scope', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_category_values_table.create(migrate_engine, checkfirst=True)

    action_category_values_table = sql.Table(
        'action_category_scope',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('action_category_scope', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_category_values_table.create(migrate_engine, checkfirst=True)

    subject_category_assignments_table = sql.Table(
        'subject_category_assignment',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('subject_category_assignments', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_category_assignments_table.create(migrate_engine, checkfirst=True)

    object_category_assignments_table = sql.Table(
        'object_category_assignment',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('object_category_assignments', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_category_assignments_table.create(migrate_engine, checkfirst=True)

    action_category_assignments_table = sql.Table(
        'action_category_assignment',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('action_category_assignments', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_category_assignments_table.create(migrate_engine, checkfirst=True)

    meta_rule_table = sql.Table(
        'metarule',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('sub_meta_rules', k_sql.JsonBlob(), nullable=True),
        sql.Column('aggregation', sql.Text(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    meta_rule_table.create(migrate_engine, checkfirst=True)

    rule_table = sql.Table(
        'rule',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('rules', k_sql.JsonBlob(), nullable=True),
        sql.Column('intra_extension_uuid', sql.ForeignKey("intra_extension.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    rule_table.create(migrate_engine, checkfirst=True)


def downgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine

    for _table in (
        'subject',
        'object',
        'action',
        'subject_category',
        'object_category',
        'action_category',
        'subject_category_scope',
        'object_category_scope',
        'action_category_scope',
        'subject_category_assignment',
        'object_category_assignment',
        'action_category_assignment',
        'metarule',
        'rule',
        'intra_extension',
    ):
        try:
            table = sql.Table(_table, meta, autoload=True)
            table.drop(migrate_engine, checkfirst=True)
        except Exception as e:
            print(e.message)


