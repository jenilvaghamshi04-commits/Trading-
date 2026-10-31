"""Read-only web home for the original command-line trading toolkit."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
MODULES = [
    ('scanner', 'Chart Scanner', 'Find chart setups.', 'scan.py'),
    ('news', 'News Monitor', 'Review headlines and filings.', 'news.py'),
    ('entry', 'Entry Timer', 'Check entry conditions.', 'entry.py'),
    ('exit', 'Exit Planner', 'Plan stops and targets.', 'exit.py'),
    ('timemachine', 'Time Machine', 'Replay historical outcomes.', 'timemachine.py'),
    ('risk', 'Risk Manager', 'Check trade limits.', 'check.py'),
    ('budget', 'Budget Manager', 'Size positions to a budget.', 'size.py'),
    ('broker', 'Order Tickets', 'Review the original broker workflow.', 'ticket.py'),
    ('alerts', 'Price Alerts', 'Configure price conditions.', 'alerts.py'),
    ('analyst', 'Earnings Analyst', 'Review company fundamentals.', 'facts.py'),
    ('pelosi', 'Congress Tracker', 'Read public trade disclosures.', 'ptr.py'),
]
CATALOG = {slug: {'id': slug, 'name': name, 'description': desc,
    'command': f'python trader-{slug}/{script} --help'}
    for slug, name, desc, script in MODULES}


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, content, mime, head=False):
        body = content.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', mime + '; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def route(self, head=False):
        path = urlsplit(self.path).path
        if path in ('/health', '/api/health'):
            ready = all((ROOT / f'trader-{slug}' / script).is_file()
                        and (ROOT / f'trader-{slug}' / 'SKILL.md').is_file()
                        for slug, _, _, script in MODULES)
            self.respond(200 if ready else 503,
                         json.dumps({'status': 'ok' if ready else 'incomplete',
                                     'modules': len(CATALOG)}), 'application/json', head)
        elif path == '/':
            self.respond(200, (ROOT / 'index.html').read_text(), 'text/html', head)
        elif path == '/api/modules':
            self.respond(200, json.dumps(list(CATALOG.values())), 'application/json', head)
        elif path.startswith('/api/modules/') and path.rsplit('/', 1)[-1] in CATALOG:
            slug = path.rsplit('/', 1)[-1]
            data = dict(CATALOG[slug])
            data['documentation'] = (ROOT / f'trader-{slug}' / 'SKILL.md').read_text()
            self.respond(200, json.dumps(data), 'application/json', head)
        else:
            self.respond(404, json.dumps({'error': 'Not found'}), 'application/json', head)

    def do_GET(self):
        self.route()

    def do_HEAD(self):
        self.route(head=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '10000'))
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f'Day Trader web home listening on 0.0.0.0:{port}', flush=True)
    server.serve_forever()
