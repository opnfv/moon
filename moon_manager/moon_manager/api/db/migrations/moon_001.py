# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import json
import sqlalchemy as sql
from sqlalchemy import types as sql_types
from sqlalchemy import create_engine
import sys


class JsonBlob(sql_types.TypeDecorator):
    impl = sql.Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


def upgrade(migrate_engine):
    if isinstance(migrate_engine, str):
        migrate_engine = create_engine(migrate_engine)
    meta = sql.MetaData()
    meta.bind = migrate_engine
    sys.stdout.write("Creating ")
    sys.stdout.flush()

    table = sql.Table(
        'pdp',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('vim_project_id', sql.String(64), nullable=True, default=""),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.UniqueConstraint('name', name='unique_constraint_models'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(table) + " ")
    sys.stdout.flush()

    table = sql.Table(
        'slaves',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('address', sql.String(256), nullable=True, default=""),
        sql.Column('grant_if_unknown_project', sql.Boolean, nullable=True, default=""),
        sql.Column('process', sql.String(256), nullable=False, default=""),
        sql.Column('log', sql.String(256), nullable=False, default=""),
        sql.Column('api_key', sql.String(256), nullable=False, default=""),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.UniqueConstraint('name', name='unique_constraint_models'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(table) + " ")
    sys.stdout.flush()

    table = sql.Table(
        'policies',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('model_id', sql.String(64), nullable=True, default=""),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.UniqueConstraint('name', 'model_id', name='unique_constraint_models'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(table) + " ")
    sys.stdout.flush()

    table = sql.Table(
        'models',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.UniqueConstraint('name', name='unique_constraint_models'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(table) + " ")
    sys.stdout.flush()

    subject_categories_table = sql.Table(
        'subject_categories',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('description', sql.String(256), nullable=True),

        sql.UniqueConstraint('name', name='unique_constraint_subject_categories'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_categories_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(subject_categories_table) + " ")
    sys.stdout.flush()

    object_categories_table = sql.Table(
        'object_categories',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('description', sql.String(256), nullable=True),

        sql.UniqueConstraint('name', name='unique_constraint_object_categories'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_categories_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(object_categories_table) + " ")
    sys.stdout.flush()

    action_categories_table = sql.Table(
        'action_categories',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('description', sql.String(256), nullable=True),

        sql.UniqueConstraint('name', name='unique_constraint_action_categories'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_categories_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(action_categories_table) + " ")
    sys.stdout.flush()

    subjects_table = sql.Table(
        'subjects',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.UniqueConstraint('name', name='unique_constraint_subjects'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subjects_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(subjects_table) + " ")
    sys.stdout.flush()

    objects_table = sql.Table(
        'objects',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.UniqueConstraint('name', name='unique_constraint_objects'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    objects_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(objects_table) + " ")
    sys.stdout.flush()

    actions_table = sql.Table(
        'actions',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.UniqueConstraint('name', name='unique_constraint_actions'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    actions_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(actions_table) + " ")
    sys.stdout.flush()

    subject_data_table = sql.Table(
        'subject_data',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.Column('category_id', sql.ForeignKey("subject_categories.id"), nullable=False),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.UniqueConstraint('name', 'category_id', 'policy_id',
                             name='unique_constraint_subject_data'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_data_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(subject_data_table) + " ")
    sys.stdout.flush()

    object_data_table = sql.Table(
        'object_data',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.Column('category_id', sql.ForeignKey("object_categories.id"), nullable=False),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.UniqueConstraint('name', 'category_id', 'policy_id',
                             name='unique_constraint_object_data'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_data_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(object_data_table) + " ")
    sys.stdout.flush()

    action_data_table = sql.Table(
        'action_data',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.Column('category_id', sql.ForeignKey("action_categories.id"), nullable=False),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.UniqueConstraint('name', 'category_id', 'policy_id',
                             name='unique_constraint_action_data'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_data_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(action_data_table) + " ")
    sys.stdout.flush()

    subject_assignments_table = sql.Table(
        'subject_assignments',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('assignments', sql.String(256), nullable=True),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.Column('subject_id', sql.ForeignKey("subjects.id"), nullable=False),
        sql.Column('category_id', sql.ForeignKey("subject_categories.id"), nullable=False),
        sql.UniqueConstraint('policy_id', 'subject_id', 'category_id',
                             name='unique_constraint_subject_assignment'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    subject_assignments_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(subject_assignments_table) + " ")
    sys.stdout.flush()

    object_assignments_table = sql.Table(
        'object_assignments',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('assignments', sql.String(256), nullable=True),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.Column('object_id', sql.ForeignKey("objects.id"), nullable=False),
        sql.Column('category_id', sql.ForeignKey("object_categories.id"), nullable=False),
        sql.UniqueConstraint('policy_id', 'object_id', 'category_id',
                             name='unique_constraint_object_assignment'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    object_assignments_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(object_assignments_table) + " ")
    sys.stdout.flush()

    action_assignments_table = sql.Table(
        'action_assignments',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('assignments', sql.String(256), nullable=True),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.Column('action_id', sql.ForeignKey("actions.id"), nullable=False),
        sql.Column('category_id', sql.ForeignKey("action_categories.id"), nullable=False),
        sql.UniqueConstraint('policy_id', 'action_id', 'category_id',
                             name='unique_constraint_action_assignment'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    action_assignments_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(action_assignments_table) + " ")
    sys.stdout.flush()

    meta_rules_table = sql.Table(
        'meta_rules',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('name', sql.String(256), nullable=False),
        sql.Column('subject_categories', JsonBlob(), nullable=False),
        sql.Column('object_categories', JsonBlob(), nullable=False),
        sql.Column('action_categories', JsonBlob(), nullable=False),
        sql.Column('value', JsonBlob(), nullable=True),
        sql.UniqueConstraint('name', name='unique_constraint_meta_rule_name'),
        # sql.UniqueConstraint('subject_categories', 'object_categories', 'action_categories', name='unique_constraint_meta_rule_def'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    meta_rules_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(meta_rules_table) + " ")
    sys.stdout.flush()

    rules_table = sql.Table(
        'rules',
        meta,
        sql.Column('id', sql.String(64), primary_key=True),
        sql.Column('rule', JsonBlob(), nullable=True),
        sql.Column('policy_id', sql.ForeignKey("policies.id"), nullable=False),
        sql.Column('meta_rule_id', sql.ForeignKey("meta_rules.id"), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    rules_table.create(migrate_engine, checkfirst=True)
    sys.stdout.write(str(rules_table) + " ")
    sys.stdout.flush()
    print("")


def downgrade(migrate_engine):
    if isinstance(migrate_engine, str):
        migrate_engine = create_engine(migrate_engine)
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
            'pdp',
            'slaves'
    ):
        try:
            table = sql.Table(_table, meta, autoload=True)
            table.drop(migrate_engine, checkfirst=True)
        except Exception as e:
            print(e)
