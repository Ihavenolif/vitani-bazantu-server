import json
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

class Hlasy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trida = db.Column(db.String(256))
    kod = db.Column(db.String(256))
    voted = db.Column(db.Integer)

class Odpovedi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trida = db.Column(db.String(256))
    otazka = db.Column(db.String(256))
    odpoved = db.Column(db.String(256))
    jmeno = db.Column(db.String(256))
    kod = db.Column(db.String(256))
    body_zapsany = db.Column(db.Integer)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/body")
def body():
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

    return render_template("body.html", sum1a=sum1a, sum1b=sum1b, sum1c=sum1c)

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

@app.route("/kviz", methods=["GET", "POST"])
def kviz():
    if request.method == "POST":
        if request.form["request_type"] == "time_up":
            kod = request.form["kod"]
            hlas = Hlasy.query.filter_by(kod=kod).first()
            hlas.voted = 1
            db.session.commit()
            return render_template("cas_vyprsel.html")

        if request.form["request_type"] == "post_kviz":
            if Odpovedi.query.filter_by(kod=request.form["kod"]).first().body_zapsany == 1:
                return render_template("hlasy_zapsany.html")
            name = request.form["name"]
            if name == "":
                name = "(Anonymní)"
            entry = Entry(timestamp=math.floor(datetime.timestamp(datetime.now())*1000), trida=request.form["trida"], pocetBodu=1, aktivita="Bod za správnou odpověď v kvízu od soutěžícího " + name + "!")
            odpoved = Odpovedi.query.filter_by(kod=request.form["kod"]).first()
            odpoved.jmeno = name
            odpoved.body_zapsany = 1
            db.session.add(entry)
            db.session.commit()
            return render_template("post_post_kviz_spravne.html")


        odpoved = request.form["odpoved"]
        kod = request.form["kod"]

        with open("question_data.json") as json_file:
            KVIZ_DATA = json.load(json_file)

        QUESTION_DATA = KVIZ_DATA[kod]

        hlas = Hlasy.query.filter_by(kod=kod).first()
        hlas.voted = 1
        odpovedEntry = Odpovedi(odpoved=QUESTION_DATA["odpoved" + str(odpoved)], otazka=QUESTION_DATA["otazka"], trida=request.form["trida"], jmeno="Anonymní", kod=kod, body_zapsany=0)
        db.session.add(odpovedEntry)
        db.session.commit()

        if str(QUESTION_DATA["spravnaOdpoved"]) == odpoved:
            return render_template("post_kviz_spravne.html", trida=request.form["trida"], spravnaOdpoved=QUESTION_DATA["odpoved" + str(QUESTION_DATA["spravnaOdpoved"])], kod=kod)
        else:
            return render_template("post_kviz_spatne.html", spravnaOdpoved=QUESTION_DATA["odpoved" + str(QUESTION_DATA["spravnaOdpoved"])])

    try:
        kod = request.args["kod"]
    except:
        return render_template("kod_nenalezen.html")

    hlas = Hlasy.query.filter_by(kod=kod).first()

    if not hlas:
        return render_template("kod_nenalezen.html")

    with open("question_data.json") as json_file:
        KVIZ_DATA = json.load(json_file)

    QUESTION_DATA = KVIZ_DATA[kod]

    if hlas.voted == 1:
        return render_template("kod_vyuzit.html")

    return render_template("kviz.html", 
        otazka=QUESTION_DATA["otazka"], 
        odpoved1=QUESTION_DATA["odpoved1"], 
        odpoved2=QUESTION_DATA["odpoved2"],
        odpoved3=QUESTION_DATA["odpoved3"],
        odpoved4=QUESTION_DATA["odpoved4"],
        kod=kod,
        trida=hlas.trida
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0")