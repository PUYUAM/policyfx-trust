#!/usr/bin/env python3
# api/server.py — Policy+FX REST API

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs

PORT = 5000

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/fx':
            self.send_json('../data/fx/latest.json')
        elif parsed_path.path == '/api/policy':
            self.send_json('../data/policy/latest.json')
        elif parsed_path.path == '/api/shcomp':
            self.send_json('../data/shanghai/latest.json')
        else:
            self.send_error(404, 'Not Found')

    def send_json(self, file_path):
        try:
            with open(file_path) as f:
                data = json.load(f)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except FileNotFoundError:
            self.send_error(404, 'Data not found')

if __name__ == '__main__':
    server = HTTPServer(('localhost', PORT), APIHandler)
    print(f'✅ Policy+FX API running on http://localhost:{PORT}')
    server.serve_forever()