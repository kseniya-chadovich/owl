# ===== File paths =====
CATALOG_FILE = "data/course_catalog.json"
PLAN_FILE = "data/plan.json"

# ===== Weights =====
PLAN_WEIGHT        = 1500
UNSAT_GENED_WEIGHT = 400
GENED_WEIGHT       = 400
DAY_PREF_WEIGHT    = 300
DAY_NO_PENALTY     = -300
LUNCH_PENALTY      = -100
NO_MORN_PENALTY    = -200
NO_EVEN_PENALTY    = -200
MODE_MATCH_REWARD  = 200
ONE_CREDIT_PENALTY = -350
NORMAL_ELEC_REWARD = 350
AVOID_PROF_PENALTY = -250
CREDITS_NUDGE      = 1

# ===== Solver settings =====
TIME_LIMIT_SEC     = 15
