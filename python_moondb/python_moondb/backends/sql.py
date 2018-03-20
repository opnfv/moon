# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import copy
import json
from uuid import uuid4
import sqlalchemy as sql
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy import types as sql_types
from python_moonutilities import configuration
from python_moonutilities import exceptions
from python_moondb.core import PDPDriver, PolicyDriver, ModelDriver

logger = logging.getLogger("moon.db.driver.sql")
Base = declarative_base()
DEBUG = True if configuration.get_configuration("logging")['logging']['loggers']['moon']['level'] == "DEBUG" else False


class DictBase:
    attributes = []

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)
        # new_d = d.copy()
        #
        # new_d['extra'] = {k: new_d.pop(k) for k in six.iterkeys(d)
        #                   if k not in cls.attributes and k != 'extra'}
        #
        # return cls(**new_d)

    def to_dict(self):
        d = dict()
        for attr in self.__class__.attributes:
            d[attr] = getattr(self, attr)
        return d

    def __getitem__(self, key):
        # if "extra" in dir(self) and key in self.extra:
        #     return self.extra[key]
        return getattr(self, key)


class JsonBlob(sql_types.TypeDecorator):

    impl = sql.Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


class Model(Base, DictBase):
    __tablename__ = 'models'
    attributes = ['id', 'value']
    id = sql.Column(sql.String(64), primary_key=True)
    value = sql.Column(JsonBlob(), nullable=True)

    def to_dict(self):
        return {
            "name": self.value.get("name"),
            "description": self.value.get("description", ""),
            "meta_rules": self.value.get("meta_rules", list()),
        }


class Policy(Base, DictBase):
    __tablename__ = 'policies'
    attributes = ['id', 'value']
    id = sql.Column(sql.String(64), primary_key=True)
    value = sql.Column(JsonBlob(), nullable=True)

    def to_dict(self):
        return {
            "name": self.value.get("name"),
            "description": self.value.get("description", ""),
            "model_id": self.value.get("model_id", ""),
            "genre": self.value.get("genre", ""),
        }


class PDP(Base, DictBase):
    __tablename__ = 'pdp'
    attributes = ['id', 'value']
    id = sql.Column(sql.String(64), primary_key=True)
    value = sql.Column(JsonBlob(), nullable=True)

    def to_dict(self):
        return {
            "name": self.value.get("name"),
            "description": self.value.get("description", ""),
            "keystone_project_id": self.value.get("keystone_project_id", ""),
            "security_pipeline": self.value.get("security_pipeline", []),
        }


class PerimeterCategoryBase(DictBase):
    attributes = ['id', 'name', 'description']
    id = sql.Column(sql.String(64), primary_key=True)
    name = sql.Column(sql.String(256), nullable=False)
    description = sql.Column(sql.String(256), nullable=True)


class SubjectCategory(Base, PerimeterCategoryBase):
    __tablename__ = 'subject_categories'


class ObjectCategory(Base, PerimeterCategoryBase):
    __tablename__ = 'object_categories'


class ActionCategory(Base, PerimeterCategoryBase):
    __tablename__ = 'action_categories'


class PerimeterBase(DictBase):
    attributes = ['id', 'value']
    id = sql.Column(sql.String(64), primary_key=True)
    value = sql.Column(JsonBlob(), nullable=True)
    __mapper_args__ = {'concrete': True}
    def __repr__(self):
        return "{}: {}".format(self.id, json.dumps(self.value))

    def to_return(self):
        return {
            'id': self.id,
            'name': self.value.get("name", ""),
            'description': self.value.get("description", ""),
            'email': self.value.get("email", ""),
            'extra': self.value.get("extra", dict()),
            'policy_list': self.value.get("policy_list", [])
        }

    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value
        }


class Subject(Base, PerimeterBase):
    __tablename__ = 'subjects'


class Object(Base, PerimeterBase):
    __tablename__ = 'objects'


class Action(Base, PerimeterBase):
    __tablename__ = 'actions'


class PerimeterDataBase(DictBase):
    attributes = ['id', 'value', 'category_id', 'policy_id']
    id = sql.Column(sql.String(64), primary_key=True)
    value = sql.Column(JsonBlob(), nullable=True)
    @declared_attr
    def policy_id(cls):
        return sql.Column(sql.ForeignKey("policies.id"), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.value.get("name", ""),
            'description': self.value.get("description", ""),
            'category_id': self.category_id,
            'policy_id': self.policy_id
        }


class SubjectData(Base, PerimeterDataBase):
    __tablename__ = 'subject_data'
    category_id = sql.Column(sql.ForeignKey("subject_categories.id"), nullable=False)


class ObjectData(Base, PerimeterDataBase):
    __tablename__ = 'object_data'
    category_id = sql.Column(sql.ForeignKey("object_categories.id"), nullable=False)


class ActionData(Base, PerimeterDataBase):
    __tablename__ = 'action_data'
    category_id = sql.Column(sql.ForeignKey("action_categories.id"), nullable=False)


class PerimeterAssignmentBase(DictBase):
    attributes = ['id', 'assignments', 'policy_id', 'subject_id', 'category_id']
    id = sql.Column(sql.String(64), primary_key=True)
    assignments = sql.Column(JsonBlob(), nullable=True)
    category_id = None

    @declared_attr
    def policy_id(cls):
        return sql.Column(sql.ForeignKey("policies.id"), nullable=False)

    def _to_dict(self, element_key, element_value):
        return {
            "id": self.id,
            "policy_id": self.policy_id,
            element_key: element_value,
            "category_id": self.category_id,
            "assignments": self.assignments,
        }


class SubjectAssignment(Base, PerimeterAssignmentBase):
    __tablename__ = 'subject_assignments'
    subject_id = sql.Column(sql.ForeignKey("subjects.id"), nullable=False)
    category_id = sql.Column(sql.ForeignKey("subject_categories.id"), nullable=False)

    def to_dict(self):
        return self._to_dict("subject_id", self.subject_id)


class ObjectAssignment(Base, PerimeterAssignmentBase):
    __tablename__ = 'object_assignments'
    attributes = ['id', 'assignments', 'policy_id', 'object_id', 'category_id']
    object_id = sql.Column(sql.ForeignKey("objects.id"), nullable=False)
    category_id = sql.Column(sql.ForeignKey("object_categories.id"), nullable=False)

    def to_dict(self):
        return self._to_dict("object_id", self.object_id)


