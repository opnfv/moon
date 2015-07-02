# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import six
from uuid import uuid4
import copy

from keystone import config
from oslo_log import log
from keystone.common import sql
from keystone import exception
from keystone.contrib.moon.exception import *
from oslo_serialization import jsonutils
from keystone.contrib.moon import IntraExtensionDriver
from keystone.contrib.moon import TenantDriver
# from keystone.contrib.moon import InterExtensionDriver

from keystone.contrib.moon.exception import TenantException, TenantListEmpty

CONF = config.CONF
LOG = log.getLogger(__name__)


class IntraExtension(sql.ModelBase, sql.DictBase):
    __tablename__ = 'intra_extension'
    attributes = ['id', 'name', 'model', 'description']
    id = sql.Column(sql.String(64), primary_key=True)
    name = sql.Column(sql.String(64), nullable=False)
    model = sql.Column(sql.String(64), nullable=True)
    description = sql.Column(sql.Text())

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class Subject(sql.ModelBase, sql.DictBase):
    __tablename__ = 'subject'
    attributes = ['id', 'subjects', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    subjects = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class Object(sql.ModelBase, sql.DictBase):
    __tablename__ = 'object'
    attributes = ['id', 'objects', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    objects = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class Action(sql.ModelBase, sql.DictBase):
    __tablename__ = 'action'
    attributes = ['id', 'actions', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    actions = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class SubjectCategory(sql.ModelBase, sql.DictBase):
    __tablename__ = 'subject_category'
    attributes = ['id', 'subject_categories', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    subject_categories = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ObjectCategory(sql.ModelBase, sql.DictBase):
    __tablename__ = 'object_category'
    attributes = ['id', 'object_categories', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    object_categories = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ActionCategory(sql.ModelBase, sql.DictBase):
    __tablename__ = 'action_category'
    attributes = ['id', 'action_categories', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    action_categories = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class SubjectCategoryScope(sql.ModelBase, sql.DictBase):
    __tablename__ = 'subject_category_scope'
    attributes = ['id', 'subject_category_scope', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    subject_category_scope = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ObjectCategoryScope(sql.ModelBase, sql.DictBase):
    __tablename__ = 'object_category_scope'
    attributes = ['id', 'object_category_scope', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    object_category_scope = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ActionCategoryScope(sql.ModelBase, sql.DictBase):
    __tablename__ = 'action_category_scope'
    attributes = ['id', 'action_category_scope', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    action_category_scope = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class SubjectCategoryAssignment(sql.ModelBase, sql.DictBase):
    __tablename__ = 'subject_category_assignment'
    attributes = ['id', 'subject_category_assignments', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    subject_category_assignments = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ObjectCategoryAssignment(sql.ModelBase, sql.DictBase):
    __tablename__ = 'object_category_assignment'
    attributes = ['id', 'object_category_assignments', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    object_category_assignments = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ActionCategoryAssignment(sql.ModelBase, sql.DictBase):
    __tablename__ = 'action_category_assignment'
    attributes = ['id', 'action_category_assignments', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    action_category_assignments = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class MetaRule(sql.ModelBase, sql.DictBase):
    __tablename__ = 'metarule'
    attributes = ['id', 'sub_meta_rules', 'aggregation', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    sub_meta_rules = sql.Column(sql.JsonBlob(), nullable=True)
    aggregation = sql.Column(sql.Text(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class Rule(sql.ModelBase, sql.DictBase):
    __tablename__ = 'rule'
    attributes = ['id', 'rules', 'intra_extension_uuid']
    id = sql.Column(sql.String(64), primary_key=True)
    rules = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_uuid = sql.Column(sql.ForeignKey("intra_extension.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class Tenant(sql.ModelBase, sql.DictBase):
    __tablename__ = 'tenants'
    attributes = [
        'id', 'name', 'authz', 'admin'
    ]
    id = sql.Column(sql.String(64), primary_key=True, nullable=False)
    name = sql.Column(sql.String(128), nullable=True)
    authz = sql.Column(sql.String(64), nullable=True)
    admin = sql.Column(sql.String(64), nullable=True)

    @classmethod
    def from_dict(cls, d):
        """Override parent from_dict() method with a different implementation.
        """
        new_d = d.copy()
        uuid = new_d.keys()[0]
        return cls(id=uuid, **new_d[uuid])

    def to_dict(self):
        """
        """
        tenant_dict = {}
        for key in ("id", "name", "authz", "admin"):
            tenant_dict[key] = getattr(self, key)
        return tenant_dict

__all_objects__ = (
    Subject,
    Object,
    Action,
    SubjectCategory,
    ObjectCategory,
    ActionCategory,
    SubjectCategoryScope,
    ObjectCategoryScope,
    ActionCategoryScope,
    SubjectCategoryAssignment,
    ObjectCategoryAssignment,
    ActionCategoryAssignment,
    MetaRule,
    Rule,
)

class IntraExtensionConnector(IntraExtensionDriver):

    def get_intra_extension_list(self):
        with sql.transaction() as session:
            query = session.query(IntraExtension.id)
            intraextensions = query.all()
            # return intraextensions
            return [intraextension[0] for intraextension in intraextensions]

    def set_intra_extension(self, intra_id, intra_extension):
        with sql.transaction() as session:
            # intra_extension["admin"] = jsonutils.dumps(intra_extension["admin"])
            # intra_extension["authz"] = jsonutils.dumps(intra_extension["authz"])
            ie_ref = IntraExtension.from_dict(intra_extension)
            session.add(ie_ref)
            return IntraExtension.to_dict(ie_ref)

    def get_intra_extension(self, uuid):
        with sql.transaction() as session:
            query = session.query(IntraExtension)
            query = query.filter_by(id=uuid)
            ref = query.first()
            if not ref:
                raise exception.NotFound
            return ref.to_dict()

    def delete_intra_extension(self, intra_extension_id):
        with sql.transaction() as session:
            ref = session.query(IntraExtension).get(intra_extension_id)
            # Must delete all references to that IntraExtension
            for _object in __all_objects__:
                query = session.query(_object)
                query = query.filter_by(intra_extension_uuid=intra_extension_id)
                _ref = query.first()
                if _ref:
                    session.delete(_ref)
            session.flush()
            session.delete(ref)

    # Getter and setter for name

    def get_name(self, uuid):
        intra_extension = self.get_intra_extension(uuid)
        return intra_extension["name"]

    def set_name(self, uuid, name):
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and setter for model

    def get_model(self, uuid):
        intra_extension = self.get_intra_extension(uuid)
        return intra_extension["model"]

    def set_model(self, uuid, model):
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and setter for description

    def get_description(self, uuid):
        intra_extension = self.get_intra_extension(uuid)
        return intra_extension["description"]

    def set_description(self, uuid, args):
        raise exception.NotImplemented()  # pragma: no cover

    def get_subject_dict(self, extension_uuid):
        with sql.transaction() as session:
            query = session.query(Subject)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            return ref.to_dict()

    def set_subject_dict(self, extension_uuid, subject_uuid):
        with sql.transaction() as session:
            query = session.query(Subject)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            new_ref = Subject.from_dict(
                {
                    "id": uuid4().hex,
                    'subjects': subject_uuid,
                    'intra_extension_uuid': extension_uuid
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in Subject.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_subject(self, extension_uuid, subject_uuid, subject_name):
        with sql.transaction() as session:
            query = session.query(Subject)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            subjects = dict(old_ref["subjects"])
            subjects[subject_uuid] = subject_name
            new_ref = Subject.from_dict(
                {
                    "id": old_ref["id"],
                    'subjects': subjects,
                    'intra_extension_uuid': old_ref["intra_extension_uuid"]
                }
            )
            for attr in Subject.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return {"subject": {"uuid": subject_uuid, "name": subject_name}}

    def remove_subject(self, extension_uuid, subject_uuid):
        with sql.transaction() as session:
            query = session.query(Subject)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            else:
                old_ref = ref.to_dict()
                subjects = dict(old_ref["subjects"])
                try:
                    subjects.pop(subject_uuid)
                except KeyError:
                    LOG.error("KeyError in remove_subject {} | {}".format(subject_uuid, subjects))
                else:
                    new_ref = Subject.from_dict(
                        {
                            "id": old_ref["id"],
                            'subjects': subjects,
                            'intra_extension_uuid': old_ref["intra_extension_uuid"]
                        }
                    )
                    for attr in Subject.attributes:
                        if attr != 'id':
                            setattr(ref, attr, getattr(new_ref, attr))

    def get_object_dict(self, extension_uuid):
        with sql.transaction() as session:
            query = session.query(Object)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            return ref.to_dict()

    def set_object_dict(self, extension_uuid, object_uuid):
        with sql.transaction() as session:
            query = session.query(Object)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            new_ref = Object.from_dict(
                {
                    "id": uuid4().hex,
                    'objects': object_uuid,
                    'intra_extension_uuid': extension_uuid
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in Object.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_object(self, extension_uuid, object_uuid, object_name):
        with sql.transaction() as session:
            query = session.query(Object)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            objects = dict(old_ref["objects"])
            objects[object_uuid] = object_name
            new_ref = Object.from_dict(
                {
                    "id": old_ref["id"],
                    'objects': objects,
                    'intra_extension_uuid': old_ref["intra_extension_uuid"]
                }
            )
            for attr in Object.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return {"object": {"uuid": object_uuid, "name": object_name}}

    def remove_object(self, extension_uuid, object_uuid):
        with sql.transaction() as session:
            query = session.query(Object)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            else:
                old_ref = ref.to_dict()
                objects = dict(old_ref["objects"])
                try:
                    objects.pop(object_uuid)
                except KeyError:
                    LOG.error("KeyError in remove_object {} | {}".format(object_uuid, objects))
                else:
                    new_ref = Object.from_dict(
                        {
                            "id": old_ref["id"],
                            'objects': objects,
                            'intra_extension_uuid': old_ref["intra_extension_uuid"]
                        }
                    )
                    for attr in Object.attributes:
                        if attr != 'id':
                            setattr(ref, attr, getattr(new_ref, attr))

    def get_action_dict(self, extension_uuid):
        with sql.transaction() as session:
            query = session.query(Action)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            return ref.to_dict()

    def set_action_dict(self, extension_uuid, action_uuid):
        with sql.transaction() as session:
            query = session.query(Action)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            new_ref = Action.from_dict(
                {
                    "id": uuid4().hex,
                    'actions': action_uuid,
                    'intra_extension_uuid': extension_uuid
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in Action.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_action(self, extension_uuid, action_uuid, action_name):
        with sql.transaction() as session:
            query = session.query(Action)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            actions = dict(old_ref["actions"])
            actions[action_uuid] = action_name
            new_ref = Action.from_dict(
                {
                    "id": old_ref["id"],
                    'actions': actions,
                    'intra_extension_uuid': old_ref["intra_extension_uuid"]
                }
            )
            for attr in Action.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return {"action": {"uuid": action_uuid, "name": action_name}}

    def remove_action(self, extension_uuid, action_uuid):
        with sql.transaction() as session:
            query = session.query(Action)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            else:
                old_ref = ref.to_dict()
                actions = dict(old_ref["actions"])
                try:
                    actions.pop(action_uuid)
                except KeyError:
                    LOG.error("KeyError in remove_action {} | {}".format(action_uuid, actions))
                else:
                    new_ref = Action.from_dict(
                        {
                            "id": old_ref["id"],
                            'actions': actions,
                            'intra_extension_uuid': old_ref["intra_extension_uuid"]
                        }
                    )
                    for attr in Action.attributes:
                        if attr != 'id':
                            setattr(ref, attr, getattr(new_ref, attr))

    # Getter and Setter for subject_category

    def get_subject_category_dict(self, extension_uuid):
        with sql.transaction() as session:
            query = session.query(SubjectCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            return ref.to_dict()

    def set_subject_category_dict(self, extension_uuid, subject_categories):
        with sql.transaction() as session:
            query = session.query(SubjectCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            new_ref = SubjectCategory.from_dict(
                {
                    "id": uuid4().hex,
                    'subject_categories': subject_categories,
                    'intra_extension_uuid': extension_uuid
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in SubjectCategory.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_subject_category_dict(self, extension_uuid, subject_category_uuid, subject_category_name):
        with sql.transaction() as session:
            query = session.query(SubjectCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            subject_categories = dict(old_ref["subject_categories"])
            subject_categories[subject_category_uuid] = subject_category_name
            new_ref = SubjectCategory.from_dict(
                {
                    "id": old_ref["id"],
                    'subject_categories': subject_categories,
                    'intra_extension_uuid': old_ref["intra_extension_uuid"]
                }
            )
            for attr in SubjectCategory.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return {"subject_category": {"uuid": subject_category_uuid, "name": subject_category_name}}

    def remove_subject_category(self, extension_uuid, subject_category_uuid):
        with sql.transaction() as session:
            query = session.query(SubjectCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            else:
                old_ref = ref.to_dict()
                subject_categories = dict(old_ref["subject_categories"])
                try:
                    subject_categories.pop(subject_category_uuid)
                except KeyError:
                    pass
                else:
                    new_ref = SubjectCategory.from_dict(
                        {
                            "id": old_ref["id"],
                            'subject_categories': subject_categories,
                            'intra_extension_uuid': old_ref["intra_extension_uuid"]
                        }
                    )
                    for attr in SubjectCategory.attributes:
                        if attr != 'id':
                            setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Getter and Setter for object_category

    def get_object_category_dict(self, extension_uuid):
        with sql.transaction() as session:
            query = session.query(ObjectCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            return ref.to_dict()

    def set_object_category_dict(self, extension_uuid, object_categories):
        with sql.transaction() as session:
            query = session.query(ObjectCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            new_ref = ObjectCategory.from_dict(
                {
                    "id": uuid4().hex,
                    'object_categories': object_categories,
                    'intra_extension_uuid': extension_uuid
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in ObjectCategory.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_object_category_dict(self, extension_uuid, object_category_uuid, object_category_name):
        with sql.transaction() as session:
            query = session.query(ObjectCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            object_categories = dict(old_ref["object_categories"])
            object_categories[object_category_uuid] = object_category_name
            new_ref = ObjectCategory.from_dict(
                {
                    "id": old_ref["id"],
                    'object_categories': object_categories,
                    'intra_extension_uuid': old_ref["intra_extension_uuid"]
                }
            )
            for attr in ObjectCategory.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return {"object_category": {"uuid": object_category_uuid, "name": object_category_name}}

    def remove_object_category(self, extension_uuid, object_category_uuid):
        with sql.transaction() as session:
            query = session.query(ObjectCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            else:
                old_ref = ref.to_dict()
                object_categories = dict(old_ref["object_categories"])
                try:
                    object_categories.pop(object_category_uuid)
                except KeyError:
                    pass
                else:
                    new_ref = ObjectCategory.from_dict(
                        {
                            "id": old_ref["id"],
                            'object_categories': object_categories,
                            'intra_extension_uuid': old_ref["intra_extension_uuid"]
                        }
                    )
                    for attr in ObjectCategory.attributes:
                        if attr != 'id':
                            setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Getter and Setter for action_category

    def get_action_category_dict(self, extension_uuid):
        with sql.transaction() as session:
            query = session.query(ActionCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            return ref.to_dict()

    def set_action_category_dict(self, extension_uuid, action_categories):
        with sql.transaction() as session:
            query = session.query(ActionCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            new_ref = ActionCategory.from_dict(
                {
                    "id": uuid4().hex,
                    'action_categories': action_categories,
                    'intra_extension_uuid': extension_uuid
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in ActionCategory.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_action_category_dict(self, extension_uuid, action_category_uuid, action_category_name):
        with sql.transaction() as session:
            query = session.query(ActionCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            action_categories = dict(old_ref["action_categories"])
            action_categories[action_category_uuid] = action_category_name
            new_ref = ActionCategory.from_dict(
                {
                    "id": old_ref["id"],
                    'action_categories': action_categories,
                    'intra_extension_uuid': old_ref["intra_extension_uuid"]
                }
            )
            for attr in ActionCategory.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return {"action_category": {"uuid": action_category_uuid, "name": action_category_name}}

    def remove_action_category(self, extension_uuid, action_category_uuid):
        with sql.transaction() as session:
            query = session.query(ActionCategory)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            else:
                old_ref = ref.to_dict()
                action_categories = dict(old_ref["action_categories"])
                try:
                    action_categories.pop(action_category_uuid)
                except KeyError:
                    pass
                else:
                    new_ref = ActionCategory.from_dict(
                        {
                            "id": old_ref["id"],
                            'action_categories': action_categories,
                            'intra_extension_uuid': old_ref["intra_extension_uuid"]
                        }
                    )
                    for attr in ActionCategory.attributes:
                        if attr != 'id':
                            setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Getter and Setter for subject_category_value_scope

    def get_subject_category_scope_dict(self, extension_uuid, subject_category):
        with sql.transaction() as session:
            query = session.query(SubjectCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            result = copy.deepcopy(ref.to_dict())
            if subject_category not in result["subject_category_scope"].keys():
                raise AuthzMetadata()
            result["subject_category_scope"] = {subject_category: result["subject_category_scope"][subject_category]}
            return result

    def set_subject_category_scope_dict(self, extension_uuid, subject_category, scope):
        with sql.transaction() as session:
            query = session.query(SubjectCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                new_ref = SubjectCategoryScope.from_dict(
                    {
                        "id": uuid4().hex,
                        'subject_category_scope': {subject_category: scope},
                        'intra_extension_uuid': extension_uuid
                    }
                )
                session.add(new_ref)
                ref = new_ref
            else:
                tmp_ref = ref.to_dict()
                tmp_ref['subject_category_scope'].update({subject_category: scope})
                session.delete(ref)
                new_ref = SubjectCategoryScope.from_dict(tmp_ref)
                session.add(new_ref)
            return ref.to_dict()

    def add_subject_category_scope_dict(self, extension_uuid, subject_category, scope_uuid, scope_name):
        with sql.transaction() as session:
            query = session.query(SubjectCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            scope = copy.deepcopy(old_ref["subject_category_scope"])
            if subject_category not in scope.keys():
                scope[subject_category] = dict()
            scope[subject_category][scope_uuid] = scope_name
            self.set_subject_category_scope_dict(extension_uuid, subject_category, scope[subject_category])
            return {"subject_category_scope": {"uuid": scope_uuid, "name": scope_name}}

    def remove_subject_category_scope_dict(self, extension_uuid, subject_category, scope_uuid):
        with sql.transaction() as session:
            query = session.query(SubjectCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            scope = dict(old_ref["subject_category_scope"])
            if subject_category not in scope:
                return
            try:
                scope[subject_category].pop(scope_uuid)
            except KeyError:
                return
            new_ref = SubjectCategoryScope.from_dict(
                {
                    "id": old_ref["id"],
                    'subject_category_scope': scope,
                    'intra_extension_uuid': old_ref["intra_extension_uuid"]
                }
            )
            for attr in SubjectCategoryScope.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Getter and Setter for object_category_scope

    def get_object_category_scope_dict(self, extension_uuid, object_category):
        with sql.transaction() as session:
            query = session.query(ObjectCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            result = copy.deepcopy(ref.to_dict())
            if object_category not in result["object_category_scope"].keys():
                raise AuthzMetadata()
            result["object_category_scope"] = {object_category: result["object_category_scope"][object_category]}
            return result

    def set_object_category_scope_dict(self, extension_uuid, object_category, scope):
        with sql.transaction() as session:
            query = session.query(ObjectCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                new_ref = ObjectCategoryScope.from_dict(
                    {
                        "id": uuid4().hex,
                        'object_category_scope': {object_category: scope},
                        'intra_extension_uuid': extension_uuid
                    }
                )
                session.add(new_ref)
                ref = new_ref
            else:
                tmp_ref = ref.to_dict()
                tmp_ref['object_category_scope'].update({object_category: scope})
                session.delete(ref)
                new_ref = ObjectCategoryScope.from_dict(tmp_ref)
                session.add(new_ref)
            return ref.to_dict()

    def add_object_category_scope_dict(self, extension_uuid, object_category, scope_uuid, scope_name):
        with sql.transaction() as session:
            query = session.query(ObjectCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            scope = dict(old_ref["object_category_scope"])
            if object_category not in scope:
                scope[object_category] = dict()
            scope[object_category][scope_uuid] = scope_name
            self.set_object_category_scope_dict(extension_uuid, object_category, scope[object_category])
            return {"object_category_scope": {"uuid": scope_uuid, "name": scope_name}}

    def remove_object_category_scope_dict(self, extension_uuid, object_category, scope_uuid):
        with sql.transaction() as session:
            query = session.query(ObjectCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            scope = dict(old_ref["object_category_scope"])
            if object_category not in scope:
                return
            try:
                scope[object_category].pop(scope_uuid)
            except KeyError:
                return
            new_ref = ObjectCategoryScope.from_dict(
                {
                    "id": old_ref["id"],
                    'object_category_scope': scope,
                    'intra_extension_uuid': old_ref["intra_extension_uuid"]
                }
            )
            for attr in ObjectCategoryScope.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Getter and Setter for action_category_scope
 
    def get_action_category_scope_dict(self, extension_uuid, action_category):
        with sql.transaction() as session:
            query = session.query(ActionCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            result = copy.deepcopy(ref.to_dict())
            if action_category not in result["action_category_scope"].keys():
                raise AuthzMetadata("Unknown category id {}/{}".format(action_category, result["action_category_scope"].keys()))
            result["action_category_scope"] = {action_category: result["action_category_scope"][action_category]}
            return result

    def set_action_category_scope_dict(self, extension_uuid, action_category, scope):
        with sql.transaction() as session:
            query = session.query(ActionCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                new_ref = ActionCategoryScope.from_dict(
                    {
                        "id": uuid4().hex,
                        'action_category_scope': {action_category: scope},
                        'intra_extension_uuid': extension_uuid
                    }
                )
                session.add(new_ref)
                ref = new_ref
            else:
                tmp_ref = ref.to_dict()
                tmp_ref['action_category_scope'].update({action_category: scope})
                session.delete(ref)
                new_ref = ActionCategoryScope.from_dict(tmp_ref)
                session.add(new_ref)
            return ref.to_dict()

    def add_action_category_scope_dict(self, extension_uuid, action_category, scope_uuid, scope_name):
        with sql.transaction() as session:
            query = session.query(ActionCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            scope = dict(old_ref["action_category_scope"])
            if action_category not in scope:
                scope[action_category] = dict()
            scope[action_category][scope_uuid] = scope_name
            self.set_action_category_scope_dict(extension_uuid, action_category, scope[action_category])
            return {"action_category_scope": {"uuid": scope_uuid, "name": scope_name}}

    def remove_action_category_scope_dict(self, extension_uuid, action_category, scope_uuid):
        with sql.transaction() as session:
            query = session.query(ActionCategoryScope)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            scope = dict(old_ref["action_category_scope"])
            if action_category not in scope:
                return
            try:
                scope[action_category].pop(scope_uuid)
            except KeyError:
                return
            new_ref = ActionCategoryScope.from_dict(
                {
                    "id": old_ref["id"],
                    'action_category_scope': scope,
                    'intra_extension_uuid': old_ref["intra_extension_uuid"]
                }
            )
            for attr in ActionCategoryScope.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Getter and Setter for subject_category_assignment

    def get_subject_category_assignment_dict(self, extension_uuid, subject_uuid):
        """ From a subject_uuid, return a dictionary of (category: scope for that subject)

        :param extension_uuid: intra extension UUID
        :param subject_uuid: subject UUID
        :return: a dictionary of (keys are category nd values are scope for that subject)
        """
        with sql.transaction() as session:
            query = session.query(SubjectCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound("get_subject_category_assignment_dict")
            _ref = ref.to_dict()
            if subject_uuid in _ref["subject_category_assignments"]:
                _backup_dict = _ref["subject_category_assignments"][subject_uuid]
                _ref["subject_category_assignments"] = dict()
                _ref["subject_category_assignments"][subject_uuid] = _backup_dict
            else:
                _ref["subject_category_assignments"] = dict()
                _ref["subject_category_assignments"][subject_uuid] = dict()
            return _ref

    def set_subject_category_assignment_dict(self, extension_uuid, subject_uuid=None, assignment_dict={}):
        with sql.transaction() as session:
            query = session.query(SubjectCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if type(assignment_dict) is not dict:
                raise IntraExtensionError()
            for value in assignment_dict.values():
                if type(value) is not list:
                    raise IntraExtensionError(str(value))
            if not subject_uuid:
                subject_category_assignments = {}
            else:
                subject_category_assignments = {subject_uuid: assignment_dict}
            new_ref = SubjectCategoryAssignment.from_dict(
                {
                    "id": uuid4().hex,
                    'subject_category_assignments': subject_category_assignments,
                    'intra_extension_uuid': extension_uuid
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                new_ref.subject_category_assignments[subject_uuid] = assignment_dict
                for attr in SubjectCategoryAssignment.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_subject_category_assignment_dict(self, extension_uuid, subject_uuid, category_uuid, scope_uuid):
        with sql.transaction() as session:
            query = session.query(SubjectCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            assignments = ref.to_dict()['subject_category_assignments']
            if subject_uuid not in assignments:
                assignments[subject_uuid] = dict()
            if category_uuid not in assignments[subject_uuid]:
                assignments[subject_uuid][category_uuid] = list()
            if scope_uuid not in assignments[subject_uuid][category_uuid]:
                assignments[subject_uuid][category_uuid].append(scope_uuid)
            return self.set_subject_category_assignment_dict(
                extension_uuid,
                subject_uuid,
                assignments[subject_uuid])

    def remove_subject_category_assignment(self, extension_uuid, subject_uuid, category_uuid, scope_uuid):
        with sql.transaction() as session:
            query = session.query(SubjectCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            if subject_uuid in old_ref["subject_category_assignments"]:
                if category_uuid in old_ref["subject_category_assignments"][subject_uuid]:
                    old_ref["subject_category_assignments"][subject_uuid][category_uuid].remove(scope_uuid)
                    if not old_ref["subject_category_assignments"][subject_uuid][category_uuid]:
                        old_ref["subject_category_assignments"][subject_uuid].pop(category_uuid)
                    if not old_ref["subject_category_assignments"][subject_uuid]:
                        old_ref["subject_category_assignments"].pop(subject_uuid)
            try:
                self.set_subject_category_assignment_dict(
                    extension_uuid,
                    subject_uuid,
                    old_ref["subject_category_assignments"][subject_uuid])
            except KeyError:
                self.set_subject_category_assignment_dict(
                    extension_uuid,
                    subject_uuid,
                    {})

    # Getter and Setter for object_category_assignment

    def get_object_category_assignment_dict(self, extension_uuid, object_uuid):
        """ From a object_uuid, return a dictionary of (category: scope for that object)

        :param extension_uuid: intra extension UUID
        :param object_uuid: object UUID
        :return: a dictionary of (keys are category nd values are scope for that object)
        """
        with sql.transaction() as session:
            query = session.query(ObjectCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            _ref = ref.to_dict()
            if object_uuid in _ref["object_category_assignments"]:
                _backup_dict = _ref["object_category_assignments"][object_uuid]
                _ref["object_category_assignments"] = dict()
                _ref["object_category_assignments"][object_uuid] = _backup_dict
            else:
                _ref["object_category_assignments"] = dict()
                _ref["object_category_assignments"][object_uuid] = dict()
            return _ref

    def set_object_category_assignment_dict(self, extension_uuid, object_uuid=None, assignment_dict={}):
        with sql.transaction() as session:
            query = session.query(ObjectCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if type(assignment_dict) is not dict:
                raise IntraExtensionError()
            for value in assignment_dict.values():
                if type(value) is not list:
                    raise IntraExtensionError(str(value))
            new_ref = ObjectCategoryAssignment.from_dict(
                {
                    "id": uuid4().hex,
                    'object_category_assignments': {object_uuid: assignment_dict},
                    'intra_extension_uuid': extension_uuid
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                new_ref.object_category_assignments[object_uuid] = assignment_dict
                for attr in ObjectCategoryAssignment.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_object_category_assignment_dict(self, extension_uuid, object_uuid, category_uuid, scope_uuid):
        with sql.transaction() as session:
            query = session.query(ObjectCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            assignments = ref.to_dict()['object_category_assignments']
            if object_uuid not in assignments:
                assignments[object_uuid] = dict()
            if category_uuid not in assignments[object_uuid]:
                assignments[object_uuid][category_uuid] = list()
            if scope_uuid not in assignments[object_uuid][category_uuid]:
                assignments[object_uuid][category_uuid].append(scope_uuid)
            return self.set_object_category_assignment_dict(
                extension_uuid,
                object_uuid,
                assignments[object_uuid])

    def remove_object_category_assignment(self, extension_uuid, object_uuid, category_uuid, scope_uuid):
        with sql.transaction() as session:
            query = session.query(ObjectCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            if object_uuid in old_ref["object_category_assignments"]:
                if category_uuid in old_ref["object_category_assignments"][object_uuid]:
                    old_ref["object_category_assignments"][object_uuid][category_uuid].remove(scope_uuid)
                    if not old_ref["object_category_assignments"][object_uuid][category_uuid]:
                        old_ref["object_category_assignments"][object_uuid].pop(category_uuid)
                    if not old_ref["object_category_assignments"][object_uuid]:
                        old_ref["object_category_assignments"].pop(object_uuid)
            self.set_object_category_assignment_dict(
                extension_uuid,
                object_uuid,
                old_ref["object_category_assignments"][object_uuid])

    # Getter and Setter for action_category_assignment

    def get_action_category_assignment_dict(self, extension_uuid, action_uuid):
        """ From a action_uuid, return a dictionary of (category: scope for that action)

        :param extension_uuid: intra extension UUID
        :param action_uuid: action UUID
        :return: a dictionary of (keys are category nd values are scope for that action)
        """
        with sql.transaction() as session:
            query = session.query(ActionCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            _ref = ref.to_dict()
            if action_uuid in _ref["action_category_assignments"]:
                _backup_dict = _ref["action_category_assignments"][action_uuid]
                _ref["action_category_assignments"] = dict()
                _ref["action_category_assignments"][action_uuid] = _backup_dict
            else:
                _ref["action_category_assignments"] = dict()
                _ref["action_category_assignments"][action_uuid] = dict()
            return _ref

    def set_action_category_assignment_dict(self, extension_uuid, action_uuid=None, assignment_dict={}):
        with sql.transaction() as session:
            query = session.query(ActionCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if type(assignment_dict) is not dict:
                raise IntraExtensionError()
            for value in assignment_dict.values():
                if type(value) is not list:
                    raise IntraExtensionError(str(value))
            new_ref = ActionCategoryAssignment.from_dict(
                {
                    "id": uuid4().hex,
                    'action_category_assignments': {action_uuid: assignment_dict},
                    'intra_extension_uuid': extension_uuid
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                new_ref.action_category_assignments[action_uuid] = assignment_dict
                for attr in ActionCategoryAssignment.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_action_category_assignment_dict(self, extension_uuid, action_uuid, category_uuid, scope_uuid):
        with sql.transaction() as session:
            query = session.query(ActionCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            assignments = ref.to_dict()['action_category_assignments']
            if action_uuid not in assignments:
                assignments[action_uuid] = dict()
            if category_uuid not in assignments[action_uuid]:
                assignments[action_uuid][category_uuid] = list()
            if scope_uuid not in assignments[action_uuid][category_uuid]:
                assignments[action_uuid][category_uuid].append(scope_uuid)
            return self.set_action_category_assignment_dict(
                extension_uuid,
                action_uuid,
                assignments[action_uuid])

    def remove_action_category_assignment(self, extension_uuid, action_uuid, category_uuid, scope_uuid):
        with sql.transaction() as session:
            query = session.query(ActionCategoryAssignment)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            old_ref = ref.to_dict()
            if action_uuid in old_ref["action_category_assignments"]:
                if category_uuid in old_ref["action_category_assignments"][action_uuid]:
                    old_ref["action_category_assignments"][action_uuid][category_uuid].remove(scope_uuid)
                    if not old_ref["action_category_assignments"][action_uuid][category_uuid]:
                        old_ref["action_category_assignments"][action_uuid].pop(category_uuid)
                    if not old_ref["action_category_assignments"][action_uuid]:
                        old_ref["action_category_assignments"].pop(action_uuid)
            self.set_action_category_assignment_dict(
                extension_uuid,
                action_uuid,
                old_ref["action_category_assignments"][action_uuid])

    # Getter and Setter for meta_rule

    def get_meta_rule_dict(self, extension_uuid):
        with sql.transaction() as session:
            query = session.query(MetaRule)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            return ref.to_dict()

    def set_meta_rule_dict(self, extension_uuid, meta_rule):
        with sql.transaction() as session:
            query = session.query(MetaRule)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            meta_rule["id"] = uuid4().hex
            meta_rule["intra_extension_uuid"] = extension_uuid
            new_ref = MetaRule.from_dict(meta_rule)
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in MetaRule.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Getter and Setter for rules

    def get_rules(self, extension_uuid):
        with sql.transaction() as session:
            query = session.query(Rule)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            if not ref:
                raise IntraExtensionNotFound()
            return ref.to_dict()

    def set_rules(self, extension_uuid, subrules):
        with sql.transaction() as session:
            query = session.query(Rule)
            query = query.filter_by(intra_extension_uuid=extension_uuid)
            ref = query.first()
            rules = dict()
            rules["id"] = uuid4().hex
            rules["intra_extension_uuid"] = extension_uuid
            rules["rules"] = subrules
            new_ref = Rule.from_dict(rules)
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in Rule.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()


class TenantConnector(TenantDriver):

    def get_tenant_dict(self):
        with sql.transaction() as session:
            query = session.query(Tenant)
            # query = query.filter_by(uuid=tenant_uuid)
            # ref = query.first().to_dict()
            tenants = query.all()
            if not tenants:
                raise TenantListEmpty()
            return {tenant.id: Tenant.to_dict(tenant) for tenant in tenants}
            # return [Tenant.to_dict(tenant) for tenant in tenants]

    def set_tenant_dict(self, tenant):
        with sql.transaction() as session:
            uuid = tenant.keys()[0]
            query = session.query(Tenant)
            query = query.filter_by(id=uuid)
            ref = query.first()
            if not ref:
                # if not result, create the database line
                ref = Tenant.from_dict(tenant)
                session.add(ref)
                return Tenant.to_dict(ref)
            elif not tenant[uuid]["authz"] and not tenant[uuid]["admin"]:
                # if admin and authz extensions are not set, delete the mapping
                session.delete(ref)
                return
            elif tenant[uuid]["authz"] or tenant[uuid]["admin"]:
                tenant_ref = ref.to_dict()
                tenant_ref.update(tenant[uuid])
                new_tenant = Tenant(
                    id=uuid,
                    name=tenant[uuid]["name"],
                    authz=tenant[uuid]["authz"],
                    admin=tenant[uuid]["admin"],
                )
                for attr in Tenant.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_tenant, attr))
                return Tenant.to_dict(ref)
            raise TenantException()


# class InterExtension(sql.ModelBase, sql.DictBase):
#     __tablename__ = 'inter_extension'
#     attributes = [
#         'id',
#         'requesting_intra_extension_uuid',
#         'requested_intra_extension_uuid',
#         'virtual_entity_uuid',
#         'genre',
#         'description',
#     ]
#     id = sql.Column(sql.String(64), primary_key=True)
#     requesting_intra_extension_uuid = sql.Column(sql.String(64))
#     requested_intra_extension_uuid = sql.Column(sql.String(64))
#     virtual_entity_uuid = sql.Column(sql.String(64))
#     genre = sql.Column(sql.String(64))
#     description = sql.Column(sql.Text())
#
#     @classmethod
#     def from_dict(cls, d):
#         """Override parent from_dict() method with a simpler implementation.
#         """
#         new_d = d.copy()
#         return cls(**new_d)
#
#     def to_dict(self):
#         """Override parent to_dict() method with a simpler implementation.
#         """
#         return dict(six.iteritems(self))
#
#
# class InterExtensionConnector(InterExtensionDriver):
#
#     def get_inter_extensions(self):
#         with sql.transaction() as session:
#             query = session.query(InterExtension.id)
#             interextensions = query.all()
#             return [interextension.id for interextension in interextensions]
#
#     def create_inter_extensions(self, inter_id, inter_extension):
#         with sql.transaction() as session:
#             ie_ref = InterExtension.from_dict(inter_extension)
#             session.add(ie_ref)
#         return InterExtension.to_dict(ie_ref)
#
#     def get_inter_extension(self, uuid):
#         with sql.transaction() as session:
#             query = session.query(InterExtension)
#             query = query.filter_by(id=uuid)
#             ref = query.first()
#             if not ref:
#                 raise exception.NotFound
#             return ref.to_dict()
#
#     def delete_inter_extensions(self, inter_extension_id):
#         with sql.transaction() as session:
#             ref = session.query(InterExtension).get(inter_extension_id)
#             session.delete(ref)

