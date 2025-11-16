from typing import List, Optional
from pydantic import BaseModel


class PersonalInfo(BaseModel):
    user_id: str                  # Supabase UUID
    full_name: str
    age: Optional[int] = None
    is_international: bool = False


class AcademicInfo(BaseModel):
    user_id: str
    current_semester: int         # <-- INTEGER
    taken_courses: List[str] = []
    taken_geneds: List[str] = []


class StudentRegistration(BaseModel):
    personal: PersonalInfo
    academic: AcademicInfo
