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
from copypasta_3 import copypasta_3
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

LADKA_QUOTES = [
    "Pokud by praskla Lipenská přehrada, Český Krumlov by to nepřežil tak, jak to přežil",
    "Bakterie se rozmnoží v teplé pitné vodě v boileru, jo?",
    "Před 8000 lety ušel vlastně velbloud 640 km za 2 dny. tedy Parní lokomotiva jede 160 km/h.",
    "Evropa patří k stabilním státům. Já státy neporovnávám, jenom je rozděluju.",
    "Krajina je trojrozměrná část krajinné sféry obsahující části jednotlivých geosfér. Tvoří ji prvky přírodní a antropogenní.",
    "Těžba hnědého uhlí je proces, kterým se získává hnědé uhlí z půdy. Hnědé uhlí je jedním z samozřejmě nejdůležitějších surovin tedy pro průmysl a tedy energetiku.",
    "V Americe nebyla žádná světová válka.",
    "Chceš se globalizovat? jsi ráda globalizována?",
    "Měli ve viktoriánské Anglii těstoviny? Samozřejmě když se našly tedy zkamenělé v prosím vás Číně jo? tak to asi mít budou.",
    "Přírodní krajina má charakter tedy přírodní krajiny.",
    "Italové se stěhovali do Ameriky a jiných částí Evropy.",
    "Delfíni žijí v Dunaji, v deltě.",
    "Sám si rozhoduje o vnitřních záležitostech a žádný jiný stát nemá, nebo nesmí, nemůže zasahovat do tady toho dalšího. Takže to je tedy ta suverenita?",
    "No Ukrajina ukrajinská vláda nemá svrchovanou moc nad krymem. Nemá svrchovanou moc nad tou doněckou a luhanskou oblastí",
    "Vlastně v té v té východní části Ukrajiny jo? Tam prostě to nefunguje podle těch vlastně těch zákonů té úpravy",
    "Kosovo má err nějakou vládu, nebo ne? Má armádu. Jo a ty mají teda jako nad sebou?",
    "Takže podle tohoto hlediska si ty státy rozředíme jo podle svrchované a nezávislé",
    "Judaismus pozor není světovým náboženstvím. Judaismus je tím národním. Národní náboženství vlastně je.",
    "Demokratický nebo? To tady přesně tak. Takže nebo jestli jsou monarchie nebo. Prezident republiky, takže podle státní zřízení monarchie republika podle ekonomické vyspělosti, vyspělé či rozvojové státy nějak pojmenovat",
    "Takže rusko 17 milionů kilometrů čtverečních a dále je přes 10 milionů kilometrů čtverečních Kanada. Jo další státy jako Čína a Spojené Státy jo ty mají přibližně rozlohu jako Evropa.",
    "Vlastně ty státy, když se porovnávají mezi sebou podle té ekonomické vyspělosti? Čili to porovnávám tahleta HDP přesně tak HDP, ale HDP má 2 rozměry.",
    "To znamená jako nominální to absolutní to maximum, co prostě co je ta hodnota toho, co ty státy vyrobí nebo poskytnou služeb",
    "Takže stupeň ekonomické vyspělosti směsi. A takže nejdříve se budeme zabývat tím vlastně dělením státu podle toho mezinárodně. Z právního postavení.",
    "Mluvili jsme o tom, že tedy je ten stát nezávislý, nezávislý stát, je stát svrchovaný. Suverénním příkladem může být první mezi nejvyspělejšími státy světa Kanada a vymezit ten.",
    "Tedy ten nezávislý stát i základní politickou biografická jednotka má vlastní území, má vlastní vládu a ale má také obecně mezinárodně právní uznání",
    "V současné době 194 států asi na té politické mapě světa, ale každý zdroj vám řekne trošičku něco jiného, protože ty státy jako služba mají trošičku jiný stav.",
    "Nebudeme dělit, ale řekneme si něco o nejstarší státech, které fungují těch obětí. Díky těm hranicím fungují až do současnosti. Tak nejstarší stát na světě mezi nejstarší státy světa na světě patří.",
    "V jiných samozřejmě hranicích, než než v současnosti v Evropě je nejstarší státem je Dánsko, Švédsko, Francie. ", 
    "V Africe nejnovější stát. Vznik. Tady ani nemám ještě ani na tý mapě. Rok 2011 vznikl. Jižní Súdán. Jo jižní Súdán 2011. ", 
    "Dále v Evropě máme nějaké vlastně území, které jsou potenciálně mohou vzniknout jako samostatné státy. ", 
    "Máme areál nějaký stát, který se nejspíš vlastně bude, bude rozpadat, na část státu, na nějaké územní jednotky menší. ", 
    "No ve Španělsku samozřejmě. Referendum, kdy tedy Katalánci, Katalánsko, Katalánci se vyslovili pro to, že chtějí být samostatným státem, když se chtějí prostě odtrhnout od Španělska ", 
    "Tak, takže ta závislá území ty závislé oblasti mohou mít název různý jo, ale jsou to politicky nesamostatná území s omezenou suverenitu. ", 
    "Vlastníkem je nezávislý stát, který vlastně je zastupován na tom území. ",
    "Guvernér samozřejmě zastupuje, ale královnu jo a takže to je zase něco něco jiného. ", 
    "Jsou to zámořské departmenty Francie. V ve francouzské guyaně mají euro jo, když jsou to vlastně součástí součástí Francie. ", 
    "V současné době už mají samozřejmě určitou samostatnost. Určitou autonomii mají i vlastní vládu, která komunikuje samozřejmě s tou vládou. ", 
    "Tam kdybychom se podívali na mapu, tak tam máme ty menší ostrůvky, které jsou britské či francouzské a většinou nevelké. ", 
    "Jak jsem řekla malý počet obyvatel. Nepatrný hospodářský potenciál. Vyjádřil jsem vždycky, že chtějí být v rámci Dánska, protože mají nižší ten hospodářský potenciál jo a daří se jim samozřejmě v rámci toho demokratického státu. ", 
    "Odsouhlasili, že chtějí být ale kongres spojených států amerických to nikdy neodsouhlasil jo, aby byly, aby měli stejný status jako třeba Aljaška nebo jako havajské ostrovy. ",
    "Kdo jel lanovkou na Sněžku, ostuda.",
    "Vemte si pevnou obuv, ať tam nejste za kašpárky.",
    "Někdy se změní počasí a musí v těch pantoflíčkách jít zase dolů.",
    "Né králíci, ale Králíky.",
    "Na Sněžníku bývá… Sníh výborně.",
    "Já vím, že se zdá, že vás to nezajímá. To se nezdá…",
    "Chlapi neumí ani rozlišovat barvy.",
    "Ledovcové údolí bylo samozřejmě vymodelováno ledovcem.",
    "Broumovská vrchovina je v Broumovském výběžku.",
]

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
    f = open("navstevnost_log.txt", "a")
    f.write("/clashofclans" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
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
            if entry.pocet_coinu > 769: continue
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

        if int(request.form["pocetCoinu"]) > 769:
            with open("./ivanman_cheaters.txt", "a") as result_file:
                #WIN,POCETBODU,POCETCOINU,CAS,MAPA,TIMESTAMP
                result_file.write(request.form["win"] + "," + request.form["pocetBodu"] + "," + request.form["pocetCoinu"] + "," + request.form["cas"] + "," + request.form["map"] + "," + str(datetime.timestamp(datetime.now())) + "\n")
                result_file.close()
            return render_template(
                "ivanman/post_game_exploited.html", 
                id=request.form["id"], 
                win=1,
                pocetBodu=request.form["pocetBodu"],
                pocetCoinu=request.form["pocetCoinu"],
                cas=request.form["cas"],
                list=sendable_list,
                map=request.form["map"]
            )

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
        if entry.pocet_coinu > 769: continue
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

@app.route("/ladkaguesser", methods=["GET", "POST"])
def ladkaguesser():
    if(request.method == "GET"):
        f = open("navstevnost_log.txt", "a")
        f.write("/ladkaguesser" + "," + str(datetime.timestamp(datetime.now())) + "\n")
        f.close()
        return render_template("ladka_guesser.html")
    
    retval = {
        "isFromAI": False,
        "value": ""
    }

    retval["isFromAI"] = random.choice((True, False))

    if not retval["isFromAI"]:
        retval["value"] = random.choice(LADKA_QUOTES)
        return json.dumps(retval)

    response = openai.Completion.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = "Napiš jednu nebo dvě krátké věty v češtině na téma " + LADKA_VALUES[f"{random.randint(1, len(LADKA_VALUES))}"] + ". ",
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

    retval["value"] = final_text
    return json.dumps(retval)

@app.route("/ladkaguesser_data", methods=["POST"])
def ladkaguesser_data():
    print("kokot")
    with open("ladkaguesser_data.csv", "a") as question_file:
        question_value = request.json['value'].replace('\n', ' ')
        question_file.write(f"{request.json['pointCount']};{request.json['wasAI']};{question_value}\n")
        question_file.close()
    
    return "ok"

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

@app.route("/copypasta_3")
def copypasta_3_route():
    f = open("navstevnost_log.txt", "a")
    f.write("/copypasta_3" + "," + str(datetime.timestamp(datetime.now())) + "\n")
    f.close()
    return render_template("copypasta.html", pasta=copypasta_3())

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