# Enter "python -m scripts.terminal_chat" in the terminal to test
# Terminal interface for converting natural language scheduling preferences into JSON

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import google.genai as genai
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

load_dotenv(dotenv_path=ROOT_DIR / ".env")

from scheduler.generator import generate_schedules

SCHEMA_DESCRIPTION = """
You are an assistant that converts student scheduling preferences into a strict JSON object.
Return ONLY minified JSON with these exact keys:
{
  "gened_preference": list of two-letter gen-ed codes like "GA".
  "min_credits": int,
  "max_credits": int,
  "current_semester": int,
  "preferred_days": list of strings using ONLY individual weekday tokens "M","T","W","Th","F" (e.g. ["M","W","F"], ["T","Th"]),
  "no_days": list of strings using ONLY individual weekday tokens "M","T","W","Th","F" (same format as preferred_days),
  "lunch_break": boolean,
  "no_mornings": boolean,
  "no_evenings": boolean,
  "prefer_mode": "online" or "offline" or null,
  "avoid_professors": list of strings,
}
If the user does not mention a field, infer a reasonable default or set null/empty list.
If the user does not specify credits, use min_credits=12 and max_credits=18.
Treat abbreviations like "TTh" as representing both Tuesday and Thursday by converting them into the two separate tokens "T" and "Th".
Before producing the JSON, build an internal CONTEXT summary that merges all prior user messages in this conversation. Always honor the most recent instruction when there is a conflict—for example, if the user first says "no Monday classes" but later says "Monday is fine", remove "M" from no_days (and do not add it back unless they ask again). If the user does not mention a field in the latest message, keep the previously stored value (e.g., after "no Fridays" then "I want an art class", the output must still include "F" in no_days). Apply this recency rule for every field.
Never include comments or extra text.
When the user mentions general education areas in natural language, map them to these codes:
  Arts -> GA
  Analytical Reading & Writing -> GW
  Intellectual Heritage I, IH1 -> GY
  Intellectual Heritage II, IH2 -> GZ
  If the user asks for the whole Intellectual Heritage sequence or both courses together -> include both GY and GZ
  Quantitative Literacy -> GQ
  Human Behavior -> GB
  Diversity & Race -> GD
  Global/World Society -> GG
  Science & Technology -> GS
  U.S. Society -> GU
""".strip()

DEFAULT_OUTPUT = {
    "gened_preference": [],
    "min_credits": 12,
    "max_credits": 18,
    "current_semester": 1,
    "preferred_days": [],
    "no_days": [],
    "lunch_break": False,
    "no_mornings": False,
    "no_evenings": False,
    "prefer_mode": None,
    "avoid_professors": [],
}

DEFAULT_NUM_SCHEDULES = 3


def load_api_key() -> str:
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError(
            "GOOGLE_API_KEY not set. Create a .env file based on .env.example or set the environment variable."
        )
    return key


def build_client() -> genai.Client:
    api_key = load_api_key()
    return genai.Client(api_key=api_key)


from google.genai import types

# Call the Gemini Model with accumulated conversation history
def request_json(
    client: genai.Client,
    model_name: str,
    conversation_history: List[str],
    temperature: float,
) -> str:
    response = client.models.generate_content(
        model=model_name,
        contents=conversation_history,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=1024,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini response is empty.")
    return text


# Extracts and parses the first JSON object found in the response text
def extract_json(raw_text: str) -> Dict[str, Any]:
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Could not locate JSON object in the response.")
    json_str = raw_text[start : end + 1]
    data = json.loads(json_str)
    return data

# Normalizes the parsed JSON into a validated payload with defaults and proper types
def normalize_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized = DEFAULT_OUTPUT.copy()
    normalized.update(data)

    normalized["gened_preference"] = _ensure_str_list(normalized.get("gened_preference", []))

    raw_min = normalized.get("min_credits")
    parsed_min = _parse_optional_int(raw_min)
    if parsed_min is None or parsed_min <= 0:
        min_credits = DEFAULT_OUTPUT["min_credits"]
    else:
        min_credits = parsed_min

    raw_max = normalized.get("max_credits")
    parsed_max = _parse_optional_int(raw_max)
    if parsed_max is None or parsed_max < min_credits:
        max_credits = DEFAULT_OUTPUT["max_credits"]
        if max_credits < min_credits:
            max_credits = min_credits
    else:
        max_credits = parsed_max

    normalized["min_credits"] = min_credits
    normalized["max_credits"] = max_credits

    normalized["current_semester"] = _parse_int(
        normalized.get("current_semester"),
        DEFAULT_OUTPUT["current_semester"],
    )

    normalized["preferred_days"] = _ensure_str_list(normalized.get("preferred_days", []))
    normalized["no_days"] = _ensure_str_list(normalized.get("no_days", []))

    normalized["lunch_break"] = bool(normalized.get("lunch_break", False))
    normalized["no_mornings"] = bool(normalized.get("no_mornings", False))
    normalized["no_evenings"] = bool(normalized.get("no_evenings", False))

    prefer_mode = normalized.get("prefer_mode")
    if prefer_mode is not None:
        prefer_mode = str(prefer_mode).lower()
        if prefer_mode not in {"online", "offline"}:
            prefer_mode = None
    normalized["prefer_mode"] = prefer_mode

    normalized["avoid_professors"] = _ensure_str_list(normalized.get("avoid_professors", []))

    return normalized


def _ensure_str_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if str(item).strip()]
    return []


