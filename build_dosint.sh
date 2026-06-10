#!/bin/bash
echo "[*] Building DOSINT from scratch..."

# Create directory structure
mkdir -p src/dosint/core src/dosint/modules src/dosint/parsers

# 1. Create database.py (Fixing the IndentationError)
cat <<'EOF' > src/dosint/core/database.py
from tinydb import TinyDB, Query
import os

if not os.path.exists('data'): os.makedirs('data')
db = TinyDB('data/main_db.json')
ReportQuery = Query()

def add_report(indicators):
    db.insert(indicators)
    return True

def find_reports(key, value):
    return db.search(ReportQuery[key] == value)
EOF

# 2. Create business.py
cat <<'EOF' > src/dosint/modules/business.py
from datetime import datetime
from dosint.core import collectors, database, reporter

def investigate(domain, explain=False):
    report = reporter.Report(f"Business Investigation for '{domain}'", explain=explain)
    pivots =[]
    local_hits = database.find_reports('domain', domain)
    report.add_section("1. Local DB Check", [(f"Found {len(local_hits)} reports", 'red' if local_hits else 'green')], "LOCAL_DB")
    whois_data = collectors.get_domain_info(domain)
    findings = [(f"Created: {d.get('creation_date')}", 'green') for d in [whois_data] if 'creation_date' in d]
    report.add_section("2. WHOIS", findings or [("WHOIS lookup failed", 'yellow')], "WHOIS")
    vt_report = collectors.get_virustotal_report(domain)
    hits = vt_report.get('malicious', 0) if isinstance(vt_report, dict) else 0
    report.add_section("3. VirusTotal", [(f"Malicious detections: {hits}", 'red' if hits > 0 else 'green')], "VT_REPUTATION")
    emails = collectors.scrape_page_for_emails(domain)
    findings = [(f"[+] Found {len(emails)} email(s)", 'green')]
    for email in emails:
        findings.append((f"  - {email}", 'white'))
        pivots.append({'type': 'email', 'value': email})
    report.add_section("4. Web Content", findings, "EMAIL_SCRAPE")
    report.print_report()
    return pivots
EOF

# 3. Create person.py
cat <<'EOF' > src/dosint/modules/person.py
from dosint.core import collectors, database, reporter

def investigate(username=None, email=None, phone=None, explain=False):
    target = username or email or phone
    report = reporter.Report(f"Person Investigation for '{target}'", explain=explain)
    pivots =[]
    if username:
        hits = collectors.get_username_hits(username)
        report.add_section("Social Media", [(f"Found {len(hits)} profiles", 'green')], "USERNAME_SEARCH")
    if phone:
        info = collectors.get_phone_info(phone)
        report.add_section("Phone Analysis", [(f"{k.capitalize()}: {v}", 'white') for k, v in info.items()], "PHONE_INFO")
    if email:
        report.add_section("Email Breach Check", [("Note: Full email check requires HIBP API key.", 'yellow')])
    report.print_report()
    return pivots
EOF

# 4. Create reporter.py
cat <<'EOF' > src/dosint/core/reporter.py
from termcolor import colored
import datetime

EXPLANATIONS = {
    "FILE_TYPE": "I identify the file type to determine what analysis tools apply.",
    "EXIF": "Checking for metadata like GPS/author which reveals clues.",
    "FLAG_GREP": "Scanning content/binary strings for common flag formats.",
    "HASH_CHECK": "Verifying file reputation against VirusTotal.",
    "LOCAL_DB": "Searching our local database for previous reports on this target.",
    "WHOIS": "Analyzing domain registration age and owner data.",
    "VT_REPUTATION": "Querying security vendors via VirusTotal.",
    "EMAIL_SCRAPE": "Extracting public emails to find contact points.",
    "USERNAME_SEARCH": "Searching platforms for the username."
}

class Report:
    def __init__(self, title, explain=False):
        self.title = title
        self.explain = explain
        self.sections = []
        self.notes =[]

    def add_section(self, title, findings, explanation_key=None):
        if self.explain and explanation_key:
            findings.insert(0, (f"🤔 Why this matters: {EXPLANATIONS.get(explanation_key)}", 'grey', ['italic']))
        self.sections.append({'title': title, 'findings': findings})

    def add_note(self, note):
        self.notes.append(note)

    def print_report(self):
        print(f"\n{colored('🔍 DOSINT REPORT: ' + self.title, 'yellow', attrs=['bold'])}")
        for section in self.sections:
            print(colored(f"\n--- {section['title']} ---", 'cyan'))
            for f in section['findings']:
                text, color, *attrs = f
                print(colored(f"  {text}", color, attrs=attrs[0] if attrs else None))
        for note in self.notes: print(colored(f"\n[!] {note}", 'magenta'))
EOF

echo "[*] Build complete!"
