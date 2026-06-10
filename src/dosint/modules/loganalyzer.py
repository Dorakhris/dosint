from dosint.core.log_parser import LogParser
from dosint.core import reporter
from collections import Counter
import os
from termcolor import colored

def analyze(filepath, log_type):
    if not os.path.exists(filepath):
        print(colored(f"[!] Error: Log file not found.", 'red'))
        return

    report = reporter.Report(f"Log Analysis for '{os.path.basename(filepath)}'")
    
    try: 
        parser = LogParser(log_type)
    except ValueError as e: 
        print(colored(f"[!] Error loading parser: {e}", 'red'))
        return
    
    events = []
    unparsed_count = 0
    with open(filepath, 'r', errors='ignore') as f:
        for line in f:
            event = parser.parse_line(line)
            if event:
                events.append(event)
            else:
                unparsed_count += 1

    summary_findings = [
        (f"Total events parsed: {len(events)}", 'white'),
        (f"Lines unrecognized by parser: {unparsed_count}", 'yellow' if unparsed_count > 0 else 'white')
    ]
    report.add_section("1. Parsing Summary", summary_findings)

    if not events:
        report.print_report()
        return

    failed_logins = [e for e in events if e.get('event_name') == 'Failed Login']
    if failed_logins:
        fail_findings = []
        fail_findings.append((f"Total Failed Logins: {len(failed_logins)}", 'red', ['bold']))
        
        # IP Counts
        ip_counts = Counter(e.get('source_ip', 'Unknown') for e in failed_logins)
        fail_findings.append(("\nTop 5 Source IPs for Failed Logins:", 'cyan'))
        for ip, count in ip_counts.most_common(5): 
            fail_findings.append((f"  - IP: {ip} (Attempts: {count})", 'white'))
            
        # Username Counts
        user_counts = Counter(e.get('username', 'Unknown') for e in failed_logins)
        fail_findings.append(("\nTop 5 Targeted Usernames:", 'cyan'))
        for user, count in user_counts.most_common(5):
            fail_findings.append((f"  - User: {user} (Attempts: {count})", 'white'))

        report.add_section("2. Failed Login Analysis", fail_findings)
    
    report.print_report()
