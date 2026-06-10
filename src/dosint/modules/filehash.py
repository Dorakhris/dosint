from dosint.core import collectors, reporter

def investigate(file_hash, explain=False):
    report = reporter.Report(f"Hash Analysis", explain=explain)
    vt_data = collectors.get_virustotal_hash_report(file_hash)
    findings =[]
    if "error" in vt_data: findings.append((f"[!] {vt_data['error']}", 'yellow'))
    else:
        stats = vt_data.get('last_analysis_stats', {})
        hits = stats.get('malicious', 0)
        findings.append((f"Malicious detections: {hits}", 'red' if hits > 0 else 'green'))
    report.add_section("VirusTotal Reputation", findings, "HASH_CHECK")
    report.print_report()
