from dosint.core import collectors, reporter

def investigate(file_hash):
    report = reporter.Report(f"File Hash Analysis for '{file_hash[:15]}...'")
    vt_data = collectors.get_virustotal_hash_report(file_hash)
    findings = []
    if "error" in vt_data: findings.append((f"[!] {vt_data['error']}", 'yellow'))
    else:
        stats = vt_data.get('last_analysis_stats', {})
        hits = stats.get('malicious', 0)
        total = sum(stats.values())
        verdict = f"🚨 CRITICAL: Flagged as MALICIOUS by {hits}/{total} vendors." if hits > 0 else f"✅ CLEAN: Not flagged by any of {total} vendors."
        findings.append((verdict, 'red' if hits > 0 else 'green', ['bold']))
        if vt_data.get('meaningful_name'): findings.append((f"Common Name: {vt_data['meaningful_name']}", 'white'))
    report.add_section("VirusTotal Reputation", findings)
    report.print_report()