class ActionAssignment(Base, PerimeterAssignmentBase):
    __tablename__ = 'action_assignments'
    attributes = ['id', 'assignments', 'policy_id', 'action_id', 'category_id']
    action_id = sql.Column(sql.ForeignKey("actions.id"), nullable=False)
    category_id = sql.Column(sql.ForeignKey("action_categories.id"), nullable=False)

    def to_dict(self):
        return self._to_dict("action_id", self.action_id)


class MetaRule(Base, DictBase):
    __tablename__ = 'meta_rules'
    attributes = ['id', 'value']
    id = sql.Column(sql.String(64), primary_key=True)
    value = sql.Column(JsonBlob(), nullable=True)

    def to_dict(self):
        return {
            "name": self.value["name"],
            "description": self.value.get("description", ""),
            "subject_categories": self.value.get("subject_categories", list()),
            "object_categories": self.value.get("object_categories", list()),
            "action_categories": self.value.get("action_categories", list()),
        }


class Rule(Base, DictBase):
    __tablename__ = 'rules'
    attributes = ['id', 'rule', 'policy_id', 'meta_rule_id']
    id = sql.Column(sql.String(64), primary_key=True)
    rule = sql.Column(JsonBlob(), nullable=True)
    policy_id = sql.Column(sql.ForeignKey("policies.id"), nullable=False)
    meta_rule_id = sql.Column(sql.ForeignKey("meta_rules.id"), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'rule': self.rule["rule"],
            'instructions': self.rule["instructions"],
            'enabled': self.rule["enabled"],
            'policy_id': self.policy_id,
            'meta_rule_id': self.meta_rule_id
        }

    def __repr__(self):
        return "{}".format(self.rule)


@contextmanager
def session_scope(engine):
    """Provide a transactional scope around a series of operations."""
    if type(engine) is str:
        echo = DEBUG
        engine = create_engine(engine, echo=echo)
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class BaseConnector(object):
    """Provide a base connector to connect them all"""
    engine = ""

    def __init__(self, engine_name):
        echo = DEBUG
        self.engine = create_engine(engine_name, echo=echo)

    def init_db(self):
        Base.metadata.create_all(self.engine)

    def set_engine(self, engine_name):
        self.engine = engine_name

    def get_session(self):
        return session_scope(self.engine)

    def get_session_for_read(self):
        return self.get_session()

    def get_session_for_write(self):
        return self.get_session()


class PDPConnector(BaseConnector, PDPDriver):

    def update_pdp(self, pdp_id, value):
        with self.get_session_for_write() as session:
            query = session.query(PDP)
            query = query.filter_by(id=pdp_id)
            ref = query.first()
            if ref:
                d = dict(ref.value)
                d.update(value)
                setattr(ref, "value", d)
            return {ref.id: ref.to_dict()}

    def delete_pdp(self, pdp_id):
        with self.get_session_for_write() as session:
            ref = session.query(PDP).get(pdp_id)
            session.delete(ref)

    def add_pdp(self, pdp_id=None, value=None):
        with self.get_session_for_write() as session:
            new = PDP.from_dict({
                "id": pdp_id if pdp_id else uuid4().hex,
                "value": value
            })
            session.add(new)
            return {new.id: new.to_dict()}

    def get_pdp(self, pdp_id=None):
        with self.get_session_for_read() as session:
            query = session.query(PDP)
            if pdp_id:
                query = query.filter_by(id=pdp_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict() for _ref in ref_list}


