from socketserver import ThreadingUnixDatagramServer
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import math

PASSWORD = os.getenv("PASSWORD")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    trida = db.Column(db.String(256))
    pocetBodu = db.Column(db.Integer)
    aktivita = db.Column(db.String(1024))

@app.route("/")
def index():
    entries = Entry.query.all()

    list = []

    for entry in entries:
        temp = {}
        temp["timestamp"] = entry.timestamp
        temp["trida"] = entry.trida
        temp["pocetBodu"] = entry.pocetBodu
        temp["aktivita"] = entry.aktivita
        list.append(temp)

    sum1a = 0
    sum1b = 0
    sum1c = 0

    for x in list:
        if x["trida"] == "1.A":
            sum1a += x["pocetBodu"]
        elif x["trida"] == "1.B":
            sum1b += x["pocetBodu"]
        else:
            sum1c += x["pocetBodu"]

    return render_template("index.html", sum1a=sum1a, sum1b=sum1b, sum1c=sum1c)

@app.route("/podrobnosti")
def podrobnosti():
    entries = Entry.query.all()

    list = []

    for entry in entries:
        temp = {}
        temp["timestamp"] = entry.timestamp
        temp["trida"] = entry.trida
        temp["pocetBodu"] = entry.pocetBodu
        temp["aktivita"] = entry.aktivita
        list.append(temp)
    
    return render_template("podrobnosti.html", list=list)

@app.route("/pridat_body", methods=["GET", "POST"])
def pridat_body():
    if request.method == "POST":
        if not PASSWORD == request.form["password"]:
            return "wrong password"
        
        entry = Entry(timestamp=math.floor(datetime.timestamp(datetime.now())*1000), trida=request.form["trida"], pocetBodu=int(request.form["pocetBodu"]), aktivita=request.form["aktivita"])
        db.session.add(entry)
        db.session.commit()
        return "body pridany"
    
    return render_template("pridat_body.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0")