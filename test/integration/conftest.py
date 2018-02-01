import pytest

from chalice import Chalice
from apispec import APISpec


@pytest.fixture
def app():
    return Chalice(__name__)


@pytest.fixture
def spec():
    return APISpec(
        title='Swagger Petstore',
        version='1.0.0',
        plugins=[
            'apispec.ext.chalice',
        ],
    )
