import pytest
from utils import random_uuid
from mock_client import mock_client


@pytest.fixture
def slug():
    return "hectiq-ai/test2"


@pytest.fixture
def teardown_config():
    yield
    import os

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "dummy/configs.toml"))
    if os.path.exists(path):
        os.remove(path)


def test_project_create():
    from pyhectiqlab import Project
    from pyhectiqlab.client import Client
    import uuid

    id = str(uuid.uuid4())[:6]
    with mock_client(Project) as p:
        p.create(name="tests/" + id, write_config=False)


def test_project_write_config(slug, teardown_config):
    import os
    import toml
    from pyhectiqlab import Project

    current = Project._configs
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "dummy/configs.toml"))

    Project._configs = config_path
    Project.write_config(slug)
    config = toml.load(open(Project._configs, "r"))
    assert slug in config
    Project._configs = current


def test_project_retrieve(slug):
    from pyhectiqlab import Project

    project = Project.retrieve(slug)
    assert project["name"] == slug
    assert project["slug"] == slug


def test_project_exists(slug):
    from pyhectiqlab import Project
    import uuid

    fake_id = str(uuid.uuid4())[:6]

    assert Project.exists(slug)
    assert not Project.exists(slug + fake_id)


def test_project_set_get(slug):
    from pyhectiqlab import Project

    assert Project.get() == None
    Project.set(slug)
    assert Project.get() == slug


if __name__ == "__main__":
    pass
