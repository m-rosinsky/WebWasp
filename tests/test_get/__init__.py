"""
File:
    tests/test_get/__init__.py

Brief:
    This file contains tests for the GET command.
"""

import os
import threading
import time
import unittest
import urllib.request

from http.server import SimpleHTTPRequestHandler, HTTPServer

from webwasp import context
from webwasp.command.command_get import CommandGet

class MyTest(unittest.TestCase):
    SERVER_URL = 'http://localhost:8000'
    FILENAME = 'sample.html'

    SAMPLE_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Sample Page</title>
</head>
<body>
    <h1>Sample Header</h1>
</body>
</html>
"""

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=cls.run_http_server)
        cls.server_thread.start()

        # Allow server to start.
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.server_thread.join()

    @classmethod
    def run_http_server(cls):
        server_address = ('', 8000)
        cls.httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        cls.httpd.serve_forever()

    def test_get_sample(self):
        # Write sample data.
        with open(self.FILENAME, 'w', encoding='utf-8') as f:
            f.write(self.SAMPLE_CONTENT)

        # Create the context object.
        c = context.Context()
        self.assertIsNotNone(c)

        # Create the URL and the command parse.
        url = f"{self.SERVER_URL}/{self.FILENAME}"
        parse = [url]

        # Create the command class and execute it with the command parse and
        # context.
        get_command = CommandGet('get')
        get_command.run(parse, c)

        # Perform assertions about the response.
        self.assertTrue(c.has_response)
        self.assertEqual(c.response.req.status_code, 200)
        self.assertEqual(c.response.req_text, self.SAMPLE_CONTENT)

        self.assertEqual(1, 2)

        # Remove sample data.
        os.remove(self.FILENAME)

if __name__=='__main__':
    unittest.main()
