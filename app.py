

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__, template_folder="templates", static_folder="static")

def init_db():
    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT UNIQUE,
            candidate TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/vote", methods=["GET", "POST"])
def vote():

    if request.method == "POST":
        voter_id = request.form["voter_id"]
        candidate = request.form["candidate"]

        conn = sqlite3.connect("votes.db", timeout=10)
        cursor = conn.cursor()

        try:
            cursor.execute(
             "INSERT INTO votes(voter_id, candidate) VALUES(?, ?)",
        (voter_id, candidate)
         )
            conn.commit()
            conn.close()
            return redirect("/result")

        except sqlite3.IntegrityError:
            conn.close()
            return "You have already voted!"

        

    return render_template("vote.html")


@app.route("/result")
def result():

    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT candidate, COUNT(*)
        FROM votes
        GROUP BY candidate
    """)

    results = cursor.fetchall()

    conn.close()

    return render_template("result.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)