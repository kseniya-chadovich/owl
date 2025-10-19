from typing import List, Optional, Literal, Union, Set
from pydantic import BaseModel, conint, field_validator

class CatalogItem(BaseModel):
    course: str                 # e.g., "CIS 1051 (802)"
    section: str                # e.g., "802"
    instructor: str
    day_time: str               # e.g., "MWF 10:00-11:20" or "Asynchronous"
    credits: int
    mode: Literal["online", "offline"]
    category: Literal["major", "elective", "gened"]
    gened_type: Optional[str] = None
    # Prerequisites support AND/OR:
    # ["ACCT 1001"] -> must have ACCT 1001 (AND)
    # [["CIS 1051", "CIS 1057"], "MATH 1041"]
    #   -> (CIS1051 OR CIS1057) AND MATH1041
    prerequisites: List[Union[str, List[str]]] = []
    semester_recommended: Optional[str] = None

class ScheduleRequest(BaseModel):
    num_schedules: conint(ge=1, le=20) = 3
    desired_credits_min: conint(ge=0) = 12
    desired_credits_max: conint(ge=0) = 18
    taken_courses: List[str] = []
    include_categories: Optional[Set[Literal["major", "elective", "gened"]]] = None
    must_include: List[str] = []            # course codes without section, e.g., "CIS 1068"
    must_exclude: List[str] = []            # course codes without section
    prefer_modes: Optional[List[Literal["online", "offline"]]] = None
    days_off: List[Literal["M","T","W","Th","F","Sa","Su"]] = []
    time_window_start: Optional[str] = None # "HH:MM"
    time_window_end: Optional[str] = None   # "HH:MM"
    one_section_per_course: bool = True     # at most one section per course base code

    @field_validator("time_window_start", "time_window_end")
    @classmethod
    def _hhmm(cls, v: Optional[str]) -> Optional[str]:
        # Validate HH:MM format (24h)
        if v is None:
            return v
        try:
            h, m = v.split(":")
            assert 0 <= int(h) <= 23 and 0 <= int(m) <= 59
        except Exception as e:
            raise ValueError("time_window_* must be HH:MM") from e
        return v

class ScheduledSection(BaseModel):
    course: str
    section: str
    instructor: str
    day_time: str
    credits: int
    mode: Literal["online", "offline"]

class Schedule(BaseModel):
    total_credits: int
    sections: List[ScheduledSection]
    violations: List[str] = []  # Reasons when no valid schedules are found

class GenerateResponse(BaseModel):
    schedules: List[Schedule]