class PolicyConnector(BaseConnector, PolicyDriver):

    def update_policy(self, policy_id, value):
        with self.get_session_for_write() as session:
            query = session.query(Policy)
            query = query.filter_by(id=policy_id)
            ref = query.first()
            if ref:
                d = dict(ref.value)
                d.update(value)
                setattr(ref, "value", d)
            return {ref.id: ref.to_dict()}

    def delete_policy(self, policy_id):
        with self.get_session_for_write() as session:
            ref = session.query(Policy).get(policy_id)
            session.delete(ref)

    def add_policy(self, policy_id=None, value=None):
        with self.get_session_for_write() as session:
            new = Policy.from_dict({
                "id": policy_id if policy_id else uuid4().hex,
                "value": value
            })
            session.add(new)
            return {new.id: new.to_dict()}

    def get_policies(self, policy_id=None):
        with self.get_session_for_read() as session:
            query = session.query(Policy)
            if policy_id:
                query = query.filter_by(id=policy_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict() for _ref in ref_list}

    def __get_perimeters(self, ClassType, policy_id, perimeter_id=None):
        with self.get_session_for_read() as session:
            query = session.query(ClassType)
            ref_list = copy.deepcopy(query.all())
            if perimeter_id:
                for _ref in ref_list:
                    _ref_value = _ref.to_return()
                    if perimeter_id == _ref.id:
                        if policy_id and policy_id in _ref_value["policy_list"]:
                            return {_ref.id: _ref_value}
                        else:
                            return {}
            elif policy_id:
                results = []
                for _ref in ref_list:
                    _ref_value = _ref.to_return()
                    if policy_id in _ref_value["policy_list"]:
                        results.append(_ref)
                return {_ref.id: _ref.to_return() for _ref in results}
            return {_ref.id: _ref.to_return() for _ref in ref_list}

    def __set_perimeter(self, ClassType, policy_id, perimeter_id=None, value=None):
        if "name" not in value or not value["name"]:
            raise exceptions.PerimeterNameInvalid
        _perimeter = None
        with self.get_session_for_write() as session:
            if perimeter_id:
                query = session.query(ClassType)
                query = query.filter_by(id=perimeter_id)
                _perimeter = query.first()
            if not _perimeter:
                if "policy_list" not in value or type(value["policy_list"]) is not list:
                    value["policy_list"] = []
                if policy_id and policy_id not in value["policy_list"]:
                    value["policy_list"] = [policy_id, ]
                new = ClassType.from_dict({
                    "id": perimeter_id if perimeter_id else uuid4().hex,
                    "value": value
                })
                session.add(new)
                return {new.id: new.to_return()}
            else:
                _value = copy.deepcopy(_perimeter.to_dict())
                if "policy_list" not in _value["value"] or type(_value["value"]["policy_list"]) is not list:
                    _value["value"]["policy_list"] = []
                if policy_id and policy_id not in _value["value"]["policy_list"]:
                    _value["value"]["policy_list"].append(policy_id)
                new_perimeter = ClassType.from_dict(_value)
                # setattr(_subject, "value", _value["value"])
                setattr(_perimeter, "value", getattr(new_perimeter, "value"))
                return {_perimeter.id: _perimeter.to_return()}

    def __delete_perimeter(self,ClassType, ClassUnknownException, policy_id, perimeter_id):
        with self.get_session_for_write() as session:
            query = session.query(ClassType)
            query = query.filter_by(id=perimeter_id)
            _perimeter = query.first()
            if not _perimeter:
                raise ClassUnknownException
            old_perimeter = copy.deepcopy(_perimeter.to_dict())
            # value = _subject.to_dict()
            try:
                old_perimeter["value"]["policy_list"].remove(policy_id)
                new_perimeter = ClassType.from_dict(old_perimeter)
                setattr(_perimeter, "value", getattr(new_perimeter, "value"))
            except ValueError:
                if not _perimeter.value["policy_list"]:
                    session.delete(_perimeter)

    def get_subjects(self, policy_id, perimeter_id=None):
        return self.__get_perimeters(Subject, policy_id, perimeter_id)

    def set_subject(self, policy_id, perimeter_id=None, value=None):
        return self.__set_perimeter(Subject, policy_id, perimeter_id=perimeter_id, value=value)

    def delete_subject(self, policy_id, perimeter_id):
        self.__delete_perimeter(Subject, exceptions.SubjectUnknown, policy_id, perimeter_id)

    def get_objects(self, policy_id, perimeter_id=None):
        return self.__get_perimeters(Object, policy_id, perimeter_id)

    def set_object(self, policy_id, perimeter_id=None, value=None):
        return self.__set_perimeter(Object, policy_id, perimeter_id=perimeter_id, value=value)

    def delete_object(self, policy_id, perimeter_id):
        self.__delete_perimeter(Object, exceptions.ObjectUnknown, policy_id, perimeter_id)

    def get_actions(self, policy_id, perimeter_id=None):
        return self.__get_perimeters(Action, policy_id, perimeter_id)

    def set_action(self, policy_id, perimeter_id=None, value=None):
        return self.__set_perimeter(Action, policy_id, perimeter_id=perimeter_id, value=value)

    def delete_action(self, policy_id, perimeter_id):
        self.__delete_perimeter(Action, exceptions.ActionUnknown, policy_id, perimeter_id)

    def __get_perimeter_data(self, ClassType, policy_id, data_id=None, category_id=None):
        logger.info("driver {} {} {}".format(policy_id, data_id, category_id))
        with self.get_session_for_read() as session:
            query = session.query(ClassType)
            if data_id:
                query = query.filter_by(policy_id=policy_id, id=data_id, category_id=category_id)
            else:
                query = query.filter_by(policy_id=policy_id, category_id=category_id)
            ref_list = query.all()
            logger.info("ref_list={}".format(ref_list))
            return {
                "policy_id": policy_id,
                "category_id": category_id,
                "data": {_ref.id: _ref.to_dict() for _ref in ref_list}
            }

    def __set_perimeter_data(self, ClassType, ClassTypeData, policy_id, data_id=None, category_id=None, value=None):
        with self.get_session_for_write() as session:
            query = session.query(ClassTypeData)
            query = query.filter_by(policy_id=policy_id, id=data_id, category_id=category_id)
            ref = query.first()
            if not ref:
                new_ref = ClassTypeData.from_dict(
                    {
                        "id": data_id if data_id else uuid4().hex,
                        'value': value,
                        'category_id': category_id,
                        'policy_id': policy_id,
                    }
                )
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in ClassType.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(ref, attr))
            # session.flush()
            return {
                "policy_id": policy_id,
                "category_id": category_id,
                "data": {ref.id: ref.to_dict()}
            }

    def __delete_perimeter_data(self, ClassType, policy_id, data_id):
        with self.get_session_for_write() as session:
            query = session.query(ClassType)
            query = query.filter_by(policy_id=policy_id, id=data_id)
            ref = query.first()
            if ref:
                session.delete(ref)

    def get_subject_data(self, policy_id, data_id=None, category_id=None):
        return self.__get_perimeter_data(SubjectData, policy_id, data_id=data_id, category_id=category_id)

    def set_subject_data(self, policy_id, data_id=None, category_id=None, value=None):
        return self.__set_perimeter_data(Subject, SubjectData, policy_id, data_id=data_id, category_id=category_id, value=value)

    def delete_subject_data(self, policy_id, data_id):
        return self.__delete_perimeter_data(SubjectData, policy_id, data_id)

    def get_object_data(self, policy_id, data_id=None, category_id=None):
        return self.__get_perimeter_data(ObjectData, policy_id, data_id=data_id, category_id=category_id)

    def set_object_data(self, policy_id, data_id=None, category_id=None, value=None):
        return self.__set_perimeter_data(Object, ObjectData, policy_id, data_id=data_id, category_id=category_id, value=value)

    def delete_object_data(self, policy_id, data_id):
        return self.__delete_perimeter_data(ObjectData, policy_id, data_id)

    def get_action_data(self, policy_id, data_id=None, category_id=None):
        return self.__get_perimeter_data(ActionData, policy_id, data_id=data_id, category_id=category_id)

    def set_action_data(self, policy_id, data_id=None, category_id=None, value=None):
        return self.__set_perimeter_data(Action, ActionData, policy_id, data_id=data_id, category_id=category_id, value=value)

    def delete_action_data(self, policy_id, data_id):
        return self.__delete_perimeter_data(ActionData, policy_id, data_id)

    def get_subject_assignments(self, policy_id, subject_id=None, category_id=None):
        with self.get_session_for_write() as session:
            query = session.query(SubjectAssignment)
            if subject_id and category_id:
                #TODO change the subject_id to perimeter_id to allow code refactoring
                query = query.filter_by(policy_id=policy_id, subject_id=subject_id, category_id=category_id)
            elif subject_id:
                query = query.filter_by(policy_id=policy_id, subject_id=subject_id)
            else:
                query = query.filter_by(policy_id=policy_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict() for _ref in ref_list}

    def add_subject_assignment(self, policy_id, subject_id, category_id, data_id):
        with self.get_session_for_write() as session:
            query = session.query(SubjectAssignment)
            query = query.filter_by(policy_id=policy_id, subject_id=subject_id, category_id=category_id)
            ref = query.first()
            if ref:
                old_ref = copy.deepcopy(ref.to_dict())
                assignments = old_ref["assignments"]
                if data_id not in assignments:
                    assignments.append(data_id)
                    setattr(ref, "assignments", assignments)
            else:
                ref = SubjectAssignment.from_dict(
                    {
                        "id": uuid4().hex,
                        "policy_id": policy_id,
                        "subject_id": subject_id,
                        "category_id": category_id,
                        "assignments": [data_id, ],
                    }
                )
                session.add(ref)
            return {ref.id: ref.to_dict()}

    def delete_subject_assignment(self, policy_id, subject_id, category_id, data_id):
        with self.get_session_for_write() as session:
            query = session.query(SubjectAssignment)
            query = query.filter_by(policy_id=policy_id, subject_id=subject_id, category_id=category_id)
            ref = query.first()
            if ref:
                old_ref = copy.deepcopy(ref.to_dict())
                assignments = old_ref["assignments"]
                # TODO (asteroide): if data_id is None, delete all
                if data_id in assignments:
                    assignments.remove(data_id)
                    # FIXME (asteroide): the setattr doesn't work here ; the assignments is not updated in the database
                    setattr(ref, "assignments", assignments)
                if not assignments:
                    session.delete(ref)

    def get_object_assignments(self, policy_id, object_id=None, category_id=None):
        with self.get_session_for_write() as session:
            query = session.query(ObjectAssignment)
            if object_id and category_id:
                #TODO change the object_id to perimeter_id to allow code refactoring
                query = query.filter_by(policy_id=policy_id, object_id=object_id, category_id=category_id)
            elif object_id:
                query = query.filter_by(policy_id=policy_id, object_id=object_id)
            else:
                query = query.filter_by(policy_id=policy_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict() for _ref in ref_list}

    def add_object_assignment(self, policy_id, object_id, category_id, data_id):
        with self.get_session_for_write() as session:
            query = session.query(ObjectAssignment)
            query = query.filter_by(policy_id=policy_id, object_id=object_id, category_id=category_id)
            ref = query.first()
            if ref:
                old_ref = copy.deepcopy(ref.to_dict())
                assignments = old_ref["assignments"]
                if data_id not in assignments:
                    assignments.append(data_id)
                    setattr(ref, "assignments", assignments)
            else:
                ref = ObjectAssignment.from_dict(
                    {
                        "id": uuid4().hex,
                        "policy_id": policy_id,
                        "object_id": object_id,
                        "category_id": category_id,
                        "assignments": [data_id, ],
                    }
                )
                session.add(ref)
            return {ref.id: ref.to_dict()}

    def delete_object_assignment(self, policy_id, object_id, category_id, data_id):
        with self.get_session_for_write() as session:
            query = session.query(ObjectAssignment)
            query = query.filter_by(policy_id=policy_id, object_id=object_id, category_id=category_id)
            ref = query.first()
            if ref:
                old_ref = copy.deepcopy(ref.to_dict())
                assignments = old_ref["assignments"]
                # TODO (asteroide): if data_id is None, delete all
                if data_id in assignments:
                    assignments.remove(data_id)
                    # FIXME (asteroide): the setattr doesn't work here ; the assignments is not updated in the database
                    setattr(ref, "assignments", assignments)
                if not assignments:
                    session.delete(ref)

    def get_action_assignments(self, policy_id, action_id=None, category_id=None):
        with self.get_session_for_write() as session:
            query = session.query(ActionAssignment)
            if action_id and category_id:
                # TODO change the action_id to perimeter_id to allow code refactoring
                query = query.filter_by(policy_id=policy_id, action_id=action_id, category_id=category_id)
            elif action_id:
                query = query.filter_by(policy_id=policy_id, action_id=action_id)
            else:
                query = query.filter_by(policy_id=policy_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict() for _ref in ref_list}

    def add_action_assignment(self, policy_id, action_id, category_id, data_id):
        with self.get_session_for_write() as session:
            query = session.query(ActionAssignment)
            query = query.filter_by(policy_id=policy_id, action_id=action_id, category_id=category_id)
            ref = query.first()
            if ref:
                old_ref = copy.deepcopy(ref.to_dict())
                assignments = old_ref["assignments"]
                if data_id not in assignments:
                    assignments.append(data_id)
                    setattr(ref, "assignments", assignments)
            else:
                ref = ActionAssignment.from_dict(
                    {
                        "id": uuid4().hex,
                        "policy_id": policy_id,
                        "action_id": action_id,
                        "category_id": category_id,
                        "assignments": [data_id, ],
                    }
                )
                session.add(ref)
            return {ref.id: ref.to_dict()}

    def delete_action_assignment(self, policy_id, action_id, category_id, data_id):
        with self.get_session_for_write() as session:
            query = session.query(ActionAssignment)
            query = query.filter_by(policy_id=policy_id, action_id=action_id, category_id=category_id)
            ref = query.first()
            if ref:
                old_ref = copy.deepcopy(ref.to_dict())
                assignments = old_ref["assignments"]
                # TODO (asteroide): if data_id is None, delete all
                if data_id in assignments:
                    assignments.remove(data_id)
                    # FIXME (asteroide): the setattr doesn't work here ; the assignments is not updated in the database
                    setattr(ref, "assignments", assignments)
                if not assignments:
                    session.delete(ref)

    def get_rules(self, policy_id, rule_id=None, meta_rule_id=None):
        with self.get_session_for_read() as session:
            query = session.query(Rule)
            if rule_id:
                query = query.filter_by(policy_id=policy_id, rule_id=rule_id)
                ref = query.first()
                return {ref.id: ref.to_dict()}
            elif meta_rule_id:
                query = query.filter_by(policy_id=policy_id, meta_rule_id=meta_rule_id)
                ref_list = query.all()
                return {
                    "meta_rule_id": meta_rule_id,
                    "policy_id": policy_id,
                    "rules": list(map(lambda x: x.to_dict(), ref_list))
                }
            else:
                query = query.filter_by(policy_id=policy_id)
                ref_list = query.all()
                return {
                    "policy_id": policy_id,
                    "rules": list(map(lambda x: x.to_dict(), ref_list))
                }

    def add_rule(self, policy_id, meta_rule_id, value):
        with self.get_session_for_write() as session:
            query = session.query(Rule)
            query = query.filter_by(policy_id=policy_id, meta_rule_id=meta_rule_id)
            ref_list = query.all()
            rules = list(map(lambda x: x.rule, ref_list))
            if not rules or value not in rules:
                logger.info("add_rule IN IF")
                ref = Rule.from_dict(
                    {
                        "id": uuid4().hex,
                        "policy_id": policy_id,
                        "meta_rule_id": meta_rule_id,
                        "rule": value
                    }
                )
                session.add(ref)
                return {ref.id: ref.to_dict()}
            return {}

    def delete_rule(self, policy_id, rule_id):
        with self.get_session_for_write() as session:
            query = session.query(Rule)
            query = query.filter_by(policy_id=policy_id, id=rule_id)
            ref = query.first()
            if ref:
                session.delete(ref)


