import yaml
import re
import os

class LogParser:
    def __init__(self, parser_name):
        parser_path = os.path.join(os.path.dirname(__file__), '..', 'parsers', f'{parser_name}.yaml')
        if not os.path.exists(parser_path): raise ValueError(f"Parser '{parser_name}.yaml' not found.")
        with open(parser_path, 'r') as f: self.config = yaml.safe_load(f)
        self.patterns = [{'name': p['name'], 'regex': re.compile(p['regex'])} for p in self.config.get('patterns', [])]

    def parse_line(self, line):
        for pattern in self.patterns:
            match = pattern['regex'].search(line)
            if match:
                event = match.groupdict()
                event['event_name'] = pattern['name']
                return event
        return None
