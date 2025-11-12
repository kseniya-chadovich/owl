from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from scripts.terminal_chat import build_client, handle_request, SCHEMA_DESCRIPTION


app = FastAPI(title="Scheduling Assistant AI Service")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini / scheduler client
client = build_client()
MODEL_NAME = "models/gemini-2.5-flash-lite"

# Store user conversation + data in memory
user_state: Dict[str, Dict[str, Any]] = {}


@app.get("/")
def root():
    return {"message": "AI Parser & Scheduler is running!"}


@app.post("/dialog")
async def dialog(request: Request):
    """Main dialog endpoint for Gemini + scheduler"""
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
    """Reset dialog for a user"""
    data = await request.json()
    user_id = data.get("user_id")
    if not user_id:
        return {"error": "Missing user_id."}
    user_state.pop(user_id, None)
    return {"message": f"Session reset for '{user_id}'."}
