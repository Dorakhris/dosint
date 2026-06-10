import subprocess
import json
from dosint.core import reporter
from termcolor import colored

def run(domain, explain=False):
    """
    Orchestrates reconnaissance using subfinder and a modern version of httpx.
    """
    report = reporter.Report(f"Reconnaissance for '{domain}'", explain=explain)
    pivot_indicators = []
    subdomains_input = ""

    # --- Step 1: Subdomain Enumeration ---
    if explain:
        report.add_section("Analysis Explanation (Subdomains)", [], "SUBDOMAIN_ENUM")
    
    print(colored(f"[*] Running subfinder to discover subdomains for '{domain}'... (This may take a while)", 'cyan'))
    
    try:
        subfinder_process = subprocess.run(
            ['subfinder', '-d', domain, '-silent'],
            capture_output=True, text=True, check=True
        )
        subdomains = [line.strip() for line in subfinder_process.stdout.strip().split('\n') if line.strip()]
        
        if not subdomains:
            report.add_section("1. Subdomain Enumeration", [("No subdomains found.", 'yellow')])
            report.print_report()
            return []
            
        print(colored(f"[+] Subfinder found {len(subdomains)} unique subdomains.", 'green'))
        subdomains_input = "\n".join(subdomains)
            
    except FileNotFoundError:
        report.add_section("1. Subdomain Enumeration", [("Error: 'subfinder' command not found. Please install it.", 'red')])
        report.print_report()
        return []
    except subprocess.CalledProcessError as e:
        report.add_section("1. Subdomain Enumeration", [(f"Subfinder failed: {e.stderr}", 'red')])
        report.print_report()
        return []

    # --- Step 2: Probe for Live Web Servers ---
    if explain:
        report.add_section("Analysis Explanation (HTTP Probing)", [], "HTTP_PROBE")
    print(colored(f"\n[*] Running httpx to find live web servers from {len(subdomains)} subdomains...", 'cyan'))
    
    try:
        httpx_cmd = ['httpx', '-json', '-title', '-status-code']
        httpx_process = subprocess.run(
            httpx_cmd,
            input=subdomains_input,
            capture_output=True,
            text=True,
            check=True
        )
        
        live_hosts_findings = []
        for line in httpx_process.stdout.strip().split('\n'):
            if line:
                try:
                    data = json.loads(line)
                    status_code = data.get('status_code', 0)
                    title = data.get('title', 'No Title').strip()
                    url = data.get('url', '')
                    
                    color = 'green' if 200 <= status_code < 300 else 'yellow' if 300 <= status_code < 400 else 'red'
                    
                    finding_text = f"{url} [{colored(status_code, color)}] - '{title}'"
                    live_hosts_findings.append((finding_text, 'white'))
                    
                    domain_pivot = url.split('//')[-1].split('/')[0]
                    pivot_indicators.append({'type': 'domain', 'value': domain_pivot})
                    
                except json.JSONDecodeError:
                    continue

        if not live_hosts_findings:
            report.add_section("2. Live Host Discovery", [("No live web servers found.", 'yellow')])
        else:
            report.add_section("2. Live Host Discovery", live_hosts_findings)
            report.add_note(f"Found {len(live_hosts_findings)} live web server(s). These are your primary targets.")

    except FileNotFoundError:
        report.add_section("2. Live Host Discovery", [("Error: 'httpx' command not found. Please install it.", 'red')])
    except subprocess.CalledProcessError as e:
        report.add_section("2. Live Host Discovery", [(f"httpx failed with error: {e.stderr}", 'red')])
        
    report.print_report()
    return pivot_indicators
