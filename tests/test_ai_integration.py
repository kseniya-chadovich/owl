import pytest


def test_dialog_returns_mocked_schedule(ai_client):
    resp = ai_client.post(
        "/dialog",
        json={
            "user_id": "ai-user-1",
            "message": "I want 12 credits",
            "academic": {"current_semester": 1, "taken_courses": [], "taken_geneds": []},
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["user_id"] == "ai-user-1"
    assert isinstance(body["schedules"], list)
    assert body["conversation_length"] >= 1


def test_dialog_handles_invalid_json_from_model(ai_client, monkeypatch):
    from scripts import terminal_chat as tc

    def bad_request_json(*_args, **_kwargs):
        return "not-json"

    monkeypatch.setattr(tc, "request_json", bad_request_json)

    resp = ai_client.post(
        "/dialog",
        json={"user_id": "ai-user-2", "message": "cause bad json", "academic": {}},
    )
    assert resp.status_code == 200
    assert "error" in resp.json()


def test_dialog_missing_user_id(ai_client):
    resp = ai_client.post("/dialog", json={"message": "hi", "academic": {}})
    assert resp.status_code == 200
    assert resp.json()["error"]


def test_reset_clears_user_state(ai_client):
    ai_client.post("/dialog", json={"user_id": "ai-user-3", "message": "hello", "academic": {}})
    reset = ai_client.post("/reset", json={"user_id": "ai-user-3"})
    assert reset.status_code == 200
    assert reset.json()["message"].startswith("Session reset")
