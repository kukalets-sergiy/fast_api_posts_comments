from app.tests.fixtures import jwt_token, client


def test_create_post(jwt_token):
    post_data = {
        "title": "Test Post",
        "content": "This is a test post."
    }
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/posts", json=post_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]


def test_create_post_with_toxic_content(jwt_token):
    post_data = {
        "title": "I hate them!",
        "content": "Go in hell!"
    }
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/posts/", json=post_data, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Post contains toxic content."


def test_create_post_without_toxic_content(jwt_token):
    post_data = {
        "title": "I like you!",
        "content": "You're doing great!"
    }
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/posts/", json=post_data, headers=headers)
    assert response.status_code == 200
