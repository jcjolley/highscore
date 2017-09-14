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
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    def update_command(self, post_data, game, score, imgurl=None):
        out_str = "Congratulations " + post_data['user_name'][0] + ", Updating highscore for " + game + " to " + score
        self.wfile.write(bytes(out_str, "utf-8"))
        return


    def setgamesort_command(self, post_data, game, sort):
        return

    def archive_command(self, post_data, game):
        return


    def status(self, post_data, game=None sort=None):
        return


    def parse_command(self, post_data):
        print('Post Text:', post_data['text'])
        my_args = post_data['text'][0].split(" ")
        switchMap = {
            'update' : self.update_command
        }
        command = switchMap[my_args[0]]
        my_args.pop(0)
        return command(post_data, *my_args)


    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(
            self.rfile.read(length).decode('utf-8'))
        # You now have a dictionary of the post data
        print('POST data: ', post_data)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.parse_command(post_data)


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, highScore_RequestHandler)
    print('running server...')
    httpd.serve_forever()

run()
