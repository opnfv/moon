# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import sqlalchemy as sql


def upgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine

    table = sql.Table(
        'pdp',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.Text(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    table.create(migrate_engine, checkfirst=True)

    table = sql.Table(
        'policies',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.Text(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    table.create(migrate_engine, checkfirst=True)

    table = sql.Table(
        'models',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.Text(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    table.create(migrate_engine, checkfirst=True)

    subject_categories_table = sql.Table(
        'subject_categories',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('description', sql.String(256), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_categories_table.create(migrate_engine, checkfirst=True)

    object_categories_table = sql.Table(
        'object_categories',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('description', sql.String(256), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_categories_table.create(migrate_engine, checkfirst=True)

    action_categories_table = sql.Table(
        'action_categories',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('description', sql.String(256), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_categories_table.create(migrate_engine, checkfirst=True)

    subjects_table = sql.Table(
        'subjects',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.Text(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subjects_table.create(migrate_engine, checkfirst=True)

    objects_table = sql.Table(
        'objects',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.Text(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    objects_table.create(migrate_engine, checkfirst=True)

    actions_table = sql.Table(
        'actions',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.Text(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    actions_table.create(migrate_engine, checkfirst=True)

    subject_data_table = sql.Table(
        'subject_data',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.Text(), nullable=True),
        sql.Column('category_id', sql.ForeignKey("subject_categories.id"), nullable=False),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_data_table.create(migrate_engine, checkfirst=True)

    object_data_table = sql.Table(
        'object_data',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.Text(), nullable=True),
        sql.Column('category_id', sql.ForeignKey("object_categories.id"), nullable=False),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_data_table.create(migrate_engine, checkfirst=True)

    action_data_table = sql.Table(
        'action_data',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.Text(), nullable=True),
        sql.Column('category_id', sql.ForeignKey("action_categories.id"), nullable=False),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_data_table.create(migrate_engine, checkfirst=True)

    subject_assignments_table = sql.Table(
        'subject_assignments',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('assignments', sql.Text(), nullable=True),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.Column('subject_id', sql.ForeignKey("subjects.id"), nullable=False),
        sql.Column('category_id', sql.ForeignKey("subject_categories.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_assignments_table.create(migrate_engine, checkfirst=True)

    object_assignments_table = sql.Table(
        'object_assignments',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('assignments', sql.Text(), nullable=True),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.Column('object_id', sql.ForeignKey("objects.id"), nullable=False),
        sql.Column('category_id', sql.ForeignKey("object_categories.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_assignments_table.create(migrate_engine, checkfirst=True)

    action_assignments_table = sql.Table(
        'action_assignments',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('assignments', sql.Text(), nullable=True),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.Column('action_id', sql.ForeignKey("actions.id"), nullable=False),
        sql.Column('category_id', sql.ForeignKey("action_categories.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_assignments_table.create(migrate_engine, checkfirst=True)

    meta_rules_table = sql.Table(
        'meta_rules',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('value', sql.Text(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    meta_rules_table.create(migrate_engine, checkfirst=True)

    rules_table = sql.Table(
        'rules',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('rule', sql.Text(), nullable=True),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.Column('meta_rule_id', sql.ForeignKey("meta_rules.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    rules_table.create(migrate_engine, checkfirst=True)


def downgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine

    for _table in (
        'rules',
        'meta_rules',
        'action_assignments',
        'object_assignments',
        'subject_assignments',
        'action_data',
        'object_data',
        'subject_data',
        'actions',
        'objects',
        'subjects',
        'action_categories',
        'object_categories',
        'subject_categories',
        'models',
        'policies',
        'pdp'
    ):
        try:
            table = sql.Table(_table, meta, autoload=True)
            table.drop(migrate_engine, checkfirst=True)
        except Exception as e:
            print(e)


