import pytest


def test_register_and_get_student(data_client):
    payload = {
        "personal": {
            "user_id": "user-1",
            "full_name": "Test User",
            "age": 21,
            "is_international": False,
        },
        "academic": {
            "user_id": "user-1",
            "current_semester": 2,
            "taken_courses": ["CIS 1001"],
            "taken_geneds": ["GA"],
        },
    }
    resp = data_client.post("/register-student", json=payload)
    assert resp.status_code == 200

    fetched = data_client.get("/students/user-1")
    assert fetched.status_code == 200
    body = fetched.json()
    assert body["personal"]["full_name"] == "Test User"
    assert body["academic"]["current_semester"] == 2
    assert body["academic"]["taken_courses"] == ["CIS 1001"]


def test_register_upserts_existing_student(data_client):
    first = {
        "personal": {"user_id": "user-2", "full_name": "First", "age": 18, "is_international": True},
        "academic": {"user_id": "user-2", "current_semester": 1, "taken_courses": [], "taken_geneds": []},
    }
    updated = {
        "personal": {"user_id": "user-2", "full_name": "First Last", "age": 19, "is_international": True},
        "academic": {"user_id": "user-2", "current_semester": 2, "taken_courses": ["CIS 1001"], "taken_geneds": []},
    }
    assert data_client.post("/register-student", json=first).status_code == 200
    assert data_client.post("/register-student", json=updated).status_code == 200

    fetched = data_client.get("/students/user-2").json()
    assert fetched["personal"]["age"] == 19
    assert fetched["academic"]["current_semester"] == 2
    assert fetched["academic"]["taken_courses"] == ["CIS 1001"]


def test_save_and_get_schedule(data_client):
    payload = {
        "personal": {"user_id": "sched-1", "full_name": "Schedule User", "age": 20, "is_international": False},
        "academic": {"user_id": "sched-1", "current_semester": 1, "taken_courses": [], "taken_geneds": []},
    }
    data_client.post("/register-student", json=payload)

    schedule = {"user_id": "sched-1", "schedule": {"courses": [{"course": "CIS 1001"}], "total_credits": 3}}
    resp = data_client.post("/students/schedules", json=schedule)
    assert resp.status_code == 200

    fetched = data_client.get("/students/schedules/sched-1")
    assert fetched.status_code == 200
    assert fetched.json()["schedule"]["total_credits"] == 3


def test_get_schedule_returns_404_when_missing(data_client):
    missing = data_client.get("/students/schedules/unknown-user")
    assert missing.status_code == 404


def test_conversation_save_load_and_delete(data_client):
    user_id = "conv-1"
    convo = ["Hi", "Assistant reply"]
    resp = data_client.post("/students/conversation", json={"user_id": user_id, "conversation": convo})
    assert resp.status_code == 200

    fetched = data_client.get(f"/students/conversation/{user_id}")
    assert fetched.status_code == 200
    assert fetched.json()["conversation"] == convo

    delete_resp = data_client.delete(f"/students/conversation/{user_id}")
    assert delete_resp.status_code == 200
    fetched_after = data_client.get(f"/students/conversation/{user_id}")
    assert fetched_after.status_code == 200
    assert fetched_after.json()["conversation"] == []


def test_delete_student_clears_related_records(data_client):
    user_id = "delete-me"
    data_client.post(
        "/register-student",
        json={
            "personal": {"user_id": user_id, "full_name": "Name", "age": 20, "is_international": False},
            "academic": {"user_id": user_id, "current_semester": 1, "taken_courses": [], "taken_geneds": []},
        },
    )
    data_client.post("/students/schedules", json={"user_id": user_id, "schedule": {"courses": [], "total_credits": 0}})
    data_client.post("/students/conversation", json={"user_id": user_id, "conversation": ["hi"]})

    assert data_client.delete(f"/students/{user_id}").status_code == 200

    student = data_client.get(f"/students/{user_id}").json()
    assert student["personal"] is None
    assert student["academic"] is None
    assert data_client.get(f"/students/schedules/{user_id}").status_code == 404
    assert data_client.get(f"/students/conversation/{user_id}").json()["conversation"] == []


def test_register_student_invalid_payload_returns_422(data_client):
    bad_payload = {"personal": {"user_id": "oops"}}
    resp = data_client.post("/register-student", json=bad_payload)
    assert resp.status_code == 422
