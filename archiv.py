from __main__ import app
from flask import render_template

@app.route("/archiv")
def archiv():
    return render_template("archiv/archiv.html")

@app.route("/archiv/vitani_novacku")
def vitani():
    return render_template("archiv/vitani_novacku.html")

