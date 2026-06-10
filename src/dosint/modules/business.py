from dosint.core import collectors, database, reporter
from datetime import datetime

def investigate(domain, explain=False):
    report = reporter.Report(f"Business: {domain}", explain=explain)
    local_hits = database.find_reports('domain', domain)
    report.add_section("1. Local DB", [(f"Found {len(local_hits)} reports", 'red' if local_hits else 'green')], "LOCAL_DB")
    whois_data = collectors.get_domain_info(domain)
    findings = [(f"Created: {d.get('creation_date')}", 'green') for d in [whois_data] if 'creation_date' in d]
    report.add_section("2. WHOIS", findings or [("WHOIS lookup failed", 'yellow')], "WHOIS")
    vt_report = collectors.get_virustotal_report(domain)
    hits = vt_report.get('malicious', 0) if isinstance(vt_report, dict) else 0
    report.add_section("3. VirusTotal", [(f"Malicious detections: {hits}", 'red' if hits > 0 else 'green')], "VT_REPUTATION")
    emails = collectors.scrape_page_for_emails(domain)
    findings = [(f"[+] Found {len(emails)} email(s)", 'green')]
    pivots = []
    for email in emails:
        findings.append((f"  - {email}", 'white'))
        pivots.append({'type': 'email', 'value': email})
    report.add_section("4. Web Content", findings, "EMAIL_SCRAPE")
    report.print_report()
    return pivots
