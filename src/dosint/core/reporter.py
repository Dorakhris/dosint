# src/dosint/core/reporter.py

from termcolor import colored
import datetime

def print_banner():
    """
    Prints the main DOSINT startup banner.
    """
    
    # Corrected ASCII art for "DOSINT"
    banner_art = """
   ██████╗  ██████╗ ███████╗██╗███╗   ██╗████████╗
   ██╔══██╗██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
   ██║  ██║██║   ██║███████╗██║██╔██╗ ██║   ██║   
   ██║  ██║██║   ██║╚════██║██║██║╚██╗██║   ██║   
   ██████╔╝╚██████╔╝███████║██║██║ ╚████║   ██║   
   ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
    """
    
    version = "3.0.0"
    author = "Dorakhris" # Change this to your name/handle
    
    print(colored("="*60, 'yellow'))
    print(colored(banner_art, 'cyan', attrs=['bold']))
    print(colored(f"      An Intelligent OSINT, CTF, & Forensics Assistant", 'cyan'))
    print(colored("="*60, 'yellow'))
    
    print(f"Version: {version}")
    print(f"Author: {author}")
    print(f"Start Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + colored("Type 'dosint --help' to see available commands.", 'green'))
    print(colored("Example: dosint investigate biz example.com", 'green'))

class Report:
    """A class to build and print standardized reports."""
    def __init__(self, title):
        self.title = title
        self.sections = []
        self.notes = []

    def add_section(self, title, findings):
        """'findings' is a list of tuples: (text, color, *optional_attrs)"""
        self.sections.append({'title': title, 'findings': findings})

    def add_note(self, note):
        """Adds a high-level observation to the report summary."""
        self.notes.append(note)

    def print_report(self):
        """Prints the fully formatted report to the console."""
        print("\n" + colored("="*60, 'yellow'))
        print(colored(f"🔍 DOSINT REPORT: {self.title}", 'yellow', attrs=['bold']))
        print(colored("="*60, 'yellow'))
        
        for section in self.sections:
            print(colored(f"\n--- {section['title']} ---", 'cyan'))
            if not section['findings']:
                print(colored("  No information found.", 'white'))
            else:
                for finding in section['findings']:
                    # Unpack tuple, allowing for optional 'attrs' like ['bold']
                    text, color, *attrs = finding
                    attrs = attrs[0] if attrs else None
                    print(colored(f"  {text}", color, attrs=attrs))
        
        if self.notes:
            print(colored("\n--- Analyst Notes ---", 'cyan'))
            for note in self.notes:
                print(colored(f"  [!] {note}", 'magenta'))

        print(colored("\n" + "="*60, 'yellow'))
