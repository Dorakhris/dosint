# src/dosint/cli.py

import argparse
import sys
from termcolor import colored

# Import all necessary components
from .core.reporter import print_banner
from .modules import business, person, localfile, filehash, loganalyzer, setup_wizard, dorking
from .core import database

def handle_pivots(indicators):
    """
    Takes a list of indicators, presents them as an interactive menu,
    and launches a new investigation based on user choice.
    """
    if not indicators:
        return # Exit if there are no new indicators to pivot on

    print(colored("\n[?] PIVOT OPTIONS:", 'cyan', attrs=['bold']))
    
    unique_indicators = [dict(t) for t in {tuple(d.items()) for d in indicators}]
    
    for i, indicator in enumerate(unique_indicators):
        print(colored(f"  [{i+1}] Investigate {indicator['type'].capitalize()}: {indicator['value']}", 'white'))
    
    print(colored(f"  [q] Quit", 'white'))

    while True:
        choice = input(colored("\nWhat's your next move? > ", 'cyan'))
        if choice.lower() == 'q':
            sys.exit(0)
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(unique_indicators):
                chosen_indicator = unique_indicators[choice_index]
                
                print(colored(f"\nPivoting to {chosen_indicator['type']}: {chosen_indicator['value']}...", 'yellow'))
                
                pivots = []
                if chosen_indicator['type'] == 'email':
                    pivots = person.investigate(email=chosen_indicator['value'])
                elif chosen_indicator['type'] == 'domain':
                    pivots = business.investigate(domain=chosen_indicator['value'])
                elif chosen_indicator['type'] == 'username':
                    pivots = person.investigate(username=chosen_indicator['value'])
                
                handle_pivots(pivots)
                break 
            else:
                print(colored("Invalid choice. Please try again.", 'red'))
        except (ValueError, IndexError):
            print(colored("Invalid input. Please enter a number or 'q'.", 'red'))

def main():
    """The main entry point for the DOSINT command-line interface."""

    if len(sys.argv) == 1:
        print_banner()
        sys.exit(0)

    parser = argparse.ArgumentParser(
        prog="dosint",
        description="DOSINT - An intelligent OSINT, CTF, & Forensics Assistant.",
        epilog="Example: dosint dork --target example.com --engine duckduckgo"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Setup Command ---
    setup_parser = subparsers.add_parser("setup", help="Configure API keys interactively.")

    # --- Investigate Command ---
    inv_parser = subparsers.add_parser("investigate", help="Run a full OSINT investigation on a target.")
    inv_subparsers = inv_parser.add_subparsers(dest="target", required=True)
    
    biz_parser = inv_subparsers.add_parser("biz", help="Investigate a business domain.")
    biz_parser.add_argument("domain", help="The domain to investigate.")

    person_parser = inv_subparsers.add_parser("person", help="Investigate a person.")
    person_group = person_parser.add_mutually_exclusive_group(required=True)
    person_group.add_argument("--username", help="Username to investigate.")
    person_group.add_argument("--email", help="Email to investigate.")
    person_group.add_argument("--phone", help="Phone number to investigate.")

    # --- Local Command ---
    local_parser = subparsers.add_parser("local", help="Analyze a local file for CTF flags and intelligence.")
    local_parser.add_argument("filepath", help="Path to the local file.")
    
    # --- Hash Command ---
    hash_parser = subparsers.add_parser("hash", help="Check the reputation of a file hash against VirusTotal.")
    hash_parser.add_argument("filehash", help="The MD5, SHA1, or SHA256 hash to check.")

    # --- Dork Command ---
    dork_parser = subparsers.add_parser("dork", help="Automate Google Dorking to find exposed information.")
    dork_parser.add_argument("--target", required=True, help="The target domain or keyword (e.g., 'example.com').")
    dork_parser.add_argument("--dorks", help="A comma-separated list of dork categories to run (e.g., 'files,login').")
    dork_parser.add_argument("--engine", choices=['google', 'duckduckgo'], default='google', help="The search engine to use (default: google).")

    # --- Log Analyzer Command ---
    log_parser = subparsers.add_parser("analyze-log", help="Parse a log file for IOCs.")
    log_parser.add_argument("filepath", help="Path to the log file.")
    log_parser.add_argument("--type", required=True, help="The type of log (e.g., 'ssh_debian').")

    # --- Report Command ---
    report_parser = subparsers.add_parser("report", help="Report an indicator to the local intelligence database.")
    report_parser.add_argument("--domain", help="Domain indicator.")
    report_parser.add_argument("--phone", help="Phone number indicator.")
    report_parser.add_argument("--email", help="Email indicator.")

    args = parser.parse_args()

    # --- Command Routing Logic ---
    if args.command == "setup":
        setup_wizard.run()
    elif args.command == "investigate":
        pivots = []
        if args.target == "biz":
            pivots = business.investigate(domain=args.domain)
        elif args.target == "person":
            pivots = person.investigate(username=args.username, email=args.email, phone=args.phone)
        handle_pivots(pivots)
    elif args.command == "local":
        localfile.investigate(args.filepath)
    elif args.command == "hash":
        filehash.investigate(args.filehash)
    elif args.command == "dork":
        categories = args.dorks.split(',') if args.dorks else None
        dorking.run(target=args.target, dork_categories=categories, engine=args.engine)
    elif args.command == "analyze-log":
        loganalyzer.analyze(args.filepath, args.type)
    elif args.command == "report":
        indicators = {'domain': args.domain, 'phone': args.phone, 'email': args.email}
        report_data = {k: v for k, v in indicators.items() if v}
        if report_data and database.add_report(report_data):
            print("✅ Report added successfully to the local database.")
        else:
            print("[!] No data provided to report.")

if __name__ == "__main__":
    main()
