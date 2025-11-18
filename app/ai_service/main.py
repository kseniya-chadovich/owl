# app/ai_service/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from scripts.terminal_chat import build_client, handle_request, SCHEMA_DESCRIPTION

app = FastAPI(title="Scheduling Assistant AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = build_client()
MODEL_NAME = "models/gemini-2.5-flash-lite"

# In-memory storage (per user)
user_state: Dict[str, Dict[str, Any]] = {}

@app.get("/")
def root():
    return {"message": "AI Parser & Scheduler is running!"}

@app.post("/dialog")
async def dialog(request: Request):
    data = await request.json()

    user_id = data.get("user_id")
    message = data.get("message", "").strip()
    incoming_academic = data.get("academic") or {}

    if not user_id:
        return {"error": "Missing user_id."}
    if not message:
        return {"error": "Missing message."}

    # Initialize state if not present
    if user_id not in user_state:
        user_state[user_id] = {
            "conversation": [SCHEMA_DESCRIPTION],
            "student_data": incoming_academic,
        }
    else:
        # Update academic info every request
        user_state[user_id]["student_data"] = incoming_academic

    state = user_state[user_id]

    try:
        result = handle_request(
            client=client,
            model_name=MODEL_NAME,
            message=message,
            student_data=state["student_data"],       # <-- academic included
            conversation_history=state["conversation"],
            num_schedules=3,
            temperature=0.2,
        )
    except Exception as e:
        return {"error": str(e)}

    # Update conversation history
    state["conversation"] = result["conversation"]

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
        return {"error": "Missing user_id"}
    user_state.pop(user_id, None)
    return {"message": f"Session reset for {user_id}"}
