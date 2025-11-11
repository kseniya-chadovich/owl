import requests

BASE_URL = "http://localhost:8000"


def register_student_example():
    """Example: register or update one student's personal + academic info."""
    payload = {
        "personal": {
            "user_id": "s1234567",
            "full_name": "Test Student",
            "age": 20,
            "is_international": True,
        },
        "academic": {
            "user_id": "s1234567",
            "current_semester": "Fall 2025",
            "taken_courses": ["CIS1001", "ENG1002"],
            "taken_geneds": ["Humanities", "Math"],
        },
    }

    r = requests.post(f"{BASE_URL}/register-student", json=payload)
    print("POST /register-student:", r.status_code, r.json())


def get_student_example():
    """Example: fetch merged data for scheduler/frontend."""
    user_id = "s1234567"
    r = requests.get(f"{BASE_URL}/students/{user_id}")
    print(f"GET /students/{user_id}:", r.status_code, r.json())


def get_personal_only_example():
    """Example: fetch only personal info."""
    user_id = "s1234567"
    r = requests.get(f"{BASE_URL}/students/personal/{user_id}")
    print(f"GET /students/personal/{user_id}:", r.status_code, r.json())


def get_academic_only_example():
    """Example: fetch only academic info."""
    user_id = "s1234567"
    r = requests.get(f"{BASE_URL}/students/academic/{user_id}")
    print(f"GET /students/academic/{user_id}:", r.status_code, r.json())


def save_schedule_example():
    """Example: save final schedule for a student."""
    user_id = "s1234567"
    schedule = {
        "semester": "Fall 2025",
        "sections": [
            {"course": "CIS1001", "day": "Mon", "time": "09:00-10:15"},
            {"course": "ENG1002", "day": "Wed", "time": "13:00-14:15"},
        ],
    }
    payload = {"user_id": user_id, "schedule": schedule}
    r = requests.post(f"{BASE_URL}/students/schedules", json=payload)
    print("POST /students/schedules:", r.status_code, r.json())


def get_schedule_example():
    """Example: fetch saved schedule for a student."""
    user_id = "s1234567"
    r = requests.get(f"{BASE_URL}/students/schedules/{user_id}")
    print(f"GET /students/schedules/{user_id}:", r.status_code, r.json())


def delete_student_example():
    """Example: delete student and all related info."""
    user_id = "s1234567"
    r = requests.delete(f"{BASE_URL}/students/{user_id}")
    print(f"DELETE /students/{user_id}:", r.status_code, r.json())


if __name__ == "__main__":
    # Run these one by one as needed.
    register_student_example()
    get_student_example()
    get_personal_only_example()
    get_academic_only_example()
    save_schedule_example()
    get_schedule_example()
    # delete_student_example()  # uncomment if you want to clean up test data
