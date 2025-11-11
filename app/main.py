from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from scripts.terminal_chat import build_client, handle_request, SCHEMA_DESCRIPTION
from app.supabase_client import get_supabase

app = FastAPI(title="Scheduling Assistant API")

# Allow frontend access (adjust origins later if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI scheduler client (existing)
client = build_client()
MODEL_NAME = "models/gemini-2.5-flash-lite"

# In-memory conversation state (existing)
user_state: Dict[str, Dict[str, Any]] = {}


# ---------- Models ----------

class PersonalInfo(BaseModel):
    user_id: str
    full_name: str
    age: int
    is_international: bool


class AcademicInfo(BaseModel):
    user_id: str
    current_semester: str
    taken_courses: List[str]
    taken_geneds: List[str]


class RegisterStudentPayload(BaseModel):
    personal: PersonalInfo
    academic: AcademicInfo


class SchedulePayload(BaseModel):
    user_id: str
    schedule: Dict[str, Any]


# ---------- Health check ----------

@app.get("/")
def root():
    return {"message": "Scheduling Assistant API is running!"}


# ---------- Existing: dialog with LLM ----------

@app.post("/dialog")
async def dialog(request: Request):
    """
    Main dialog endpoint.
    Uses in-memory state + provided student_data.
    """
    data = await request.json()
    user_id = data.get("user_id", "default")
    message = data.get("message", "").strip()
    new_student_data = data.get("student_data", {})
    num_schedules = data.get("num_schedules", 3)
    temperature = data.get("temperature", 0.2)

    if not message:
        return {"error": "Missing 'message' field in request."}

    academic_fields = {"taken_courses", "taken_geneds", "current_semester"}
    academic_data = {k: v for k, v in new_student_data.items() if k in academic_fields}

    if user_id not in user_state:
        user_state[user_id] = {
            "conversation": [SCHEMA_DESCRIPTION],
            "student_data": academic_data,
        }
    else:
        if academic_data:
            user_state[user_id]["student_data"].update(academic_data)

    student_data = user_state[user_id]["student_data"]
    conversation = user_state[user_id]["conversation"]

    try:
        result = handle_request(
            client=client,
            model_name=MODEL_NAME,
            message=message,
            student_data=student_data,
            conversation_history=conversation,
            num_schedules=num_schedules,
            temperature=temperature,
        )
    except Exception as e:
        return {"error": str(e)}

    user_state[user_id]["conversation"] = result["conversation"]

    return {
        "user_id": user_id,
        "payload": result["payload"],
        "schedules": result["schedules"],
        "conversation_length": len(result["conversation"]),
    }


@app.post("/reset")
async def reset_user(request: Request):
    """
    Reset in-memory dialog state for one user.
    """
    data = await request.json()
    user_id = data.get("user_id")

    if not user_id:
        return {"error": "Missing user_id."}

    if user_id in user_state:
        del user_state[user_id]

    return {"message": f"All data reset for user '{user_id}'."}


# ---------- New: registration / CRUD for student info ----------

@app.post("/register-student")
async def register_student(payload: RegisterStudentPayload):
    """
    Save or update student personal + academic info in Supabase.
    Used on registration.
    """
    supabase = get_supabase()

    personal_data = payload.personal.model_dump()
    academic_data = payload.academic.model_dump()

    # Upsert personal info
    supabase.table("student_personal").upsert(
        personal_data,
        on_conflict="user_id",
    ).execute()

    # Upsert academic info
    supabase.table("student_academic").upsert(
        academic_data,
        on_conflict="user_id",
    ).execute()

    return {"message": "Student data saved.", "user_id": payload.personal.user_id}


@app.get("/students/{user_id}")
async def get_student(user_id: str):
    """
    Get merged student info for scheduler/frontend.
    Returns:
      - personal
      - academic
      - scheduler_input: flattened object ready for the scheduler
    """
    supabase = get_supabase()

    # personal
    personal_res = (
        supabase.table("student_personal")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    personal = personal_res.data[0] if personal_res.data else None

    # academic
    academic_res = (
        supabase.table("student_academic")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    academic = academic_res.data[0] if academic_res.data else None

    if not personal and not academic:
        raise HTTPException(status_code=404, detail="Student not found")

    scheduler_input = {
        "user_id": user_id,
        "current_semester": (academic or {}).get("current_semester"),
        "taken_courses": (academic or {}).get("taken_courses", []),
        "taken_geneds": (academic or {}).get("taken_geneds", []),
        "is_international": (personal or {}).get("is_international"),
    }

    return {
        "personal": personal,
        "academic": academic,
        "scheduler_input": scheduler_input,
    }


@app.get("/students/personal/{user_id}")
async def get_student_personal(user_id: str):
    """
    Get only personal info.
    """
    supabase = get_supabase()
    res = (
        supabase.table("student_personal")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=404, detail="Student personal info not found")
    return res.data[0]


@app.get("/students/academic/{user_id}")
async def get_student_academic(user_id: str):
    """
    Get only academic info.
    """
    supabase = get_supabase()
    res = (
        supabase.table("student_academic")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=404, detail="Student academic info not found")
    return res.data[0]


@app.post("/students/schedules")
async def save_schedule(payload: SchedulePayload):
    """
    Save or update the final schedule for a student.
    Called after the user selects a schedule.
    """
    supabase = get_supabase()

    data = {
        "user_id": payload.user_id,
        "schedule": payload.schedule,
    }

    supabase.table("student_schedules").upsert(
        data,
        on_conflict="user_id",
    ).execute()

    return {"message": "Schedule saved.", "user_id": payload.user_id}


@app.get("/students/schedules/{user_id}")
async def get_schedule(user_id: str):
    """
    Get saved schedule for a student.
    """
    supabase = get_supabase()
    res = (
        supabase.table("student_schedules")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return res.data[0]


@app.delete("/students/{user_id}")
async def delete_student(user_id: str):
    """
    Delete a student and all related info (personal, academic, schedules).
    """
    supabase = get_supabase()

    supabase.table("student_schedules").delete().eq("user_id", user_id).execute()
    supabase.table("student_academic").delete().eq("user_id", user_id).execute()
    supabase.table("student_personal").delete().eq("user_id", user_id).execute()

    return {"message": f"User {user_id} and related info deleted."}
