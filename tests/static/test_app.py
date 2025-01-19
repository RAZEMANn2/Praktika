import pytest
from app import app
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Upload an Image' in rv.data


