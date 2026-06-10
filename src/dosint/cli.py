# src/dosint/cli.py

import argparse
import sys
from termcolor import colored

# Import all modules
from dosint.modules import business, person, localfile, filehash, loganalyzer, recon, setup_wizard, dorking
from dosint.core import database, reporter

def main():
    """The main entry point for the DOSINT command-line interface."""
    
    # If the user just types 'dosint', show the banner and exit.
    if len(sys.argv) == 1:
        reporter.print_banner()
        sys.exit(0)

    # --- Parent Parser for Global Arguments ---
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("-e", "--explain", action="store_true", help="Explain the investigative steps.")

    # --- Main Application Parser ---
    p = argparse.ArgumentParser(
        prog="dosint",
        description="DOSINT - An intelligent OSINT, CTF, & Forensics Assistant.",
        parents=[parent]
    )
    sub = p.add_subparsers(dest="command", required=True)
    
    # --- 1. Setup Command ---
    sub.add_parser("setup", help="Configure API keys.", parents=[parent])
    
    # --- 2. Recon Command ---
    r = sub.add_parser("recon", help="Discover live subdomains.", parents=[parent])
    r.add_argument("domain", help="The target domain.")
    
    # --- 3. Investigate Command (OSINT) ---
    inv = sub.add_parser("investigate", help="Run full OSINT investigation.", parents=[parent]).add_subparsers(dest="target", required=True)
    
    b = inv.add_parser("biz", help="Investigate a business domain.", parents=[parent])
    b.add_argument("domain", help="The domain to investigate.")
    
    ps = inv.add_parser("person", help="Investigate a person.", parents=[parent])
    ps.add_argument("--username", help="Username to investigate.")
    ps.add_argument("--email", help="Email to investigate.")
    ps.add_argument("--phone", help="Phone number to investigate.")
    
    # --- 4. Local Command (Forensics/CTF) ---
    local = sub.add_parser("local", help="Analyze a local file for flags.", parents=[parent])
    local.add_argument("filepath", help="Path to the file.")
    
    # --- 5. Hash Command ---
    h = sub.add_parser("hash", help="Check file hash reputation.", parents=[parent])
    h.add_argument("filehash", help="The hash to check.")
    
    # --- 6. Dork Command ---
    d = sub.add_parser("dork", help="Automate Google Dorking.", parents=[parent])
    d.add_argument("--target", required=True, help="The target domain/keyword.")
    d.add_argument("--dorks", help="Comma-separated list of categories.")
    d.add_argument("--engine", choices=['google', 'duckduckgo'], default='google', help="Search engine to use.")
    
    # --- 7. Analyze-Log Command ---
    l = sub.add_parser("analyze-log", help="Parse log files for IOCs.", parents=[parent])
    l.add_argument("filepath", help="Path to the log file.")
    l.add_argument("--type", required=True, help="Type of log (e.g., 'ssh_debian').")
    
    # --- 8. Report Command ---
    rep = sub.add_parser("report", help="Add indicator to local DB.", parents=[parent])
    rep.add_argument("--domain")
    rep.add_argument("--phone")
    rep.add_argument("--email")
    
    args = p.parse_args()
    
    # --- Command Routing Logic ---
    if args.command == "setup":
        setup_wizard.run()
        
    elif args.command == "recon":
        recon.run(domain=args.domain, explain=args.explain)
        
    elif args.command == "investigate":
        if args.target == "biz":
            business.investigate(domain=args.domain, explain=args.explain)
        elif args.target == "person":
            person.investigate(username=args.username, email=args.email, phone=args.phone, explain=args.explain)
            
    elif args.command == "local":
        localfile.investigate(filepath=args.filepath, explain=args.explain)
        
    elif args.command == "hash":
        filehash.investigate(file_hash=args.filehash, explain=args.explain)
        
    elif args.command == "dork":
        categories = args.dorks.split(',') if args.dorks else None
        dorking.run(target=args.target, dork_categories=categories, engine=args.engine)
        
    elif args.command == "analyze-log":
        loganalyzer.analyze(filepath=args.filepath, log_type=args.type)
        
    elif args.command == "report":
        indicators = {'domain': args.domain, 'phone': args.phone, 'email': args.email}
        report_data = {k: v for k, v in indicators.items() if v}
        if report_data:
            if database.add_report(report_data):
                print("✅ Report added successfully to the local database.")
        else:
            print("[!] No data provided to report.")

if __name__ == "__main__":
    main()
