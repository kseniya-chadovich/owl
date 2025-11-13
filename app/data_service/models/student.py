# app/models/student.py
from typing import List, Optional
from pydantic import BaseModel

class PersonalInfo(BaseModel):
    user_id: str          # example: "s1234567" or email
    full_name: str
    age: Optional[int] = None
    is_international: bool = False

class AcademicInfo(BaseModel):
    user_id: str
    current_semester: Optional[str] = None   # example: "Fall 2025"
    taken_courses: List[str] = []            # example: ["CIS1001", "ENG1002"]
    taken_geneds: List[str] = []             # example: ["Humanities", "Math"]

class StudentRegistration(BaseModel):
    personal: PersonalInfo
    academic: AcademicInfo