def _parse_int(value: Any, default: int) -> int:
    try:
        if value is None:
            raise TypeError
        return int(value)
    except (TypeError, ValueError):
        return int(default)


def _parse_optional_int(value: Any) -> Optional[int]:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def interactive_loop(
    client: genai.Client,
    model_name: str,
    temperature: float,
    num_schedules: int,
) -> None:
    conversation_history: List[str] = [SCHEMA_DESCRIPTION]
    print("Type scheduling requests. Enter 'exit' to stop or 'reset' to clear context.")
    while True:
        try:
            user_text = input("Request> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return
        if user_text.lower() in {"exit", "quit"}:
            print("Bye!")
            return
        if user_text.lower() == "reset":
            conversation_history = [SCHEMA_DESCRIPTION]
            print("Conversation history cleared.")
            continue
        if not user_text:
            continue
        conversation_history.append(f"User: {user_text}")
        try:
            raw_output = request_json(client, model_name, conversation_history, temperature)
            payload = normalize_payload(extract_json(raw_output))
        except Exception as exc:
            conversation_history.pop()
            print(f"Error: {exc}")
            continue
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        show_schedules(payload, num_schedules)


def run_once(
    client: genai.Client,
    model_name: str,
    request_text: str,
    temperature: float,
    num_schedules: int,
) -> None:
    conversation_history: List[str] = [SCHEMA_DESCRIPTION, f"User: {request_text.strip()}"]
    raw_output = request_json(client, model_name, conversation_history, temperature)
    payload = normalize_payload(extract_json(raw_output))
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    show_schedules(payload, num_schedules)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CLI for Gemini-powered schedule preference parsing")
    parser.add_argument("request", nargs="?", help="Single scheduling request to parse")
    parser.add_argument(
        "--model",
        default="models/gemini-2.5-flash-lite",
        help="Gemini model name (default: models/gemini-2.5-flash-lite)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Generation temperature (default: 0.2)",
    )
    parser.add_argument(
        "--num-schedules",
        type=int,
        default=DEFAULT_NUM_SCHEDULES,
        help="Number of schedules to generate after parsing (default: 3)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        client = build_client()
    except Exception as exc:
        print(f"Failed to initialize Gemini client: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.request:
        run_once(client, args.model, args.request, args.temperature, args.num_schedules)
    else:
        interactive_loop(client, args.model, args.temperature, args.num_schedules)


def show_schedules(payload: Dict[str, Any], num_schedules: int) -> None:
    try:
        schedules = generate_schedules_from_payload(payload, num_schedules)
    except Exception as exc:
        print(f"Failed to generate schedules: {exc}")
        return
    if not schedules:
        print("No valid schedules were found for these preferences.")
        return
    print_schedules(schedules)


def generate_schedules_from_payload(payload: Dict[str, Any], num_schedules: int):
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", suffix=".json", delete=False
        ) as tmp:
            json.dump(payload, tmp, ensure_ascii=False)
            tmp_path = tmp.name
        return generate_schedules(tmp_path, num_schedules=num_schedules)
    finally:
        if tmp_path:
            try:
                os.remove(tmp_path)
            except OSError:
                pass


def print_schedules(schedules: List[Dict[str, Any]]) -> None:
    for idx, sched in enumerate(schedules, start=1):
        print(f"\n--- Schedule {idx} ---")
        for course in sched.get("courses", []):
            print(
                f"{course.get('course')} | {course.get('day_time')} | {course.get('credits')}cr | "
                f"{course.get('category')} | gened={course.get('gened_type')} | "
                f"mode={course.get('mode')} | prof={course.get('instructor')}"
            )
        print(f"Total credits: {sched.get('total_credits')}")
        print("Progress report:", sched.get("progress_report"))

def handle_request(
    client: genai.Client,
    model_name: str,
    message: str,
    student_data: Optional[Dict[str, Any]] = None,
    conversation_history: Optional[List[str]] = None,
    num_schedules: int = 3,
    temperature: float = 0.2,
) -> Dict[str, Any]:
    """
    High-level helper for backend API use.
    Keeps original logic, but allows passing student_data and conversation context.
    """
    if conversation_history is None:
        conversation_history = [SCHEMA_DESCRIPTION]
    conversation_history.append(f"User: {message}")

    raw_output = request_json(client, model_name, conversation_history, temperature)
    payload = normalize_payload(extract_json(raw_output))

    if student_data:
        payload = {**payload, **student_data}

    schedules = generate_schedules_from_payload(payload, num_schedules)

    return {
        "payload": payload,
        "schedules": schedules,
        "conversation": conversation_history,
    }


if __name__ == "__main__":
    main()
