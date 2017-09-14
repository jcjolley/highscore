#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import MySQLdb

# HTTPRequestHandler class

db = MySQLdb.connect(host="jcjolley.com",
                     user="highscores",
                     passwd="highscores",
                     db="highscores")

cur = db.cursor()

def: getScores(cur, game):
    get_game_sql = "SELECT id FROM games WHERE name = %s"
    cur.execute(get_game_sql, game)
    rows = cur.fetchall()
    game_id = rows[0]
    cur.close()

    get_scores_for_game_sql = "SELECT playerId, score FROM scores WHERE gameId = %s"
    cur.execute(get_scores_for_game_sql, game_id)
    score_rows = cur.fetchall()

    out_str = "Leaderboard: \n"
    for row in score_rows
        for col in row
            out_str + col + " "
        out_str + "\n"
    
    return out_str

class HighScoreRequestHandler(BaseHTTPRequestHandler):

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
        print("We're in game sort")
        out_str ="Setting sort for " + game + " to " + sort
        self.wfile.write(bytes(out_str, "utf-8"))
        return

    def archive_command(self, post_data, game):
        out_str = game + " status set to archived"
        self.wfile.write(bytes(out_str, "utf-8"))
        return

    def status_command(self, post_data, game=None, sort=None):
        print('In status command')
        out_str = "THe default status command"
        if (game): 
            out_str = "Leaderboard for " + game + " is: <TBD>"
        else:
            out_str = "All leaderboards: <TBD>"
        
        self.wfile.write(bytes(out_str, "utf-8"))
        return

    def default_command(self, *args):
        return self.status_command(None)

    def parse_command(self, post_data):
        print('Post Text:', post_data['text'])
        my_args = post_data['text'][0].split(" ")
        switch_map = {
            'update' : self.update_command,
            'setgamesort' : self.setgamesort_command,
            'archive' : self.archive_command,
            'status' : self.status_command
        } 

        command = switch_map.get(my_args[0], self.default_command)
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
    httpd = HTTPServer(server_address, HighScoreRequestHandler)
    print('running server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
