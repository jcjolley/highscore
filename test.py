#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

# HTTPRequestHandler class


class highScore_RequestHandler(BaseHTTPRequestHandler):

  # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(
            self.rfile.read(length).decode('utf-8'))
        # You now have a dictionary of the post data
        print('POST data: ', post_data)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("<html><body><p>Post Recieved</p></body></html>", "utf-8"))


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, highScore_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
