from datetime import datetime
from dosint.core import collectors, database, reporter

def investigate(domain):
    report = reporter.Report(f"Business Investigation for '{domain}'")
    pivots = []
    
    local_hits = database.find_reports('domain', domain)
    report.add_section("Local DB Check", [(f"🚨 Found {len(local_hits)} report(s) in local DB.", 'red', ['bold'])] if local_hits else [("[+] Domain not found in local DB.", 'green')])

    whois_data = collectors.get_domain_info(domain)
    if "error" in whois_data: report.add_section("WHOIS", [(whois_data['error'], 'yellow')])
    else:
        findings = []
        c_date = whois_data.get("creation_date")
        if isinstance(c_date, list): c_date = c_date[0]
        if c_date:
            age_days = (datetime.now() - c_date).days
            findings.append((f"Created: {c_date.strftime('%Y-%m-%d')} ({age_days/365.25:.1f} years ago)", 'yellow' if age_days < 365 else 'green'))
            if age_days < 180: report.add_note("Domain is very new (red flag).")
        if whois_data.get("registrar"): findings.append((f"Registrar: {whois_data.get('registrar')}", 'white'))
        report.add_section("WHOIS", findings)

    vt_report = collectors.get_virustotal_report(domain)
    if "error" in vt_report: report.add_section("VirusTotal", [(vt_report['error'], 'yellow')])
    else:
        hits = vt_report.get('malicious', 0)
        report.add_section("VirusTotal", [(f"Malicious detections: {hits}", 'red' if hits > 0 else 'green')])
        if hits > 0: report.add_note("VirusTotal flagged this domain as malicious.")

    print("[*] Scraping homepage for emails...")
    emails = collectors.scrape_page_for_emails(domain)
    if emails:
        findings = [(f"[+] Found {len(emails)} email(s):", 'green')]
        for email in emails:
            findings.append((f"  - {email}", 'white'))
            pivots.append({'type': 'email', 'value': email})
        report.add_section("Email Scraping", findings)
    
    report.print_report()
    return pivots
