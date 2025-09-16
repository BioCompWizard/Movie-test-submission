# coding: utf-8
import sys
import json
import urllib2
import time

def get_token(server_url):
    auth_data = json.dumps({"username": "username", "password": "password"})
    req = urllib2.Request(server_url + "/api/auth")
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, auth_data)
    data = json.loads(response.read())
    return data["bearer"]

def count_movies_for_year(server_url, token, year):
    total = 0
    page = 1
    current_token = token  # Start with the first token.
    while True:
        url = server_url + "/api/movies/" + year + "/" + str(page)
        req = urllib2.Request(url)
        req.add_header('Authorization', 'Bearer ' + current_token)
        try:
            response = urllib2.urlopen(req)
            movies = json.loads(response.read())
            count = len(movies)
            total += count
            if count < 10:
                break
            page += 1
            time.sleep(0.1)  # Wait to be nice.
        except urllib2.HTTPError as e:
            if e.code == 401:  # Token expired, get a new one!
                print "Token expired - getting a new one!"
                current_token = get_token(server_url)
                continue  # Try the same page again with new token.
            if e.code == 404:
                break
            print "Oops on page " + str(page) + ": " + str(e)
            break
    return total

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Give me years! Like: python movie_client.py 2000 2010"
        sys.exit(1)

    server_url = "http://localhost:8080"
    try:
        token = get_token(server_url)
    except Exception as e:
        print "Token trouble: " + str(e)
        sys.exit(1)

    for year in sys.argv[1:]:
        count = count_movies_for_year(server_url, token, year)
        print "Year " + year + " has " + str(count) + " movies!"