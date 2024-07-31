import datetime
from app.tests.fixtures import jwt_token, client


def test_comment_analytics(jwt_token):
    # headers for authorization
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # today's date
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    today_str = today.strftime("%Y-%m-%d")
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")

    # get initial analytics data
    start_response = client.get(f"/analytics/comments-daily-breakdown?date_from=2024-07-30&date_to={tomorrow_str}")
    assert start_response.status_code == 200
    start_data = start_response.json()

    # comment's data
    nice_content = {
        "content": "You're doing great!",
        "post_id": 1
    }
    toxic_content = {
        "content": "Go in hell!",
        "post_id": 1
    }

    # non-toxic comments creation
    response = client.post(
        "/comments/",
        json=nice_content,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["is_blocked"] == False
    nice_comment_id = response.json()["id"]

    # toxic comments creation
    response = client.post(
        "/comments/",
        json=toxic_content,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["is_blocked"] == True
    toxic_comment_id = response.json()["id"]

    # checking analytical data
    response = client.get(f"/analytics/comments-daily-breakdown?date_from=2024-07-30&date_to={tomorrow_str}")
    assert response.status_code == 200
    data = response.json()

    # checking that the last record in the data corresponds to the current date
    assert data[-1]['date'] == today_str

    # checking data for current date
    assert data[-1]['total_comments'] == start_data[-1]["total_comments"] + 2
    assert data[-1]['blocked_comments'] == start_data[-1]["blocked_comments"] + 1

    # checking that other data has not changed
    for i in range(len(start_data) - 1):
        assert data[i]['total_comments'] == start_data[i]['total_comments']
        assert data[i]['blocked_comments'] == start_data[i]['blocked_comments']

    # checking for unnecessary data
    assert len(data) == len(start_data)

    # checking data types
    for record in data:
        assert isinstance(record['date'], str)
        assert isinstance(record['total_comments'], int)
        assert isinstance(record['blocked_comments'], int)

    # clean up by deleting the test comments
    response = client.delete(f"/comments/delete/{nice_comment_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Comment was deleted successfully"

    response = client.delete(f"/comments/delete/{toxic_comment_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Comment was deleted successfully"
