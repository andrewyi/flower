import pytest
from merchant import create_app


@pytest.fixture
def app():
    return create_app('test')
