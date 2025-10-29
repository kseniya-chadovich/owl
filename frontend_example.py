"""
frontend_example.py
-------------------

Example script for frontend developers showing how to communicate
with the Scheduling Assistant backend hosted on Render.

Endpoints:
  - POST /dialog  → Send user messages and academic info
  - POST /reset   → Clear session data when user finalizes schedule

To run this example:
    pip install requests
    python frontend_example.py
"""

import requests
import json

# Replace this with your actual Render deployment URL
BASE_URL = "https://scheduler-backend.onrender.com"

# ---------- Example Data ----------

# 1️⃣ Academic data (fixed for one semester/session)
academic_info = {
    "taken_courses": ["MATH 1021", "CIS 1051"],
    "taken_geneds": ["GB"],
    "min_credits": 12,
    "max_credits": 18,
    "current_semester": 2
}

# 2️⃣ Initial user message (natural language)
initial_message = "No Tuesday classes, prefer online please"

# 3️⃣ Follow-up user message during the same session
update_message = "Actually, I’m okay with mornings now but no Friday classes."

# 4️⃣ Unique ID for this user
user_id = "kseniya123"

# ---------- Helper Functions ----------

def send_dialog(message, student_data=None):
    """Send a message to the /dialog endpoint."""
    url = f"{BASE_URL}/dialog"
    payload = {
        "user_id": user_id,
        "message": message,
    }
    if student_data:
        payload["student_data"] = student_data

    print(f"\n➡️ Sending POST to {url}")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        print("\n✅ Response received:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")


def reset_session():
    """Trigger a reset for the user via /reset endpoint."""
    url = f"{BASE_URL}/reset"
    payload = {"user_id": user_id}

    print(f"\n🧹 Sending POST to {url} to reset user session")
    print(json.dumps(payload, indent=2))

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        print("\n✅ Reset successful:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Reset failed: {e}")

# ---------- Example Workflow ----------

def main():
    print("=== 1️⃣ Starting New Session ===")
    send_dialog(initial_message, student_data=academic_info)

    print("\n=== 2️⃣ Updating Preferences (Same Session) ===")
    send_dialog(update_message)

    print("\n=== 3️⃣ Resetting Session (End of Semester) ===")
    reset_session()


if __name__ == "__main__":
    main()
