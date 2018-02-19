import pytest
import requests_mock
from . import mock_config

from .conf.conf_projects import *
from .conf.conf_models import *
from .conf.conf_pdps import *
from .conf.conf_action_categories import *
from .conf.conf_object_categories import *
from .conf.conf_subject_categories import *
from .conf.conf_meta_rules import *
from .conf.conf_action_assignments import *
from .conf.conf_object_assignments import *
from .conf.conf_subject_assignments import *
from .conf.conf_policies import *
from .conf.conf_subjects import *
from .conf.conf_objects import *
from .conf.conf_actions import *
from .conf.conf_subject_data import *
from .conf.conf_object_data import *
from .conf.conf_action_data import *
from .conf.conf_rules import *


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """ Modify the response from Requests module
    """
    with requests_mock.Mocker(real_http=True) as m:
        mock_config.register_consul(m)

        conf_projects(m)
        conf_models(m)
        conf_pdps(m)
        conf_action_categories(m)
        conf_object_categories(m)
        conf_subject_categories(m)
        conf_meta_rules(m)
        conf_policies(m)
        conf_subjects(m)
        conf_objects(m)
        conf_actions(m)
        conf_object_data(m)
        conf_subject_data(m)
        conf_action_data(m)
        conf_action_assignments(m)
        conf_object_assignments(m)
        conf_subject_assignments(m)
        conf_rule_assignments(m)
        yield m


