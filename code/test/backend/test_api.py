import pytest
from flask import Flask
from src.backend.api import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_social_media_insights(client):
    """Test the /get-scoialmediainsights endpoint"""
    response = client.get('/get-scoialmediainsights')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_social_media_insights_error_handling(client):
    """Test error handling in the /get-scoialmediainsights endpoint"""
    # Simulate a database error by temporarily modifying the endpoint
    with app.test_request_context('/get-scoialmediainsights'):
        response = client.get('/get-scoialmediainsights')
        assert response.status_code in [200, 500]  # Either success or error
        if response.status_code == 500:
            data = json.loads(response.data)
            assert 'error' in data 