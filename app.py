import json
import os
import math
import logging
import html
import re
import openai
import random
from copypasta import copypasta
from copypasta_2 import copypasta_2
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import func, Column, Integer, String, Float
from datetime import datetime

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='log.log')

PASSWORD = os.getenv("PASSWORD")
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
CORS(app)

db = SQLAlchemy(app)

LADKA_VALUES = {
    "1": "Asie",
    "2": "Česká republika",
    "3": "Evropa",
    "4": "Evropská Unie",
    "5": "globalizace",
    "6": "HDP x DPH",
    "7": "kontinent",
    "8": "Latinská amerika",
    "9": "Jaderné elektrárny v České republice",
    "10": "obilnice světa",
    "11": "podnebná pásma",
    "12": "půda",
    "13": "roční období",
    "14": "Těžba černého uhlí",
    "15": "Těžba hnědého uhlí",
    "16": "udržitelný rozvoj",
    "17": "vesmír",
    
}

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

class IvanmanDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jmeno = db.Column(db.String(256))
    pocet_bodu = db.Column(db.Float())
    pocet_coinu = db.Column(db.Integer)
    cas = db.Column(db.Integer)

@app.route("/clashofclans")
def clashofclans():
    return render_template("clashofclans.html")

@app.route("/timelapse", methods=["GET", "POST"])
def timelapse():
    with open("parsed_drawing_data.json") as map_file:
        map_text = map_file.read()
        map_file.close()
    
    if(request.method == "GET"):
        return render_template("timelapse.html")

    return map_text

@app.route("/ivanman", methods=["GET", "POST"])
def ivanman():
    if(request.method == "GET"):
        try:
            map = request.args["map"]
        except:
            map = "autoselect"

        imgs_to_send = []

        imgs_to_send.append(random.randint(1,22))

        while len(imgs_to_send) < 6:
            roll = random.randint(1,22)
            if not (roll in imgs_to_send):
                imgs_to_send.append(roll)

        last_id = db.session.query(func.max(IvanmanDatabase.id)).first()[0]

        f = open("navstevnost_log.txt", "a")
        f.write("/ivanman" + "," + str(datetime.timestamp(datetime.now())) + "\n")
        f.close()

        return render_template("ivanman/ivanman.html", id=last_id+1, imglist=imgs_to_send, ucitel0=imgs_to_send[0], ucitel1=imgs_to_send[1], ucitel2=imgs_to_send[2], ucitel3=imgs_to_send[3], ucitel4=imgs_to_send[4], ucitel5=imgs_to_send[5], map=map)

    try:
        if request.json["request"] == "start_game":
            entry = IvanmanDatabase(id=request.json["id"])
            db.session.add(entry)
            db.session.commit()
            return ""
    except:
        () #does nothing

    if request.form["request"] == "post_game":
        entries = IvanmanDatabase.query.all()

        list = []

        for entry in entries:
            temp = {}
            if not entry.pocet_bodu: continue
            temp["pocetBodu"] = entry.pocet_bodu
            temp["pocetCoinu"] = entry.pocet_coinu
            temp["cas"] = entry.cas
            temp["jmeno"] = entry.jmeno
            list.append(temp)
    
        with open("./ivanman_results.txt", "a") as result_file:
            #WIN,POCETBODU,POCETCOINU,CAS,MAPA
            result_file.write(request.form["win"] + "," + request.form["pocetBodu"] + "," + request.form["pocetCoinu"] + "," + request.form["cas"] + "," + request.form["map"] + "\n")
            result_file.close()

        new_list = sorted(list, key=lambda d: d["pocetBodu"])
        new_list.reverse()

        sendable_list = new_list[0:10]

        if request.form["win"] == "1":
            return render_template(
                "ivanman/post_game_win.html", 
                id=request.form["id"], 
                win=1,
                pocetBodu=request.form["pocetBodu"],
                pocetCoinu=request.form["pocetCoinu"],
                cas=request.form["cas"],
                list=sendable_list,
                map=request.form["map"]
            )
        else:
            return render_template(
                "ivanman/post_game_loss.html", 
                id=request.form["id"], 
                win=0,
                pocetBodu=request.form["pocetBodu"],
                pocetCoinu=request.form["pocetCoinu"],
                cas=request.form["cas"],
                list=sendable_list,
                ucitel=request.form["ucitel"],
                map=request.form["map"]
            )

    if request.form["request"] == "point_submit":
        entry = IvanmanDatabase.query.filter_by(id=request.form["id"]).first()
        jmeno = request.form["jmeno"]
        entry.jmeno = html.escape(jmeno)
        entry.pocet_bodu = request.form["pocetBodu"]
        entry.pocet_coinu = request.form["pocetCoinu"]
        entry.cas = request.form["cas"]
        db.session.commit()
        return "<script>window.location=\"/ivanman/leaderboard\"</script>"

