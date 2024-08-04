import time
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


# def test_auto_reply(jwt_token):
#     # Headers for authorization
#     headers = {"Authorization": f"Bearer {jwt_token}"}
#
#     # Create a post with auto-reply enabled
#     post_data = {
#         "title": "Test Post",
#         "content": "This is a test post",
#         "auto_reply_enabled": True,
#         "auto_reply_delay": 60
#     }
#     post_response = client.post("/posts/", json=post_data, headers=headers)
#     post_id = post_response.json()["id"]
#
#     # Create a comment on the post
#     comment_data = {
#         "content": "This is a test comment",
#         "post_id": post_id
#     }
#     comment_response = client.post("/comments/", json=comment_data, headers=headers)
#     comment_id = comment_response.json()["id"]
#
#     # Wait for the auto-reply task to be executed
#     time.sleep(70)  # Wait more than the delay to ensure the task has been executed
#
#     # Verify the auto-reply comment
#     auto_reply_response = client.get(f"/comments/{comment_id}")
#     assert auto_reply_response.status_code == 200
#     assert "Thank you for your comment" in auto_reply_response.json()["content"]
