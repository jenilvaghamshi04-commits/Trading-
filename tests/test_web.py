"""HTTP regressions for the scanner page and its original reference."""
import json
import threading
import unittest
from urllib.request import Request, urlopen

from _load import load

web = load('.', 'app')


class ScannerPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = web.ThreadingHTTPServer(('127.0.0.1', 0), web.Handler)
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()
        cls.base = 'http://127.0.0.1:%s' % cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join()

    def test_scanner_page_with_and_without_trailing_slash(self):
        for path in ('/scanner', '/scanner/'):
            with urlopen(self.base + path) as response:
                self.assertEqual(response.status, 200)
                self.assertIn('text/html', response.headers['Content-Type'])
                self.assertIn('Build your scan command', response.read().decode())

    def test_home_links_to_scanner(self):
        with urlopen(self.base + '/') as response:
            self.assertIn('href="/scanner"', response.read().decode())

    def test_original_reference_available(self):
        with urlopen(self.base + '/api/modules/scanner') as response:
            data = json.load(response)
            self.assertIn('# trader-scanner', data['documentation'])
            self.assertIn('--max-confirm', data['documentation'])

    def test_head_scanner_returns_no_body(self):
        with urlopen(Request(self.base + '/scanner', method='HEAD')) as response:
            self.assertEqual(response.status, 200)
            self.assertGreater(int(response.headers['Content-Length']), 0)
            self.assertEqual(response.read(), b'')
