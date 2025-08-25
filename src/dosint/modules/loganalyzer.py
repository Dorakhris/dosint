from dosint.core.log_parser import LogParser
from collections import Counter

def analyze(filepath, log_type):
    print(f"[*] Analyzing '{filepath}' with parser '{log_type}'...")
    try: parser = LogParser(log_type)
    except ValueError as e: return print(f"[!] Error: {e}")
    
    events, unparsed = [], 0
    with open(filepath, 'r', errors='ignore') as f:
        for line in f: (events.append(e) if (e := parser.parse_line(line)) else (unparsed := unparsed + 1))

    print(f"[*] Analysis complete. Parsed {len(events)} events. ({unparsed} lines unparsed).")
    
    failed = [e for e in events if e['event_name'] == 'Failed Login']
    if failed:
        print("\n--- Failed Login Analysis ---")
        ip_counts = Counter(e['source_ip'] for e in failed)
        print("Top 5 Source IPs for Failed Logins:")
        for ip, count in ip_counts.most_common(5): print(f"  - IP: {ip}, Attempts: {count}")
