import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import math
import logging

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='log.log')

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
    spravne = db.Column(db.Integer)

@app.route("/jestlitohlenekdouhadnetakjegej")
def body_realtime():
    return render_template("body_realtime.html")

@app.route("/jestlitohlenekdouhadnetakjekokot")
def body_realtime_zapis():
    return render_template("realtime_zapis_bodu.html")

@app.route("/jasetistrasnemocomlouvam")
def livechat():
    return render_template("livechat.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/g5jeguq2")
def kod_na_dvorku_a():
    f = open("detektivka_log.txt", "a")
    f.write("A našlo kód na dvorku - " + str(datetime.now()) + "\n")
    f.close()
    return render_template("detektivka/day1/kod_na_dvorku_a.html")

@app.route("/qafu9fg3")
def kod_na_dvorku_b():
    f = open("detektivka_log.txt", "a")
    f.write("B našlo kód na dvorku - " + str(datetime.now()) + "\n")
    f.close()
    return render_template("detektivka/day1/kod_na_dvorku_b.html")

@app.route("/io6ednnl")
def kod_na_dvorku_c():
    f = open("detektivka_log.txt", "a")
    f.write("C našlo kód na dvorku - " + str(datetime.now()) + "\n")
    f.close()
    return render_template("detektivka/day1/kod_na_dvorku_c.html")

@app.route("/e04szccd")
def kod_mimo_skolu_a():
    f = open("detektivka_log.txt", "a")
    f.write("A našlo kód na hřišti - " + str(datetime.now()) + "\n")
    f.close()
    return render_template("detektivka/day1/kod_mimo_skolu.html")

@app.route("/nfqgrui6")
def kod_mimo_skolu_b():
    f = open("detektivka_log.txt", "a")
    f.write("B našlo kód v altánku - " + str(datetime.now()) + "\n")
    f.close()
    return render_template("detektivka/day1/kod_mimo_skolu.html")

@app.route("/zq17hdr8")
def kod_mimo_skolu_c():
    f = open("detektivka_log.txt", "a")
    f.write("C našlo kód u pomníku - " + str(datetime.now()) + "\n")
    f.close()
    return render_template("detektivka/day1/kod_mimo_skolu.html")

@app.route("/7ozk1bw5")
def oteviraci_doba():
    return render_template("detektivka/day3/oteviraci_doba.html")

@app.route("/prehled_kvizu")
def prehled_kvizu():
    odpovedi = Odpovedi.query.all()

    spravne1a = 0
    spravne1b = 0
    spravne1c = 0
    spatne1a = 0
    spatne1b = 0
    spatne1c = 0

    for odpoved in odpovedi:
        if odpoved.spravne == 1:
            if odpoved.trida == "1.A":
                spravne1a += 1
            elif odpoved.trida == "1.B":
                spravne1b += 1
            else:
                spravne1c += 1  
        else:
            if odpoved.trida == "1.A":
                spatne1a += 1
            elif odpoved.trida == "1.B":
                spatne1b += 1
            else:
                spatne1c += 1 
          

    percentage_spravne1a = round((spravne1a/36)*100)
    percentage_spravne1b = round((spravne1b/36)*100)
    percentage_spravne1c = round((spravne1c/36)*100)

    if spravne1a+spatne1a == 0:
        uspesnost_a = 0
    else:
        uspesnost_a = round((spravne1a/(spravne1a+spatne1a))*100)

    if spravne1b+spatne1b == 0:
        uspesnost_b = 0
    else:
        uspesnost_b = round((spravne1b/(spravne1b+spatne1b))*100)

    if spravne1c+spatne1c == 0:
        uspesnost_c = 0
    else:
        uspesnost_c = round((spravne1c/(spravne1c+spatne1c))*100)

    
    
    

    percentage_spatne1a = round((spatne1a/36)*100)
    percentage_spatne1b = round((spatne1b/36)*100)
    percentage_spatne1c = round((spatne1c/36)*100)

    return render_template("prehled_kvizu.html", 
        spravne1a=spravne1a,
        spravne1b=spravne1b, 
        spravne1c=spravne1c, 
        spatne1a=spatne1a,
        spatne1b=spatne1b,
        spatne1c=spatne1c,
        percentage_spravne1a=percentage_spravne1a, 
        percentage_spravne1b=percentage_spravne1b, 
        percentage_spravne1c=percentage_spravne1c,
        percentage_spatne1a=percentage_spatne1a,
        percentage_spatne1b=percentage_spatne1b,
        percentage_spatne1c=percentage_spatne1c,
        uspesnost_a=uspesnost_a,
        uspesnost_b=uspesnost_b,
        uspesnost_c=uspesnost_c)

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

        if hlas.voted == 1:
            return render_template("kod_vyuzit.html")

        hlas.voted = 1
        

        if str(QUESTION_DATA["spravnaOdpoved"]) == odpoved:
            odpovedEntry = Odpovedi(odpoved=QUESTION_DATA["odpoved" + str(odpoved)], otazka=QUESTION_DATA["otazka"], trida=request.form["trida"], jmeno="Anonymní", kod=kod, body_zapsany=0, spravne=1)

            db.session.add(odpovedEntry)
            db.session.commit()
            return render_template("post_kviz_spravne.html", trida=request.form["trida"], spravnaOdpoved=QUESTION_DATA["odpoved" + str(QUESTION_DATA["spravnaOdpoved"])], kod=kod)
        else:
            odpovedEntry = Odpovedi(odpoved=QUESTION_DATA["odpoved" + str(odpoved)], otazka=QUESTION_DATA["otazka"], trida=request.form["trida"], jmeno="Anonymní", kod=kod, body_zapsany=0, spravne=0)
            
            db.session.add(odpovedEntry)
            db.session.commit()
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