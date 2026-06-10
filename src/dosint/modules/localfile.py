import os, re, magic, subprocess
from dosint.core import reporter

def _find_flags(content):
    regex = re.compile(r'(flag|ctf)\s*\{[a-zA-Z0-9_-]{4,}\}', re.IGNORECASE)
    text = content.decode('utf-8', errors='ignore') if isinstance(content, bytes) else content
    return [(f"🚩 Found: '{m.group(0)}'", 'red', ['bold']) for m in re.finditer(regex, text)]

def investigate(filepath, explain=False):
    if not os.path.exists(filepath): return
    report = reporter.Report(f"Local File: {os.path.basename(filepath)}", explain=explain)
    try: report.add_section("1. Basic Info", [(f"Type: {magic.from_file(filepath)}", 'white')], "FILE_TYPE")
    except: pass
    try:
        proc = subprocess.run(['strings', '-n', '6', filepath], capture_output=True, text=True, errors='ignore')
        report.add_section("2. Flag Search", _find_flags(proc.stdout) or [("No flags.", 'green')], "FLAG_GREP")
    except: pass
    report.print_report()
