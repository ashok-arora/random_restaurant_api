from flask import Flask
import sqlite3
import requests
import json

app = Flask(__name__)

con = sqlite3.connect('restaurants.db', check_same_thread=False)
cur = con.cursor()

@app.route("/setup/<count>", methods=["GET"])
def setup(count):
    cur.execute('CREATE TABLE IF NOT EXISTS info (name, type, description)')
    for _ in range(int(count)):
        r = requests.get('https://random-data-api.com/api/restaurant/random_restaurant').json()
        cur.execute('INSERT INTO info VALUES (?, ?, ?)', (r["name"],r["type"],r["description"]))
    con.commit()
    return f'Added {count} restaurants.'

@app.route("/<r_type>", methods=["GET"])
def filter(r_type):
    cur.execute("SELECT name, description FROM info WHERE type=?", [r_type])

    filtered = []
    for row in cur:
        info = dict(zip(['name', 'decription'], row))
        filtered.append(info)

    return json.dumps(filtered)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)