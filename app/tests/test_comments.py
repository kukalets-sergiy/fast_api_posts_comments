import pytest
from app.tests.fixtures import jwt_token, client


def get_last_post_id(jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.get("/posts", headers=headers)
    assert response.status_code == 200
    posts = response.json()
    if not posts:
        pytest.fail("No posts found.")
    return posts[-1]["id"]


def test_create_comment(jwt_token):
    post_id = get_last_post_id(jwt_token)
    comment_data = {
        "content": "This is a test comment.",
        "post_id": post_id
    }
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/comments", json=comment_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == comment_data["content"]


def test_create_comment_with_toxic_content(jwt_token):
    post_id = get_last_post_id(jwt_token)
    comment_data = {
        "content": "I hate you!!",
        "post_id": post_id
    }
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/comments/", json=comment_data, headers=headers)
    assert response.json()["is_blocked"] == True


def test_create_comment_without_toxic_content(jwt_token):
    post_id = get_last_post_id(jwt_token)
    comment_data = {
        "content": "You're doing great!",
        "post_id": post_id
    }
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/comments/", json=comment_data, headers=headers)
    assert response.status_code == 200
