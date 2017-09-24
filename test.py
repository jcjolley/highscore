#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import MySQLdb

# HTTPRequestHandler class

db = MySQLdb.connect(host="localhost",
                     user="highscores",
                     passwd="highscores",
                     db="highscores")


def getScores(cur, game):
    sql = """ SELECT p.Name, s.Score 
              FROM Scores as s 
              JOIN Players as p ON p.ID = s.PlayerID 
              JOIN Games as g ON g.ID = s.GameID 
              WHERE g.Name = %s
              ORDER BY s.Score * g.sort; """

    cur.execute(sql, (game,))
    score_rows = cur.fetchall()
    
    print('Score rows are: ', score_rows)
    
    if (score_rows):
        count = 0
        out_str = "Leaderboard for " + str(game) + ": \n ```"
        for row in score_rows:
            count += 1
            name, score = row
            print("Row is: ", row)
            print("Name: ", name, "Score: ", score)
            out_str += str(count) + ". " + str(score) + " - " + name + "\n"
        out_str += "```\n"
    else:
        out_str = "No scores for " + str(game) + "."
    return out_str


def get_or_create_user(cur, slackid, name, teamid):
    sql = """ call get_or_create_user(%s, %s, %s) """
    cur.execute(sql, (name, teamid, slackid))
    user_id = cur.fetchall()
    print("Fetched user_id: ", user_id[0][0])
    return user_id[0][0]


def get_or_create_game(cur, game, teamid):
    sql = """ call get_or_create_game(%s, %s) """
    cur.execute(sql, (game, teamid))
    game_id = cur.fetchall()
    print("Fetched game_id: ", game_id[0][0])
    return game_id[0][0]


def get_game(cur, game, teamid):
    sql = """ call get_game(%s, %s) """

    try:
        cur.execute(sql, (game, teamid))
        game_id = cur.fetchall()
        print("Fetched game_id: ", game_id[0][0])
    except Exception:
        game_id = -1

    return game_id[0][0]


def update_scores(cur, slackid, name, teamid, game, score):
    user_id = get_or_create_user(cur, slackid, name, teamid)
    game_id = get_game(cur, game, teamid)
    if (game_id == -1 ):
        raise Exception
    sql = """ call update_score(%s, %s, %s) """
    cur.execute(sql, (game_id, user_id, score))
    rows = cur.fetchall()
    for row in rows:
        user_name, game_name, new_score = row
        print(user_name, "'s New score for", game_name, "is", str(new_score))
        return (user_name, game_name, new_score)

def get_all_scores(cur):
    sql = "SELECT Name from Games;"
    cur.execute(sql)
    rows = cur.fetchall()
    score_strings = []
    for game_name in rows:
        score_strings.append(getScores(cur, game_name[0]))
    return score_strings
    


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
        name = post_data['user_name'][0]
        slackid = post_data['user_id'][0]
        teamid = post_data['team_id'][0]
        cur = db.cursor()

        try:
            user_name, game_name, new_score = update_scores(cur, slackid, name, teamid, game, score)
            out_str = "Congratulations " + user_name + ", Updating highscore for " + game_name + " to " + str(new_score)
        except Exception:
            out_str = "We haven't started competing on " + game + "yet.  Please add it if you wish to track scores for it"
            
        self.wfile.write(bytes(out_str, "utf-8"))
        cur.close()
        db.commit()
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

        cur = db.cursor()
        if (game): 
            out_str = "Leaderboard for " + game + " is: "
            out_str += getScores(cur, game)
        else:
            out_str = "\n".join(get_all_scores(cur))
        
        self.wfile.write(bytes(out_str, "utf-8"))
        cur.close()
        db.commit()
        return

    def add_command(self, post_data, game):
        sql = "SELECT * FROM "

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
