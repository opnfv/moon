import pytest

print("ANALYSING CONFTEST")


@pytest.fixture
def context():
    print("CREATING CONTEXT")
    yield {
        "hostname": "manager",
        "port": 8082,
    }
