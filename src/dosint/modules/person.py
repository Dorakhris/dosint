# src/dosint/modules/person.py

import re
from dosint.core import collectors, database, reporter
from termcolor import colored

def _generate_phone_formats(phone):
    """
    Generates common formatting variations of a phone number to maximize search hits.
    Example: +2349094915646 -> ['+2349094915646', '09094915646', '2349094915646']
    """
    formats = [phone]
    # Remove the '+' sign
    no_plus = phone.replace("+", "")
    formats.append(no_plus)
    
    # Extract local number (assumes last 10 digits for common mobile formats)
    clean_digits = re.sub(r'\D', '', phone)
    if len(clean_digits) >= 10:
        local_num = "0" + clean_digits[-10:]
        formats.append(local_num)
        
    return list(set(formats)) # Return unique formats

def investigate(username=None, email=None, phone=None, explain=False):
    """
    Orchestrates the person investigation process, now including automated
    web footprint searching for phone numbers.
    """
    target = username or email or phone
    report = reporter.Report(f"Person Investigation for '{target}'", explain=explain)
    pivots = []
    
    # --- 1. Username OSINT (Maigret) ---
    if username:
        if explain: 
            report.add_section("Analysis Explanation (Username)", [], "USERNAME_SEARCH")
        
        print(colored(f"[*] Running Maigret on username '{username}' across 100+ platforms...", 'cyan'))
        
        try:
            import subprocess
            process = subprocess.run(
                ['maigret', username, '--timeout', '5', '--top', '100'],
                capture_output=True, text=True, check=True
            )
            
            hit_pattern = re.compile(r'(?:[+|-]\s*)?([\w\d\s.-]+):\s*(https?://[^\s]+)', re.IGNORECASE)
            findings = []
            for line in process.stdout.splitlines():
                match = hit_pattern.search(line)
                if match:
                    site_name = match.group(1).strip()
                    url = match.group(2).strip()
                    if "maigret" not in url.lower() and "dbhub" not in url.lower():
                        findings.append((f"[+] Found on {site_name}: {url}", 'green'))
            
            report.add_section("Social Media Footprint (Maigret)", findings or [("No profiles found.", 'yellow')])
            
        except FileNotFoundError:
            report.add_section("Social Media Footprint (Maigret)", [("[!] Error: 'maigret' is not installed in your venv.", 'red')])
        except subprocess.CalledProcessError as e:
            report.add_section("Social Media Footprint (Maigret)", [(f"[!] Maigret execution failed: {e.stderr}", 'red')])

    # --- 2. Email Intelligence (DeHashed & Epieos) ---
    if email:
        # DeHashed
        print(f"[*] Querying DeHashed for '{email}'...")
        breach_data = collectors.query_dehashed(email)
        breach_findings = []
        if isinstance(breach_data, dict) and "error" in breach_data:
            breach_findings.append((f"[!] {breach_data['error']}", 'yellow'))
        else:
            for entry in breach_data.get('entries', []):
                breach_findings.append((f"Found in database: {entry.get('database_name')}", 'red'))
        report.add_section("Email Breach Results (DeHashed)", breach_findings or [("No breaches found.", 'green')])

        # Epieos Check
        print(f"[*] Querying Epieos for '{email}'...")
        epieos_data = collectors.query_epieos(email)
        epieos_findings = []
        if isinstance(epieos_data, dict) and "error" in epieos_data:
            epieos_findings.append((f"[!] {epieos_data['error']}", 'yellow'))
        else:
            epieos_findings.append((f"Footprint: {epieos_data}", 'white'))
        report.add_section("Epieos Intelligence", epieos_findings)

    # --- 3. Phone Analysis & Web Footprint ---
    if phone:
        if explain: 
            report.add_section("Analysis Explanation (Phone)", [], "PHONE_INFO")
            
        phone_findings = []
        info = collectors.get_phone_info(phone)
        if "error" in info:
            phone_findings.append((info['error'], 'red'))
            report.add_section("Phone Number Analysis", phone_findings)
        else:
            phone_findings.append((f"Country: {info.get('country')}", 'white'))
            phone_findings.append((f"Carrier: {info.get('carrier')}", 'white'))
            report.add_section("Phone Number Analysis", phone_findings)
            
            # --- NEW: Automated Web Footprint Search for the Phone Number ---
            print(colored("[*] Searching the web for public exposure of this phone number...", 'cyan'))
            formats = _generate_phone_formats(phone)
            web_hits = []
            
            for fmt in formats:
                # We use the fast and resilient DuckDuckGo engine we integrated
                search_query = f'"{fmt}"'
                print(f"  -> Searching for format: {search_query}")
                hits = collectors.robust_ddg_search(search_query, num_results=3)
                
                if isinstance(hits, list) and hits:
                    for url in hits:
                        # Clean up duplicates
                        if url not in [h[0] for h in web_hits]:
                            web_hits.append((f"[+] Found exposure: {url}", 'green'))
            
            report.add_section("Phone Web Footprint", web_hits or [("No public web exposure found.", 'green')])
        
    report.print_report()
    return pivots
