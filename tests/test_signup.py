from src.app import activities


def test_signup_adds_participant(client):
    # Arrange
    email = "test.student@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up test.student@mergington.edu for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up for this activity"}
    assert activities["Chess Club"]["participants"].count(email) == 1


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange

    # Act
    response = client.post("/activities/Drama Club/signup", params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered michael@mergington.edu from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_returns_404_for_missing_participant(client):
    # Arrange

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": "missing@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}