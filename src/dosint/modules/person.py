from dosint.core import collectors, database, reporter

def investigate(username=None, email=None, phone=None):
    target = username or email or phone
    report = reporter.Report(f"Person Investigation for '{target}'")
    pivots = []
    
    if username:
        hits = collectors.get_username_hits(username)
        if hits:
            findings = [(f"[+] Found {len(hits)} profile(s):", 'green')]
            for hit in hits: findings.append((f"  - {hit['site']}: {hit['url']}", 'white'))
            report.add_section("Social Media Footprint", findings)
        else: report.add_section("Social Media Footprint", [("[-] No public profiles found.", 'yellow')])
        
    if phone:
        info = collectors.get_phone_info(phone)
        report.add_section("Phone Analysis", [(f"{k.capitalize()}: {v}", 'white') for k, v in info.items()])

    if email:
        report.add_section("Email Breach Check (HIBP)", [("Note: Full email check requires HIBP API key.", 'yellow')])
        
    report.print_report()
    return pivots