@app.route("/ivanman_welcome")
def ivanman_welcome():
    f = open("navstevnost_log.txt", "a")
    f.write("/ivanman/welcome" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
    return render_template("ivanman/welcome.html")

@app.route("/ivanman/leaderboard")
def ivanman_leaderboard():
    entries = IvanmanDatabase.query.all()

    list = []

    for entry in entries:
        temp = {}
        if not entry.pocet_bodu: continue
        temp["pocetBodu"] = entry.pocet_bodu
        temp["pocetCoinu"] = entry.pocet_coinu
        temp["cas"] = entry.cas
        temp["jmeno"] = entry.jmeno
        list.append(temp)
    
    new_list = sorted(list, key=lambda d: d["pocetBodu"])
    new_list.reverse()

    sendable_list = new_list[0:10]

    print(sendable_list)

    return render_template("/ivanman/leaderboard.html", list=sendable_list)

@app.route("/map_gen", methods=["GET", "POST"])
def map_gen():
    with open("result_json.json") as map_file:
        map_text = map_file.read()
        map_file.close()
    
    if(request.method == "GET"):
        return render_template("map_image_generator.html", map=map_text)
    
    return map_text

@app.route("/archiv")
def archiv():
    f = open("navstevnost_log.txt", "a")
    f.write("/archiv" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
    return render_template("archiv/archiv.html")

@app.route("/faq")
def faq():
    f = open("navstevnost_log.txt", "a")
    f.write("/faq" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
    return render_template("faq.html")

@app.route("/archiv/vitani_novacku")
def vitani():
    f = open("navstevnost_log.txt", "a")
    f.write("/archiv/vitani_novacku" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
    return render_template("archiv/vitani_novacku.html")

@app.route("/archiv/gymplace")
def gymplace_archiv():
    f = open("navstevnost_log.txt", "a")
    f.write("/archiv/gymplace" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
    return render_template("archiv/gymplace.html")

@app.route("/gymplace_welcome")
def rplace_welcome():
    f = open("navstevnost_log.txt", "a")
    f.write("/gymplace_welcome" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
    return render_template("rplace_welcome.html")

@app.route("/gymplace")
def rplace():
    f = open("navstevnost_log.txt", "a")
    f.write("/gymplace" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
    return render_template("rplace.html")

@app.route("/gymplace_content")
def rplace_content():
    return render_template("rplace_content.html")

@app.route("/gymplace_menu")
def rplace_menu():
    return render_template("rplace_menu.html")

@app.route("/gymplace_chat")
def rplace_chat():
    return render_template("rplace_chat.html")

@app.route("/jestlitohlenekdouhadnetakjegej")
def body_realtime():
    return render_template("body_realtime.html")

@app.route("/jestlitohlenekdouhadnetakjekokot")
def body_realtime_zapis():
    return render_template("realtime_zapis_bodu.html")

@app.route("/tricetminutwellspent")
def livechat():
    return render_template("livechat.html")

@app.route("/")
def index():
    f = open("navstevnost_log.txt", "a")
    f.write("/" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
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

@app.route("/send_question", methods=["POST"])
def send_question():
    print("kokot")
    with open("question_log.txt", "a") as question_file:
        question_file.write(request.json["otazka"] + "\n")
        question_file.close()
    
    return "ok"

@app.route("/navrhy_pro_ladku", methods=["POST"])
def navrhy_pro_ladku():
    print("kokot")
    with open("navrhy_pro_ladku.txt", "a") as question_file:
        question_file.write(request.json["otazka"] + "\n")
        question_file.close()
    
    return "ok"

@app.route("/otazky_z_coc", methods=["POST"])
def otazky_z_coc():
    print("kokot")
    with open("otazky_z_coc.txt", "a") as question_file:
        question_file.write(request.json["otazka"] + "\n")
        question_file.close()
    
    return "ok"

@app.route("/ucitel_zemepisu", methods=["GET", "POST"])
def ladka():
    if(request.method == "GET"):
        f = open("navstevnost_log.txt", "a")
        f.write("/ucitel_zemepisu" + "," + str(datetime.timestamp(datetime.now())) + "\n")
        f.close()
        return render_template("ladka_generator.html")

    response = openai.Completion.create(
        model = "text-davinci-002",
        prompt = "Napiš prezentaci v češtině na téma " + LADKA_VALUES[request.json["option"]] + ".",
        temperature=0.7,
        max_tokens=500
    )
    response_text = response.get("choices")[0].get("text")

    regex_list = re.findall("(\. [A-Z]\w+)", response_text)

    for x in regex_list:
        if random.random() < 0.2:
            word_after_whitespace = x.split(" ")[1]
            response_text = response_text.replace(x, " jo? " + word_after_whitespace)

    final_text = ""

    for x in response_text:
        slovo = ""
        roll = random.randint(0, 100)

        if roll < 13:
            slovo = "tedy"
        elif roll < 13+37:
            slovo = "vlastně"
        elif roll < 13+37+15:
            slovo = "samozřejmě"
        elif roll < 13+37+15+10:
            slovo = "prosimvás"
        else:
            slovo = "tak"
    
        if x == " " and random.random() < 0.15:
            final_text += " " + slovo + " "
        else:
            final_text += x

    with open("ladka_vyplody.txt", "a") as question_file:
        question_file.write(final_text + "\n\n\n")
        question_file.close()

    return final_text

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

@app.route("/copypasta")
def copypasta_route():
    f = open("navstevnost_log.txt", "a")
    f.write("/copypasta" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
    return render_template("copypasta.html", pasta=copypasta())

@app.route("/copypasta_2")
def copypasta_2_route():
    f = open("navstevnost_log.txt", "a")
    f.write("/copypasta_2" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
    return render_template("copypasta.html", pasta=copypasta_2())

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
    app.run(host="0.0.0.0", port="5000", debug=True)