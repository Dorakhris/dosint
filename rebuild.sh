#!/bin/bash
echo "[*] Cleaning and Rebuilding DOSINT..."
rm -rf src/*
mkdir -p src/dosint/core src/dosint/modules src/dosint/parsers

# Initialize Packages
touch src/dosint/__init__.py src/dosint/core/__init__.py src/dosint/modules/__init__.py

# 1. Create database.py
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

# 2. Create reporter.py
cat <<'EOF' > src/dosint/core/reporter.py
from termcolor import colored
import datetime
class Report:
    def __init__(self, title, explain=False):
        self.title = title
        self.explain = explain
        self.sections =[]
        self.notes =[]
    def add_section(self, title, findings, explanation=""):
        if self.explain and explanation:
            findings.insert(0, (f"🤔 Why this matters: {explanation}", 'grey', ['italic']))
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

# 3. Create log_parser.py
cat <<'EOF' > src/dosint/core/log_parser.py
import yaml, re, os
class LogParser:
    def __init__(self, parser_name):
        parser_path = os.path.join(os.path.dirname(__file__), '..', 'parsers', f'{parser_name}.yaml')
        with open(parser_path, 'r') as f: config = yaml.safe_load(f)
        self.patterns = [{'name': p['name'], 'regex': re.compile(p['regex'])} for p in config.get('patterns',[])]
    def parse_line(self, line):
        for pattern in self.patterns:
            if match := pattern['regex'].search(line):
                event = match.groupdict()
                event['event_name'] = pattern['name']
                return event
        return None
EOF

# 4. Create collectors.py
cat <<'EOF' > src/dosint/core/collectors.py
import requests, whois, os, re, time, random, phonenumbers
from phonenumbers import geocoder, carrier
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from ddgs import DDGS
from termcolor import colored

def _get_api_key(k):
    import configparser
    c = configparser.ConfigParser()
    c.read(os.path.join(os.path.dirname(__file__), '../../../config.ini'))
    return c.get('API_KEYS', k, fallback=None)

def get_virustotal_report(d):
    k = _get_api_key("VIRUSTOTAL_API_KEY")
    if not k: return {"error": "API Key missing"}
    r = requests.get(f'https://www.virustotal.com/api/v3/domains/{d}', headers={'x-apikey': k}, timeout=10)
    return r.json()['data']['attributes']['last_analysis_stats'] if r.status_code == 200 else {"error": "API Error"}

def get_domain_info(d):
    try:
        w = whois.whois(d)
        return {"creation_date": w.creation_date, "registrar": w.registrar}
    except Exception as e: return {"error": str(e)}

def get_phone_info(p):
    try:
        num = phonenumbers.parse(p)
        return {"country": geocoder.description_for_number(num, "en"), "carrier": carrier.name_for_number(num, "en")}
    except: return {"error": "Invalid phone"}

def get_username_hits(u):
    sites = {"GitHub": f"https://github.com/{u}", "Twitter": f"https://twitter.com/{u}"}
    found =[]
    for s, url in sites.items():
        if requests.get(url, timeout=5).status_code == 200: found.append({"site": s, "url": url})
    return found

def scrape_page_for_emails(d):
    try:
        r = requests.get(f"https://{d}", timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        return list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text)))
    except: return[]
EOF

# 5. Create cli.py
cat <<'EOF' > src/dosint/cli.py
import argparse, sys
from dosint.modules import business, person, localfile, filehash, loganalyzer, recon
from dosint.core import database, reporter

def main():
    if len(sys.argv) == 1: reporter.print_banner(); sys.exit(0)
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("-e", "--explain", action="store_true")
    p = argparse.ArgumentParser(prog="dosint", parents=[parent])
    sub = p.add_subparsers(dest="command", required=True)
    
    sub.add_parser("setup", parents=[parent])
    r = sub.add_parser("recon", parents=[parent]); r.add_argument("domain")
    inv = sub.add_parser("investigate", parents=[parent]).add_subparsers(dest="target", required=True)
    b = inv.add_parser("biz", parents=[parent]); b.add_argument("domain")
    ps = inv.add_parser("person", parents=[parent]); ps.add_argument("--username"); ps.add_argument("--email"); ps.add_argument("--phone")
    sub.add_parser("local", parents=[parent]).add_argument("filepath")
    sub.add_parser("hash", parents=[parent]).add_argument("filehash")
    sub.add_parser("report", parents=[parent]).add_argument("--domain"); sub.add_parser("report").add_argument("--phone")
    
    args = p.parse_args()
    if args.command == "investigate":
        if args.target == "biz": business.investigate(args.domain, args.explain)
        elif args.target == "person": person.investigate(args.username, args.email, args.phone, args.explain)
    elif args.command == "local": localfile.investigate(args.filepath, args.explain)
    elif args.command == "hash": filehash.investigate(args.filehash, args.explain)
    elif args.command == "report": database.add_report({'domain': args.domain, 'phone': args.phone})

if __name__ == "__main__":
    main()
EOF

# Create empty business.py, person.py, filehash.py, localfile.py, loganalyzer.py, setup_wizard.py
touch src/dosint/modules/business.py src/dosint/modules/person.py src/dosint/modules/filehash.py src/dosint/modules/localfile.py src/dosint/modules/loganalyzer.py src/dosint/modules/setup_wizard.py

echo "[*] DOSINT rebuilt. Please paste the code into your module files."
