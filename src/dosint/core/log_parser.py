import yaml, re, os
class LogParser:
    def __init__(self, parser_name):
        parser_path = os.path.join(os.path.dirname(__file__), '..', 'parsers', f'{parser_name}.yaml')
        with open(parser_path, 'r') as f: config = yaml.safe_load(f)
        self.patterns = [{'name': p['name'], 'regex': re.compile(p['regex'])} for p in config.get('patterns',[])]
    def parse_line(self, line):
        for pattern in self.patterns:
            match = pattern['regex'].search(line)
            if match:
                event = match.groupdict()
                event['event_name'] = pattern['name']
                return event
        return None
