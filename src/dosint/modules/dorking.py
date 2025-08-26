# src/dosint/modules/dorking.py (Final, Resilient Version)

import yaml
import os
import random
import time
from dosint.core import collectors, reporter
from termcolor import colored

DORK_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'parsers', 'dorks.yaml')

def _load_dorks():
    """Loads the dork definitions from the YAML file."""
    try:
        with open(DORK_FILE_PATH, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return None

def run(target, dork_categories=None, num_results=5, engine='google'):
    """
    Orchestrates the Google Dorking process, with selectable engines.
    """
    dork_data = _load_dorks()
    if not dork_data:
        print(colored("[!] Error: Could not load dorks.yaml file.", 'red'))
        return

    report = reporter.Report(f"Dorking for '{target}' (Engine: {engine.title()})")
    
    categories_to_run = dork_data['categories']
    if dork_categories:
        categories_to_run = [cat for cat in categories_to_run if cat['name'] in dork_categories]
        if not categories_to_run:
            print(colored(f"[!] Error: No valid dork categories found for: {dork_categories}", 'red'))
            return

    print(colored(f"[*] Running {len(categories_to_run)} dork categories using the '{engine}' engine...", 'cyan'))

    for category in categories_to_run:
        cat_name = category['name']
        cat_findings = []
        print(colored(f"[*] Searching for '{cat_name}'...", 'yellow'))
        
        for dork_template in category['dorks']:
            query = dork_template.format(target=target)
            
            results = []
            # --- NEW: Engine selection logic ---
            if engine == 'google':
                # Call our improved Google collector with random jitter
                results = collectors.robust_google_search(query, num_results=num_results)
            elif engine == 'duckduckgo':
                # Call our new, more resilient DuckDuckGo collector
                results = collectors.robust_ddg_search(query, num_results=num_results)
            else:
                print(colored(f"Unknown search engine: {engine}", 'red'))
                break # Stop if the engine is invalid

            # --- Unified result processing ---
            if isinstance(results, dict) and "error" in results:
                error_message = results["error"]
                if "429" in error_message:
                    error_message += "\n[!] The search engine has temporarily blocked this IP. Try the 'duckduckgo' engine or wait a while."
                cat_findings.append((f"Dork '{query}' failed: {error_message}", 'red'))
                break 
            
            elif results:
                cat_findings.append((f"Dork '{query}' found {len(results)} result(s):", 'green'))
                for url in results:
                    cat_findings.append((f"    - {url}", 'white'))
        
        report.add_section(f"Category: {cat_name.replace('_', ' ').title()}", cat_findings)

    report.print_report()
