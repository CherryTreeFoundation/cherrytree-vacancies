"""
CherryTree Foundation - Career Map Vacancy Fetcher
Runs every 8 days via GitHub Actions.
Calls Reed API for each role, saves counts to vacancies.json.
"""

import requests
import json
import os
from datetime import datetime

REED_API_KEY = os.environ["REED_API_KEY"]
BASE_URL = "https://www.reed.co.uk/api/1.0/search"

ROLES = [
    ("it_support",   "IT support helpdesk"),
    ("it_tech",      "IT technician"),
    ("web_dev",      "web developer"),
    ("qa_tester",    "QA tester software testing"),
    ("jr_data",      "data analyst"),
    ("software_dev", "software developer"),
    ("cyber",        "cyber security analyst"),
    ("cloud_eng",    "cloud engineer AWS Azure"),
    ("recept",       "receptionist"),
    ("cust_svc",     "customer service adviser"),
    ("admin_a",      "admin assistant"),
    ("hr_asst",      "HR assistant"),
    ("off_coord",    "office coordinator"),
    ("hr_adv",       "HR advisor"),
    ("ops_off",      "operations manager"),
    ("biz_dir",      "business director"),
    ("care_train",   "care assistant trainee entry level"),
    ("home_care",    "home care worker"),
    ("care_supp",    "care support worker"),
    ("health_a",     "healthcare assistant"),
    ("mh_supp",      "mental health support worker"),
    ("snr_care",     "senior care worker"),
    ("dep_care",     "deputy care manager"),
    ("care_dir",     "care home manager director"),
    ("class_sup",    "classroom support assistant"),
    ("teach_a",      "teaching assistant"),
    ("learn_m",      "learning mentor"),
    ("youth_w",      "youth worker"),
    ("tutor",        "tutor"),
    ("past_lead",    "pastoral lead"),
    ("prog_lead",    "programme lead education"),
    ("head_teach",   "head teacher"),
    ("con_train",    "construction trainee labourer"),
    ("labourer",     "labourer construction"),
    ("banksman",     "banksman slinger"),
    ("cscs_op",      "CSCS operative construction"),
    ("site_adm",     "site administrator construction"),
    ("asst_sm",      "assistant site manager"),
    ("site_mgr",     "site manager construction"),
    ("proj_mgr",     "project manager construction"),
    ("wh_train",     "warehouse operative entry level"),
    ("wh_op",        "warehouse operative"),
    ("picker",       "picker packer warehouse"),
    ("delivery",     "delivery driver"),
    ("dispatch",     "dispatch operative"),
    ("trans_plan",   "transport planner"),
    ("wh_lead",      "warehouse team leader"),
    ("log_coord",    "logistics coordinator"),
    ("wh_mgr",       "warehouse manager"),
    ("appren_eng",   "engineering apprentice"),
    ("jr_tech",      "junior technician engineering"),
    ("grad_eng",     "graduate engineer"),
    ("engineer",     "engineer"),
    ("snr_eng",      "senior engineer"),
    ("princ_eng",    "principal engineer"),
    ("chief_eng",    "chief engineer"),
    ("eng_dir",      "engineering director"),
    ("sec_stew",     "concierge"),
    ("sec_off",      "door supervisor"),
    ("corp_sec",     "security officer"),
    ("sec_lead",     "security team leader"),
    ("sec_ops",      "security operations manager"),
    ("head_sec",     "head of security"),
    ("sec_consult",  "security consultant"),
]

def fetch_count(keywords):
    try:
        r = requests.get(
            BASE_URL,
            params={
                "keywords": keywords,
                "location": "london",
                "distancefromlocation": 10,
            },
            auth=(REED_API_KEY, ""),
            timeout=15,
        )
        if r.status_code == 200:
            return r.json().get("totalResults", 0)
        else:
            print(f"  HTTP {r.status_code} for '{keywords}'")
            return None
    except Exception as e:
        print(f"  Error for '{keywords}': {e}")
        return None

results = {}
updated = datetime.utcnow().strftime("%-d %B %Y")
print(f"Fetching vacancy counts - {updated}\n")

for role_id, keywords in ROLES:
    count = fetch_count(keywords)
    if count is not None:
        results[role_id] = {"count": count, "asOf": updated}
        print(f"  {role_id}: {count}")
    else:
        print(f"  {role_id}: FAILED")

with open("vacancies.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nDone. {len(results)} roles written to vacancies.json.")
