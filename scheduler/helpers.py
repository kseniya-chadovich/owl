import re

def extract_course_code(course_str):
    base = course_str.split("(")[0].strip()
    m = re.search(r'([A-Za-z]+)\s*(\d{3,4})', base)
    return f"{m.group(1).upper()} {m.group(2)}" if m else base

def parse_time_to_min(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m

def expand_day_tokens(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "T" and i + 1 < len(s) and s[i+1] == "h":
            out.append("Th"); i += 2
        else:
            out.append(s[i]); i += 1
    return out

def parse_daytime_slots(daytime_str):
    slots = []
    if not daytime_str or not isinstance(daytime_str, str):
        return slots
    for chunk in daytime_str.split("&"):
        chunk = chunk.strip()
        if not chunk or " " not in chunk:
            continue
        days_part, times_part = chunk.split(None, 1)
        m = re.match(r'(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})', times_part.strip())
        if not m:
            continue
        start_min, end_min = parse_time_to_min(m.group(1)), parse_time_to_min(m.group(2))
        for d in expand_day_tokens(days_part):
            slots.append((d, start_min, end_min))
    return slots

def slots_overlap(a, b):
    return any(d1 == d2 and not (e1 <= s2 or e2 <= s1)
               for d1, s1, e1 in a for d2, s2, e2 in b)

def prereqs_satisfied(section, taken_courses):
    prereqs = section.get("prerequisites", [])
    if not prereqs: return True
    for item in prereqs:
        if isinstance(item, list):
            if not any(alt in taken_courses for alt in item):
                return False
        elif item not in taken_courses:
            return False
    return True

def lunch_conflict(slots):
    return any(s < 13*60 and e > 12*60 for _, s, e in slots)

def class_starts_before(slots, minute):
    return any(s < minute for _, s, _ in slots)

def class_ends_after(slots, minute):
    return any(e > minute for _, _, e in slots)

def days_set(slots):
    return {d for d,_,_ in slots}

def is_cis_3000_plus(code):
    m = re.match(r"CIS\s*(\d+)", code)
    return m and int(m.group(1)) >= 3000
