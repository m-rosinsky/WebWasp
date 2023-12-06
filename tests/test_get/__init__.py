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
from http.cookies import SimpleCookie

from webwasp import context
from webwasp.command.command_get import CommandGet

g_referer = ''
g_cookie_names = []
g_cookie_values = []

def test_func(func):
    def wrapper(*args, **kwargs):
        print(f"\nRunning test: {func.__name__}...")
        return func(*args, **kwargs)
    return wrapper

class MyTest(unittest.TestCase):
    SERVER_URL = 'http://localhost:8000'
    FILENAME = 'sample.html'
    FULL_URL = f"{SERVER_URL}/{FILENAME}"
    
    # Use os.linesep for sample data for compatiblity with ubuntu
    # and windows tests.
    SAMPLE_CONTENT = f"""<!DOCTYPE html>{os.linesep}<html>{os.linesep}<head>{os.linesep}<title>Sample Page</title>{os.linesep}</head>{os.linesep}<body>{os.linesep}<h1>Sample Header</h1>{os.linesep}</body>{os.linesep}</html>"""

    class GetHandler(SimpleHTTPRequestHandler):
        def do_GET(self) -> None:
            global g_referer
            global g_cookie_names
            global g_cookie_values

            g_referer = self.headers.get('referer')
            if g_referer is not None:
                print(f"Got 'referer': '{g_referer}'")
            
            cookie_header = self.headers.get('Cookie')
            cookies = SimpleCookie(cookie_header)

            for cookie in cookies.values():
                print(f"Got cookie: '{cookie.key}' : '{cookie.value}'")
                g_cookie_names.append(cookie.key)
                g_cookie_values.append(cookie.value)

            return super().do_GET()

    @classmethod
    def setUpClass(cls):
        # Write sample data.
        with open(cls.FILENAME, 'w', encoding='utf-8') as f:
            f.write(cls.SAMPLE_CONTENT)

        # Spawn a thread to stand up the server.
        cls.server_thread = threading.Thread(target=cls.run_http_server)
        cls.server_thread.start()

        # Allow server to start.
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        # Close the HTTP server.
        cls.httpd.shutdown()
        cls.httpd.server_close()

        # Join the thread.
        cls.server_thread.join()

        # Remove sample data.
        os.remove(cls.FILENAME)

    @classmethod
    def run_http_server(cls):
        server_address = ('', 8000)
        cls.httpd = HTTPServer(server_address, cls.GetHandler)
        cls.httpd.serve_forever()

    @test_func
    def test_get_sample(self):
        # Create the context object.
        c = context.Context()
        self.assertIsNotNone(c)

        # Create the URL and the command parse.
        parse = [self.FULL_URL]

        # Create the command class and execute it with the command parse and
        # context.
        get_command = CommandGet('get')
        get_command.run(parse, c)

        # Perform assertions about the response.
        self.assertTrue(c.has_response)
        self.assertEqual(c.response.req.status_code, 200)
        self.assertEqual(c.response.req_text, self.SAMPLE_CONTENT)        

    @test_func
    def test_get_referer(self):
        c = context.Context()
        c.headers['referer'] = 'myref'

        # Create the command parse.
        parse = [self.FULL_URL]

        # Create the command class and execute it with the command parse and
        # context.
        get_command = CommandGet('get')
        get_command.run(parse, c)

        self.assertTrue(c.has_response)
        self.assertEqual(c.response.req.status_code, 200)
        self.assertEqual(c.response.req_text, self.SAMPLE_CONTENT)
        self.assertEqual('myref', g_referer)

    @test_func
    def test_get_cookies(self):
        c = context.Context()
        c.cookies['my_cookie'] = 'cookie_value'

        # Create the command parse.
        parse = [self.FULL_URL]

        # Create the command class and execute it with the command parse and
        # context.
        get_command = CommandGet('get')
        get_command.run(parse, c)

        self.assertTrue(c.has_response)
        self.assertEqual(c.response.req.status_code, 200)
        self.assertEqual(c.response.req_text, self.SAMPLE_CONTENT)
        self.assertEqual('my_cookie', g_cookie_names[0])
        self.assertEqual('cookie_value', g_cookie_values[0])

if __name__=='__main__':
    unittest.main()
