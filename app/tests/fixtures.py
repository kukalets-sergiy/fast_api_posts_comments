import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def jwt_token(request):
    user_data = {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "test_password"
    }
    response = client.post("/auth_user/register", json=user_data)
    print(f"Registration response status code: {response.status_code}")
    print(f"Registration response body: {response.text}")
    if response.status_code == 400 and response.json().get("detail") == "Email already registered":
        pass
    else:
        assert response.status_code == 200

    token_response = client.post("/auth_user/login", json=user_data)
    print(f"Login response status code: {token_response.status_code}")
    print(f"Login response body: {token_response.text}")
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    print(f"Token response status code: {token}")

    return token
