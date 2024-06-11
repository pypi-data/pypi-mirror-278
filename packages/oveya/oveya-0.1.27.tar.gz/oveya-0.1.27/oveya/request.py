# vaul/request.py
from urllib.parse import urlparse, parse_qs
import json

class Request:
    def __init__(self, event):
        self.method = event['requestContext']['http']['method'].upper()
        self.path = event['requestContext']['http']['path']
        self.headers = {k.lower(): v for k, v in event.get('headers', {}).items() if v is not None}
        self.body = self._parse_body(event.get('body', ''), self.headers.get('content-type', ''))
        self.query_params = self._parse_query_params(self.path)

    @staticmethod
    def _parse_query_params(path):
        if '?' in path:
            parsed = urlparse(path)
            parsed_params = parse_qs(parsed.query)
            return {k: v[0] for k, v in parsed_params.items()}
        return {}

    @staticmethod
    def _parse_body(body, content_type):
        if content_type == 'application/json':
            try:
                return json.loads(body)
            except json.JSONDecodeError as e:
                raise ValueError('Invalid JSON body') from e
        return {}

    def json(self):
        return self.body if isinstance(self.body, dict) else {}
