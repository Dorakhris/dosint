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
    "USERNAME_SEARCH": "Searching platforms for the username.",
    "PHONE_INFO": "Analyzing the phone number for carrier and location.",
    "SUBDOMAIN_ENUM": "Discovering hidden subdomains to map the target's attack surface.",
    "HTTP_PROBE": "Probing subdomains to verify which are running live web services."
}

def print_banner():
    print(colored("="*60, 'yellow'))
    print(colored("   DOSINT: An Intelligent OSINT & Forensics Assistant by Dorakhris", 'cyan', attrs=['bold']))
    print(colored("="*60, 'yellow'))

class Report:
    def __init__(self, title, explain=False):
        self.title = title
        self.explain = explain
        self.sections = []
        self.notes =[]

    def add_section(self, title, findings, explanation_key=None):
        if self.explain and explanation_key:
            expl = EXPLANATIONS.get(explanation_key, "No explanation available.")
            findings.insert(0, (f"🤔 Why this matters: {expl}", 'grey', ['italic']))
        self.sections.append({'title': title, 'findings': findings})

    def add_note(self, note):
        self.notes.append(note)

    def print_report(self):
        print(f"\n{colored('🔍 DOSINT REPORT: ' + self.title, 'yellow', attrs=['bold'])}")
        for section in self.sections:
            print(colored(f"\n--- {section['title']} ---", 'cyan'))
            for f in section['findings']:
                if isinstance(f, tuple) and len(f) >= 2:
                    text, color, *attrs = f
                    print(colored(f"  {text}", color, attrs=attrs[0] if attrs else None))
                else:
                    print(colored(f"  {f}", 'white'))
        for note in self.notes: print(colored(f"\n[!] {note}", 'magenta'))
