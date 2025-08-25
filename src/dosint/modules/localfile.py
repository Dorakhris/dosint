import os, re, magic, exifread
from dosint.core import reporter

def _grep_for_flags(text_content):
    return [(f"🚩 POTENTIAL FLAG: {m.group(0)}", 'red', ['bold']) for m in re.finditer(r'(flag|ctf|key)({.*?}|\[.*?\])', text_content, re.IGNORECASE)]

def investigate(filepath):
    if not os.path.exists(filepath): return print(f"Error: File '{filepath}' not found.")
    report = reporter.Report(f"Local File Analysis for '{os.path.basename(filepath)}'")
    
    report.add_section("File Info", [(f"Type: {magic.from_file(filepath)}", 'white'), (f"Size: {os.path.getsize(filepath)} bytes", 'white')])
    
    try:
        with open(filepath, 'r', errors='ignore') as f: content = f.read()
        report.add_section("Flag Grep (Text)", _grep_for_flags(content) or [("No flags found.", 'green')])
    except Exception as e: report.add_note(f"Could not read file as text: {e}")
    
    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            if tags:
                findings = [(f"{k}: {v}", 'white') for k, v in tags.items()]
                report.add_section("EXIF Metadata", findings)
    except Exception as e: report.add_note(f"Could not process EXIF data: {e}")

    report.print_report()
