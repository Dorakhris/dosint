import yaml
import os
from dosint.core import collectors, reporter
from termcolor import colored

DORK_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'parsers', 'dorks.yaml')

def _load_dorks():
    try:
        with open(DORK_FILE_PATH, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return None

def run(target, dork_categories=None, engine='google'):
    dork_data = _load_dorks()
    if not dork_data:
        print(colored("[!] Error: Could not load dorks.yaml file.", 'red'))
        return

    report = reporter.Report(f"Dorking for '{target}' (Engine: {engine.title()})")
    categories_to_run = dork_data.get('categories', [])
    if dork_categories:
        categories_to_run = [cat for cat in categories_to_run if cat.get('name') in dork_categories]
        if not categories_to_run:
            print(colored(f"[!] Error: No valid dork categories found.", 'red'))
            return

    print(colored(f"[*] Running {len(categories_to_run)} dork categories...", 'cyan'))

    for category in categories_to_run:
        cat_name = category.get('name', 'Unknown')
        cat_findings = []
        print(colored(f"[*] Searching for '{cat_name}'...", 'yellow'))
        
        for dork_template in category.get('dorks', []):
            query = dork_template.format(target=target)
            print(f"  -> Running dork: {query}")
            
            results = []
            if engine == 'google':
                results = collectors.robust_google_search(query)
            elif engine == 'duckduckgo':
                results = collectors.robust_ddg_search(query)

            if isinstance(results, dict) and "error" in results:
                cat_findings.append((f"Dork '{query}' failed: {results['error']}", 'red'))
                break 
            elif results:
                cat_findings.append((f"Dork '{query}' found {len(results)} result(s):", 'green'))
                for url in results:
                    cat_findings.append((f"    - {url}", 'white'))
        
        report.add_section(f"Category: {cat_name.replace('_', ' ').title()}", cat_findings)

    report.print_report()
