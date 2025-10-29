# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from scripts.terminal_chat import build_client, handle_request, SCHEMA_DESCRIPTION

app = FastAPI(title="Scheduling Assistant API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL before deploy
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = build_client()
MODEL_NAME = "models/gemini-2.5-flash-lite"

# Each user gets their own conversation + academic context
user_state = {}

@app.get("/")
def root():
    return {"message": "Scheduling Assistant API is running!"}


@app.post("/dialog")
async def dialog(request: Request):
    """
    Handles dialog and schedule generation.
    Academic data remains constant for a session.
    Personal preferences are updated by the AI model through context.
    """
    data = await request.json()
    user_id = data.get("user_id", "default")
    message = data.get("message", "").strip()
    new_student_data = data.get("student_data", {})
    num_schedules = data.get("num_schedules", 3)
    temperature = data.get("temperature", 0.2)

    if not message:
        return {"error": "Missing 'message' field in request."}

    # If this is a new session (new semester), initialize everything
    if user_id not in user_state:
        user_state[user_id] = {
            "conversation": [SCHEMA_DESCRIPTION],
            "student_data": new_student_data or {}
        }

    # Academic data stays the same for the entire session
    student_data = user_state[user_id]["student_data"]
    if not student_data and new_student_data:
        user_state[user_id]["student_data"] = new_student_data
        student_data = new_student_data

    # Reuse existing conversation (AI context)
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

    # Update conversation context (AI remembers user’s changing preferences)
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
    Fully resets the user's state (conversation + academic data).
    Called from the frontend when the student finalizes a semester schedule.
    """
    data = await request.json()
    user_id = data.get("user_id")

    if not user_id:
        return {"error": "Missing user_id."}

    if user_id in user_state:
        del user_state[user_id]

    return {"message": f"All data reset for user '{user_id}'. A new session can now start."}
