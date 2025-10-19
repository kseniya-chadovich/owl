import re
from datetime import time
from typing import List, Tuple, Union, Set, Dict
from .models import CatalogItem

def normalize_course(c: str) -> str:
    """Normalize course code by trimming and uppercasing, collapsing spaces."""
    return re.sub(r"\s+", " ", c.strip()).upper()

def base_code(course_with_section: str) -> str:
    """Extract base course code without the (section) suffix."""
    return normalize_course(re.split(r"\s*\(", course_with_section)[0])

def hhmm_to_time(s: str) -> time:
    """Convert 'HH:MM' to datetime.time."""
    h, m = map(int, s.split(":"))
    return time(hour=h, minute=m)

def expand_meetings(day_time: str) -> List[Tuple[str, time, time]]:
    """
    Parse meeting string into (day, start, end) tuples.

    Example:
      "MWF 10:00-11:20 & F 20:00-22:00" ->
        [("M",10:00,11:20), ("W",10:00,11:20), ("F",10:00,11:20), ("F",20:00,22:00)]
      "Asynchronous" -> []
    """
    if not day_time or "asynchronous" in day_time.lower():
        return []

    parts = [p.strip() for p in day_time.split("&")]
    meetings: List[Tuple[str, time, time]] = []
    for part in parts:
        m = re.search(r"(.+?)\s+(\d{1,2}:\d{2})-(\d{1,2}:\d{2})", part)
        if not m:
            continue
        days_str, start_s, end_s = m.groups()

        # Tokenize days; support Th, Sa, Su, and single-letter M/T/W/F.
        days: List[str] = []
        i = 0
        while i < len(days_str):
            if days_str.startswith("Th", i):
                days.append("Th"); i += 2
            elif days_str.startswith("Su", i):
                days.append("Su"); i += 2
            elif days_str.startswith("Sa", i):
                days.append("Sa"); i += 2
            else:
                d = days_str[i]
                if d in {"M","T","W","F"}:
                    days.append(d); i += 1
                else:
                    i += 1

        start_t, end_t = hhmm_to_time(start_s), hhmm_to_time(end_s)
        for d in days:
            meetings.append((d, start_t, end_t))
    return meetings

def overlap(a: Tuple[time, time], b: Tuple[time, time]) -> bool:
    """Check if two [start, end) intervals overlap."""
    a1, a2 = a; b1, b2 = b
    return (a1 < b2) and (b1 < a2)

def check_conflict(current: Dict[str, List[Tuple[time, time]]],
                   candidate: CatalogItem,
                   days_off: Set[str],
                   window_start: Union[None, time],
                   window_end: Union[None, time]) -> bool:
    """
    Return True if any conflict exists:
      - day is in days_off
      - time before window_start or after window_end
      - overlaps with existing meetings in 'current'
    """
    for d, s, e in expand_meetings(candidate.day_time):
        if d in days_off:
            return True
        if window_start and s < window_start:
            return True
        if window_end and e > window_end:
            return True
        for (s0, e0) in current.get(d, []):
            if overlap((s, e), (s0, e0)):
                return True
    return False

def add_to_timetable(current: Dict[str, List[Tuple[time, time]]], item: CatalogItem) -> None:
    """Append candidate meetings into the day->intervals mapping."""
    for d, s, e in expand_meetings(item.day_time):
        current.setdefault(d, []).append((s, e))

def prereq_satisfied(item: CatalogItem, taken) -> bool:
    """
    Check if prerequisites are satisfied by 'taken' (a set of normalized course codes).
    Supports OR-groups (lists) and single-course requirements (strings).
    """
    if not item.prerequisites:
        return True
    for group in item.prerequisites:
        if isinstance(group, list):
            if not any(normalize_course(g) in taken for g in group):
                return False
        else:
            if normalize_course(group) not in taken:
                return False
    return True
