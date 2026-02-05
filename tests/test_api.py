from fastapi.testclient import TestClient
from src import app as app_module

client = TestClient(app_module.app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_unregister_flow():
    email = "pytest_user@example.com"
    activity = "Basketball"

    # ensure clean state
    if email in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].remove(email)

    # signup
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # duplicate signup should fail
    r2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert r2.status_code == 400

    # unregister
    r3 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r3.status_code == 200
    assert email not in app_module.activities[activity]["participants"]

    # unregistering again should fail
    r4 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r4.status_code == 400


def test_invalid_activity_errors():
    r = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert r.status_code == 404

    r2 = client.delete("/activities/NoSuchActivity/participants?email=a@b.com")
    assert r2.status_code == 404