class ModelConnector(BaseConnector, ModelDriver):

    def update_model(self, model_id, value):
        with self.get_session_for_write() as session:
            query = session.query(Model)
            if model_id:
                query = query.filter_by(id=model_id)
            ref = query.first()
            if ref:
                d = dict(ref.value)
                d.update(value)
                setattr(ref, "value", d)
            return {ref.id: ref.to_dict()}

    def delete_model(self, model_id):
        with self.get_session_for_write() as session:
            ref = session.query(Model).get(model_id)
            session.delete(ref)

    def add_model(self, model_id=None, value=None):
        with self.get_session_for_write() as session:
            new = Model.from_dict({
                "id": model_id if model_id else uuid4().hex,
                "value": value
            })
            session.add(new)
            return {new.id: new.to_dict()}

    def get_models(self, model_id=None):
        with self.get_session_for_read() as session:
            query = session.query(Model)
            if model_id:
                ref_list = query.filter(Model.id == model_id)
            else:
                ref_list = query.all()
            return {_ref.id: _ref.to_dict() for _ref in ref_list}

    def set_meta_rule(self, meta_rule_id, value):
        with self.get_session_for_write() as session:
            query = session.query(MetaRule)
            query = query.filter_by(id=meta_rule_id)
            ref = query.first()
            if not ref:
                ref = MetaRule.from_dict(
                    {
                        "id": meta_rule_id if meta_rule_id else uuid4().hex,
                        "value": value
                    }
                )
                session.add(ref)
            else:
                setattr(ref, "value", value)
            return {ref.id: ref.to_dict()}

    def get_meta_rules(self, meta_rule_id=None):
        with self.get_session_for_read() as session:
            query = session.query(MetaRule)
            if meta_rule_id:
                query = query.filter_by(id=meta_rule_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict() for _ref in ref_list}

    def delete_meta_rule(self, meta_rule_id=None):
        with self.get_session_for_write() as session:
            query = session.query(MetaRule)
            query = query.filter_by(id=meta_rule_id)
            ref = query.first()
            if ref:
                session.delete(ref)

    def __get_perimeter_categories(self, ClassType, category_id=None):
        with self.get_session_for_read() as session:
            query = session.query(ClassType)
            if category_id:
                query = query.filter_by(id=category_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict() for _ref in ref_list}

    def __add_perimeter_category(self, ClassType, name, description, uuid=None):
        if not name:
            raise exceptions.CategoryNameInvalid
        with self.get_session_for_write() as session:
            query = session.query(ClassType)
            query = query.filter_by(name=name)
            ref = query.first()
            if not ref:
                ref = ClassType.from_dict(
                    {
                        "id": uuid if uuid else uuid4().hex,
                        "name": name,
                        "description": description
                    }
                )
                session.add(ref)
            return {ref.id: ref.to_dict()}

    def __delete_perimeter_category(self, ClassType, category_id):
        with self.get_session_for_write() as session:
            query = session.query(ClassType)
            query = query.filter_by(id=category_id)
            ref = query.first()
            if ref:
                session.delete(ref)

    def get_subject_categories(self, category_id=None):
        return self.__get_perimeter_categories(SubjectCategory, category_id=category_id)

    def add_subject_category(self, name, description, uuid=None):
        return self.__add_perimeter_category(SubjectCategory, name, description, uuid=uuid)

    def delete_subject_category(self, category_id):
        self.__delete_perimeter_category(SubjectCategory, category_id)

    def get_object_categories(self, category_id=None):
        return self.__get_perimeter_categories(ObjectCategory, category_id=category_id)

    def add_object_category(self, name, description, uuid=None):
        return self.__add_perimeter_category(ObjectCategory, name, description, uuid=uuid)

    def delete_object_category(self, category_id):
        self.__delete_perimeter_category(ObjectCategory, category_id)

    def get_action_categories(self, category_id=None):
        return self.__get_perimeter_categories(ActionCategory, category_id=category_id)

    def add_action_category(self, name, description, uuid=None):
        return self.__add_perimeter_category(ActionCategory, name, description, uuid=uuid)

    def delete_action_category(self, category_id):
        self.__delete_perimeter_category(ActionCategory, category_id)

    # Getter and Setter for subject_category

    # def get_subject_categories_dict(self, intra_extension_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(SubjectCategory)
    #         query = query.filter_by(intra_extension_id=intra_extension_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.subject_category for _ref in ref_list}
    #
    # def set_subject_category_dict(self, intra_extension_id, subject_category_id, subject_category_dict):
    #     with self.get_session_for_write() as session:
    #         query = session.query(SubjectCategory)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=subject_category_id)
    #         ref = query.first()
    #         new_ref = SubjectCategory.from_dict(
    #             {
    #                 "id": subject_category_id,
    #                 'subject_category': subject_category_dict,
    #                 'intra_extension_id': intra_extension_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in SubjectCategory.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # # session.flush()
    #         return {subject_category_id: SubjectCategory.to_dict(ref)['subject_category']}
    #
    # def del_subject_category(self, intra_extension_id, subject_category_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(SubjectCategory)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=subject_category_id)
    #         ref = query.first()
    #         self.del_subject_assignment(intra_extension_id, None, None, None)
    #         session.delete(ref)
    #
    # # Getter and Setter for object_category
    #
    # def get_object_categories_dict(self, intra_extension_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(ObjectCategory)
    #         query = query.filter_by(intra_extension_id=intra_extension_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.object_category for _ref in ref_list}
    #
    # def set_object_category_dict(self, intra_extension_id, object_category_id, object_category_dict):
    #     with self.get_session_for_write() as session:
    #         query = session.query(ObjectCategory)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=object_category_id)
    #         ref = query.first()
    #         new_ref = ObjectCategory.from_dict(
    #             {
    #                 "id": object_category_id,
    #                 'object_category': object_category_dict,
    #                 'intra_extension_id': intra_extension_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in ObjectCategory.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return {object_category_id: ObjectCategory.to_dict(ref)['object_category']}
    #
    # def del_object_category(self, intra_extension_id, object_category_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(ObjectCategory)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=object_category_id)
    #         ref = query.first()
    #         self.del_object_assignment(intra_extension_id, None, None, None)
    #         session.delete(ref)
    #
    # # Getter and Setter for action_category
    #
    # def get_action_categories_dict(self, intra_extension_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(ActionCategory)
    #         query = query.filter_by(intra_extension_id=intra_extension_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.action_category for _ref in ref_list}
    #
    # def set_action_category_dict(self, intra_extension_id, action_category_id, action_category_dict):
    #     with self.get_session_for_write() as session:
    #         query = session.query(ActionCategory)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=action_category_id)
    #         ref = query.first()
    #         new_ref = ActionCategory.from_dict(
    #             {
    #                 "id": action_category_id,
    #                 'action_category': action_category_dict,
    #                 'intra_extension_id': intra_extension_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in ActionCategory.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return {action_category_id: ActionCategory.to_dict(ref)['action_category']}
    #
    # def del_action_category(self, intra_extension_id, action_category_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(ActionCategory)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=action_category_id)
    #         ref = query.first()
    #         self.del_action_assignment(intra_extension_id, None, None, None)
    #         session.delete(ref)

    # Perimeter

    # def get_subjects_dict(self, intra_extension_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(Subject)
    #         query = query.filter_by(intra_extension_id=intra_extension_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.subject for _ref in ref_list}
    #
    # def set_subject_dict(self, intra_extension_id, subject_id, subject_dict):
    #     with self.get_session_for_write() as session:
    #         query = session.query(Subject)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=subject_id)
    #         ref = query.first()
    #         # if 'id' in subject_dict:
    #         #     subject_dict['id'] = subject_id
    #         new_ref = Subject.from_dict(
    #             {
    #                 "id": subject_id,
    #                 'subject': subject_dict,
    #                 'intra_extension_id': intra_extension_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in Subject.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return {subject_id: Subject.to_dict(ref)['subject']}
    #
    # def del_subject(self, intra_extension_id, subject_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(Subject)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=subject_id)
    #         ref = query.first()
    #         session.delete(ref)
    #
    # def get_objects_dict(self, intra_extension_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(Object)
    #         query = query.filter_by(intra_extension_id=intra_extension_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.object for _ref in ref_list}
    #
    # def set_object_dict(self, intra_extension_id, object_id, object_dict):
    #     with self.get_session_for_write() as session:
    #         query = session.query(Object)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=object_id)
    #         ref = query.first()
    #         new_ref = Object.from_dict(
    #             {
    #                 "id": object_id,
    #                 'object': object_dict,
    #                 'intra_extension_id': intra_extension_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in Object.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return {object_id: Object.to_dict(ref)['object']}
    #
    # def del_object(self, intra_extension_id, object_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(Object)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=object_id)
    #         ref = query.first()
    #         session.delete(ref)
    #
    # def get_actions_dict(self, intra_extension_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(Action)
    #         query = query.filter_by(intra_extension_id=intra_extension_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.action for _ref in ref_list}
    #
    # def set_action_dict(self, intra_extension_id, action_id, action_dict):
    #     with self.get_session_for_write() as session:
    #         query = session.query(Action)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=action_id)
    #         ref = query.first()
    #         new_ref = Action.from_dict(
    #             {
    #                 "id": action_id,
    #                 'action': action_dict,
    #                 'intra_extension_id': intra_extension_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in Action.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return {action_id: Action.to_dict(ref)['action']}
    #
    # def del_action(self, intra_extension_id, action_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(Action)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=action_id)
    #         ref = query.first()
    #         session.delete(ref)

    # Getter and Setter for subject_scope

    # def get_subject_scopes_dict(self, intra_extension_id, subject_category_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(SubjectScope)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, subject_category_id=subject_category_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.subject_scope for _ref in ref_list}
    #
    # def set_subject_scope_dict(self, intra_extension_id, subject_category_id, subject_scope_id, subject_scope_dict):
    #     with self.get_session_for_write() as session:
    #         query = session.query(SubjectScope)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, subject_category_id=subject_category_id, id=subject_scope_id)
    #         ref = query.first()
    #         new_ref = SubjectScope.from_dict(
    #             {
    #                 "id": subject_scope_id,
    #                 'subject_scope': subject_scope_dict,
    #                 'intra_extension_id': intra_extension_id,
    #                 'subject_category_id': subject_category_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in Subject.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return {subject_scope_id: SubjectScope.to_dict(ref)['subject_scope']}
    #
    # def del_subject_scope(self, intra_extension_id, subject_category_id, subject_scope_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(SubjectScope)
    #         if not subject_category_id or not subject_scope_id:
    #             query = query.filter_by(intra_extension_id=intra_extension_id)
    #             for ref in query.all():
    #                 session.delete(ref)
    #         else:
    #             query = query.filter_by(intra_extension_id=intra_extension_id, subject_category_id=subject_category_id, id=subject_scope_id)
    #             ref = query.first()
    #             session.delete(ref)
    #
    # # Getter and Setter for object_category_scope
    #
    # def get_object_scopes_dict(self, intra_extension_id, object_category_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(ObjectScope)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, object_category_id=object_category_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.object_scope for _ref in ref_list}
    #
    # def set_object_scope_dict(self, intra_extension_id, object_category_id, object_scope_id, object_scope_dict):
    #     with self.get_session_for_write() as session:
    #         query = session.query(ObjectScope)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, object_category_id=object_category_id, id=object_scope_id)
    #         ref = query.first()
    #         new_ref = ObjectScope.from_dict(
    #             {
    #                 "id": object_scope_id,
    #                 'object_scope': object_scope_dict,
    #                 'intra_extension_id': intra_extension_id,
    #                 'object_category_id': object_category_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in Object.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return {object_scope_id: ObjectScope.to_dict(ref)['object_scope']}
    #
    # def del_object_scope(self, intra_extension_id, object_category_id, object_scope_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(ObjectScope)
    #         if not object_category_id or not object_scope_id:
    #             query = query.filter_by(intra_extension_id=intra_extension_id)
    #             for ref in query.all():
    #                 session.delete(ref)
    #         else:
    #             query = query.filter_by(intra_extension_id=intra_extension_id, object_category_id=object_category_id, id=object_scope_id)
    #             ref = query.first()
    #             session.delete(ref)
    #
    # # Getter and Setter for action_scope
    #
    # def get_action_scopes_dict(self, intra_extension_id, action_category_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(ActionScope)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, action_category_id=action_category_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.action_scope for _ref in ref_list}
    #
    # def set_action_scope_dict(self, intra_extension_id, action_category_id, action_scope_id, action_scope_dict):
    #     with self.get_session_for_write() as session:
    #         query = session.query(ActionScope)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, action_category_id=action_category_id, id=action_scope_id)
    #         ref = query.first()
    #         new_ref = ActionScope.from_dict(
    #             {
    #                 "id": action_scope_id,
    #                 'action_scope': action_scope_dict,
    #                 'intra_extension_id': intra_extension_id,
    #                 'action_category_id': action_category_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in Action.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return {action_scope_id: ActionScope.to_dict(ref)['action_scope']}
    #
    # def del_action_scope(self, intra_extension_id, action_category_id, action_scope_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(ActionScope)
    #         if not action_category_id or not action_scope_id:
    #             query = query.filter_by(intra_extension_id=intra_extension_id)
    #             for ref in query.all():
    #                 session.delete(ref)
    #         else:
    #             query = query.filter_by(intra_extension_id=intra_extension_id, action_category_id=action_category_id, id=action_scope_id)
    #             ref = query.first()
    #             session.delete(ref)
    #
    # # Getter and Setter for subject_category_assignment
    #
    # def get_subject_assignment_list(self, intra_extension_id, subject_id, subject_category_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(SubjectAssignment)
    #         if not subject_id or not subject_category_id or not subject_category_id:
    #             query = query.filter_by(intra_extension_id=intra_extension_id)
    #             ref = query.all()
    #             return ref
    #         else:
    #             query = query.filter_by(intra_extension_id=intra_extension_id, subject_id=subject_id, subject_category_id=subject_category_id)
    #             ref = query.first()
    #         if not ref:
    #             return list()
    #         LOG.info("get_subject_assignment_list {}".format(ref.subject_assignment))
    #         return list(ref.subject_assignment)
    #
    # def set_subject_assignment_list(self, intra_extension_id, subject_id, subject_category_id, subject_assignment_list=[]):
    #     with self.get_session_for_write() as session:
    #         query = session.query(SubjectAssignment)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, subject_id=subject_id, subject_category_id=subject_category_id)
    #         ref = query.first()
    #         new_ref = SubjectAssignment.from_dict(
    #             {
    #                 "id": uuid4().hex,
    #                 'subject_assignment': subject_assignment_list,
    #                 'intra_extension_id': intra_extension_id,
    #                 'subject_id': subject_id,
    #                 'subject_category_id': subject_category_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in SubjectAssignment.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return subject_assignment_list
    #
    # def add_subject_assignment_list(self, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
    #     new_subject_assignment_list = self.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id)
    #     if subject_scope_id not in new_subject_assignment_list:
    #         new_subject_assignment_list.append(subject_scope_id)
    #     return self.set_subject_assignment_list(intra_extension_id, subject_id, subject_category_id, new_subject_assignment_list)
    #
    # def del_subject_assignment(self, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
    #     if not subject_id or not subject_category_id or not subject_category_id:
    #         with self.get_session_for_write() as session:
    #             for ref in self.get_subject_assignment_list(intra_extension_id, None, None):
    #                 session.delete(ref)
    #             session.flush()
    #             return
    #     new_subject_assignment_list = self.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id)
    #     new_subject_assignment_list.remove(subject_scope_id)
    #     return self.set_subject_assignment_list(intra_extension_id, subject_id, subject_category_id, new_subject_assignment_list)
    #
    # # Getter and Setter for object_category_assignment
    #
    # def get_object_assignment_list(self, intra_extension_id, object_id, object_category_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(ObjectAssignment)
    #         if not object_id or not object_category_id or not object_category_id:
    #             query = query.filter_by(intra_extension_id=intra_extension_id)
    #             ref = query.all()
    #             return ref
    #         else:
    #             query = query.filter_by(intra_extension_id=intra_extension_id, object_id=object_id, object_category_id=object_category_id)
    #             ref = query.first()
    #         if not ref:
    #             return list()
    #         return list(ref.object_assignment)
    #
    # def set_object_assignment_list(self, intra_extension_id, object_id, object_category_id, object_assignment_list=[]):
    #     with self.get_session_for_write() as session:
    #         query = session.query(ObjectAssignment)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, object_id=object_id, object_category_id=object_category_id)
    #         ref = query.first()
    #         new_ref = ObjectAssignment.from_dict(
    #             {
    #                 "id": uuid4().hex,
    #                 'object_assignment': object_assignment_list,
    #                 'intra_extension_id': intra_extension_id,
    #                 'object_id': object_id,
    #                 'object_category_id': object_category_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #         else:
    #             for attr in ObjectAssignment.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return self.get_object_assignment_list(intra_extension_id, object_id, object_category_id)
    #
    # def add_object_assignment_list(self, intra_extension_id, object_id, object_category_id, object_scope_id):
    #     new_object_assignment_list = self.get_object_assignment_list(intra_extension_id, object_id, object_category_id)
    #     if object_scope_id not in new_object_assignment_list:
    #         new_object_assignment_list.append(object_scope_id)
    #     return self.set_object_assignment_list(intra_extension_id, object_id, object_category_id, new_object_assignment_list)
    #
    # def del_object_assignment(self, intra_extension_id, object_id, object_category_id, object_scope_id):
    #     if not object_id or not object_category_id or not object_category_id:
    #         with self.get_session_for_write() as session:
    #             for ref in self.get_object_assignment_list(intra_extension_id, None, None):
    #                 session.delete(ref)
    #             session.flush()
    #             return
    #     new_object_assignment_list = self.get_object_assignment_list(intra_extension_id, object_id, object_category_id)
    #     new_object_assignment_list.remove(object_scope_id)
    #     return self.set_object_assignment_list(intra_extension_id, object_id, object_category_id, new_object_assignment_list)
    #
    # # Getter and Setter for action_category_assignment
    #
    # def get_action_assignment_list(self, intra_extension_id, action_id, action_category_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(ActionAssignment)
    #         if not action_id or not action_category_id or not action_category_id:
    #             query = query.filter_by(intra_extension_id=intra_extension_id)
    #             ref = query.all()
    #             return ref
    #         else:
    #             query = query.filter_by(intra_extension_id=intra_extension_id, action_id=action_id, action_category_id=action_category_id)
    #             ref = query.first()
    #         if not ref:
    #             return list()
    #         return list(ref.action_assignment)
    #
    # def set_action_assignment_list(self, intra_extension_id, action_id, action_category_id, action_assignment_list=[]):
    #     with self.get_session_for_write() as session:
    #         query = session.query(ActionAssignment)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, action_id=action_id, action_category_id=action_category_id)
    #         ref = query.first()
    #         new_ref = ActionAssignment.from_dict(
    #             {
    #                 "id": uuid4().hex,
    #                 'action_assignment': action_assignment_list,
    #                 'intra_extension_id': intra_extension_id,
    #                 'action_id': action_id,
    #                 'action_category_id': action_category_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #         else:
    #             for attr in ActionAssignment.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return self.get_action_assignment_list(intra_extension_id, action_id, action_category_id)
    #
    # def add_action_assignment_list(self, intra_extension_id, action_id, action_category_id, action_scope_id):
    #     new_action_assignment_list = self.get_action_assignment_list(intra_extension_id, action_id, action_category_id)
    #     if action_scope_id not in new_action_assignment_list:
    #         new_action_assignment_list.append(action_scope_id)
    #     return self.set_action_assignment_list(intra_extension_id, action_id, action_category_id, new_action_assignment_list)
    #
    # def del_action_assignment(self, intra_extension_id, action_id, action_category_id, action_scope_id):
    #     if not action_id or not action_category_id or not action_category_id:
    #         with self.get_session_for_write() as session:
    #             for ref in self.get_action_assignment_list(intra_extension_id, None, None):
    #                 session.delete(ref)
    #             session.flush()
    #             return
    #     new_action_assignment_list = self.get_action_assignment_list(intra_extension_id, action_id, action_category_id)
    #     new_action_assignment_list.remove(action_scope_id)
    #     return self.set_action_assignment_list(intra_extension_id, action_id, action_category_id, new_action_assignment_list)
    #
    # # Getter and Setter for sub_meta_rule
    #
    # def get_aggregation_algorithm_id(self, intra_extension_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(IntraExtension)
    #         query = query.filter_by(id=intra_extension_id)
    #         ref = query.first()
    #         try:
    #             return {"aggregation_algorithm": ref.intra_extension["aggregation_algorithm"]}
    #         except KeyError:
    #             return ""
    #
    # def set_aggregation_algorithm_id(self, intra_extension_id, aggregation_algorithm_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(IntraExtension)
    #         query = query.filter_by(id=intra_extension_id)
    #         ref = query.first()
    #         intra_extension_dict = dict(ref.intra_extension)
    #         intra_extension_dict["aggregation_algorithm"] = aggregation_algorithm_id
    #         setattr(ref, "intra_extension", intra_extension_dict)
    #         # session.flush()
    #         return {"aggregation_algorithm": ref.intra_extension["aggregation_algorithm"]}
    #
    # def del_aggregation_algorithm(self, intra_extension_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(IntraExtension)
    #         query = query.filter_by(id=intra_extension_id)
    #         ref = query.first()
    #         intra_extension_dict = dict(ref.intra_extension)
    #         intra_extension_dict["aggregation_algorithm"] = ""
    #         setattr(ref, "intra_extension", intra_extension_dict)
    #         return self.get_aggregation_algorithm_id(intra_extension_id)
    #
    # # Getter and Setter for sub_meta_rule
    #
    # def get_sub_meta_rules_dict(self, intra_extension_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(SubMetaRule)
    #         query = query.filter_by(intra_extension_id=intra_extension_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.sub_meta_rule for _ref in ref_list}
    #
    # def set_sub_meta_rule_dict(self, intra_extension_id, sub_meta_rule_id, sub_meta_rule_dict):
    #     with self.get_session_for_write() as session:
    #         query = session.query(SubMetaRule)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=sub_meta_rule_id)
    #         ref = query.first()
    #         new_ref = SubMetaRule.from_dict(
    #             {
    #                 "id": sub_meta_rule_id,
    #                 'sub_meta_rule': sub_meta_rule_dict,
    #                 'intra_extension_id': intra_extension_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #         else:
    #             _sub_meta_rule_dict = dict(ref.sub_meta_rule)
    #             _sub_meta_rule_dict.update(sub_meta_rule_dict)
    #             setattr(new_ref, "sub_meta_rule", _sub_meta_rule_dict)
    #             for attr in SubMetaRule.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return self.get_sub_meta_rules_dict(intra_extension_id)
    #
    # def del_sub_meta_rule(self, intra_extension_id, sub_meta_rule_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(SubMetaRule)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, id=sub_meta_rule_id)
    #         ref = query.first()
    #         session.delete(ref)
    #
    # # Getter and Setter for rules
    #
    # def get_rules_dict(self, intra_extension_id, sub_meta_rule_id):
    #     with self.get_session_for_read() as session:
    #         query = session.query(Rule)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, sub_meta_rule_id=sub_meta_rule_id)
    #         ref_list = query.all()
    #         return {_ref.id: _ref.rule for _ref in ref_list}
    #
    # def set_rule_dict(self, intra_extension_id, sub_meta_rule_id, rule_id, rule_list):
    #     with self.get_session_for_write() as session:
    #         query = session.query(Rule)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, sub_meta_rule_id=sub_meta_rule_id, id=rule_id)
    #         ref = query.first()
    #         new_ref = Rule.from_dict(
    #             {
    #                 "id": rule_id,
    #                 'rule': rule_list,
    #                 'intra_extension_id': intra_extension_id,
    #                 'sub_meta_rule_id': sub_meta_rule_id
    #             }
    #         )
    #         if not ref:
    #             session.add(new_ref)
    #             ref = new_ref
    #         else:
    #             for attr in Rule.attributes:
    #                 if attr != 'id':
    #                     setattr(ref, attr, getattr(new_ref, attr))
    #         # session.flush()
    #         return {rule_id: ref.rule}
    #
    # def del_rule(self, intra_extension_id, sub_meta_rule_id, rule_id):
    #     with self.get_session_for_write() as session:
    #         query = session.query(Rule)
    #         query = query.filter_by(intra_extension_id=intra_extension_id, sub_meta_rule_id=sub_meta_rule_id, id=rule_id)
    #         ref = query.first()
    #         session.delete(ref)


class SQLConnector(PDPConnector, PolicyConnector, ModelConnector):
    pass
