"""

Example script showing exactly what kind of JSON the frontend
should send to the backend API, and what response to expect.

It simulates:
  1. Starting a new semester session (sending academic data) - this is basically starting a new dialog, first exchange of information type of POST
  2. Updating preferences mid-session (same user) - this is in case users adds smth like "actually nevermind, Tuesday do't work for me either" aka 
  continuing current dialog (+ context awarness)
  3. Resetting the session (for next semester) - once the user is satisfied with the schedule, we want to get rid of the current dialog, at least
  on the backend. On the frontend, we can keep it or not keep it, doesn't matter
"""

import requests
import json

BASE_URL = "https://scheduling-assistant-zl2c.onrender.com"

# 1️⃣ Example: starting a new session (includes academic data)
start_payload = {
    "user_id": "1",
    "message": (
        "No Tuesday classes, prefer online and gen eds GG or GY. "
        "I also want no morning classes and a lunch break. NO prof Karam :)"
    ),
    "student_data": {
        "taken_courses": ["MATH 1021", "CIS 1041"],
        "taken_geneds": ["GB"],
        "current_semester": 2
    }
}

# 2️⃣ Example: updating preferences mid-session (no student_data)
update_payload = {
    "user_id": "1",
    "message": "Actually, I can take morning classes now, but no Friday classes please."
}

# 3️⃣ Example: resetting the session completely
reset_payload = {"user_id": "1"}


def post_json(endpoint: str, payload: dict):
    """Helper function to send POST requests and print results."""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n➡️ POST {url}")
    print("Request JSON:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        print("\n✅ Response JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return data
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return None


def main():
    print("=== 1️⃣ Start New Semester Session ===")
    post_json("/dialog", start_payload)

    print("\n=== 2️⃣ Update Preferences During Same Session ===")
    post_json("/dialog", update_payload)

    print("\n=== 3️⃣ Reset After Finalizing Schedule ===")
    post_json("/reset", reset_payload)


if __name__ == "__main__":
    main()
