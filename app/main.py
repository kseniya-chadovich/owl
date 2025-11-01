# app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from scripts.terminal_chat import build_client, handle_request, SCHEMA_DESCRIPTION

# ← 新增這兩行
from app.supabase_client import get_supabase
from app.models.student import StudentRegistration

app = FastAPI(title="Scheduling Assistant API")

# CORS (keep yours)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = build_client()
MODEL_NAME = "models/gemini-2.5-flash-lite"

# Stores per-user conversation + academic info (in memory)
user_state = {}

# ← new: create supabase client
supabase = get_supabase()

@app.get("/")
def root():
    return {"message": "Scheduling Assistant API is running!"}

# -------------------------
# 1) NEW: Register student
# -------------------------
@app.post("/register-student")
async def register_student(payload: StudentRegistration):
    """
    Save personal info and academic info into Supabase.
    This will upsert (insert or update) both tables.
    """
    personal = payload.personal
    academic = payload.academic

    # upsert personal
    personal_data = {
        "user_id": personal.user_id,
        "full_name": personal.full_name,
        "age": personal.age,
        "is_international": personal.is_international,
    }
    personal_res = supabase.table("students_personal").upsert(personal_data).execute()
    if personal_res.get("status_code", 200) >= 400:
        # simple error message
        raise HTTPException(status_code=500, detail="Failed to save personal info")

    # upsert academic
    academic_data = {
        "user_id": academic.user_id,
        "current_semester": academic.current_semester,
        "taken_courses": academic.taken_courses,
        "taken_geneds": academic.taken_geneds,
    }
    academic_res = supabase.table("students_academic").upsert(academic_data).execute()
    if academic_res.get("status_code", 200) >= 400:
        raise HTTPException(status_code=500, detail="Failed to save academic info")

    return {
        "message": "Student data saved.",
        "user_id": personal.user_id,
    }

# -------------------------
# 2) NEW: Get student info (for scheduler)
# -------------------------
@app.get("/students/{user_id}")
def get_student(user_id: str):
    """
    Return combined personal + academic data.
    Frontend / scheduler can call this to get data.
    """
    # personal
    personal_res = (
        supabase.table("students_personal")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    personal_data = None
    if personal_res.data:
        personal_data = personal_res.data[0]

    # academic
    academic_res = (
        supabase.table("students_academic")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    academic_data = None
    if academic_res.data:
        academic_data = academic_res.data[0]

    if not personal_data and not academic_data:
        raise HTTPException(status_code=404, detail="Student not found")

    # format for scheduler (important!)
    scheduler_payload = {
        "user_id": user_id,
        "current_semester": academic_data.get("current_semester") if academic_data else None,
        "taken_courses": academic_data.get("taken_courses") if academic_data else [],
        "taken_geneds": academic_data.get("taken_geneds") if academic_data else [],
        # you can pass international flag too
        "is_international": personal_data.get("is_international") if personal_data else False,
    }

    return {
        "personal": personal_data,
        "academic": academic_data,
        "scheduler_input": scheduler_payload,
    }

# -------------------------
# 你原本的 /dialog 和 /reset
# -------------------------
@app.post("/dialog")
async def dialog(request: Request):
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
    data = await request.json()
    user_id = data.get("user_id")

    if not user_id:
        return {"error": "Missing user_id."}

    if user_id in user_state:
        del user_state[user_id]

    return {"message": f"All data reset for user '{user_id}'. New session ready."}
