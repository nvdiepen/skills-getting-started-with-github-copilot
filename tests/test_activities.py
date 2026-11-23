from src import app as app_module


def test_get_activities_returns_participants(client):
    response = client.get("/activities")

    assert response.status_code == 200
    chess = response.json()["Chess Club"]
    assert chess["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_adds_participant(client):
    response = client.post(
        "/activities/Chess Club/signup", params={"email": "new@mergington.edu"}
    )

    assert response.status_code == 200
    assert "new@mergington.edu" in app_module.activities["Chess Club"]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Nope/signup", params={"email": "a@b.c"})

    assert response.status_code == 404


def test_signup_duplicate_email_returns_409(client):
    response = client.post(
        "/activities/Chess Club/signup", params={"email": "michael@mergington.edu"}
    )

    assert response.status_code == 409
    assert app_module.activities["Chess Club"]["participants"].count("michael@mergington.edu") == 1


def test_signup_full_activity_returns_409(client):
    activity = app_module.activities["Chess Club"]
    activity["max_participants"] = len(activity["participants"])

    response = client.post(
        "/activities/Chess Club/signup", params={"email": "new@mergington.edu"}
    )

    assert response.status_code == 409
    assert "new@mergington.edu" not in activity["participants"]


def test_unregister_removes_participant(client):
    response = client.delete(
        "/activities/Chess Club/participants", params={"email": "michael@mergington.edu"}
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete("/activities/Nope/participants", params={"email": "a@b.c"})

    assert response.status_code == 404


def test_unregister_student_not_signed_up_returns_404(client):
    response = client.delete(
        "/activities/Chess Club/participants", params={"email": "stranger@mergington.edu"}
    )

    assert response.status_code == 404
