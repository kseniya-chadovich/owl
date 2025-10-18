# app/main.py
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ---------- file paths ----------
CATALOG_FILE = os.getenv("CATALOG_FILE", "data/course_catalog.json")
PLAN_FILE    = os.getenv("PLAN_FILE",    "data/plan.json")
PROGRESS_FILE= os.getenv("PROGRESS_FILE","data/student_progress.json")

# ---------- import your generator ----------
try:
    from scheduler.generator import generate_schedules
except Exception:
    from generator import generate_schedules

app = FastAPI(title="Scheduling Assistant Backend", version="0.1.0")