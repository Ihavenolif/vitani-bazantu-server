import random
import string
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

def generate_random_password(length):
    characters = list(string.digits + "abcdef")

	## shuffling the characters
    random.shuffle(characters)
	
	## picking random characters from the list
    password = []
    for i in range(length):
        password.append(random.choice(characters))

	## shuffling the resultant password
    random.shuffle(password)

	## converting the list to string
	## printing the list
    return "".join(password)

f = open("qrcode_url_list.txt", "a")
f.write("1.A\n\n")

for i in range(36):
    hlas = Hlasy()
    hlas.trida = "1.A"
    kod = generate_random_password(16)
    hlas.kod = kod
    hlas.voted = 0

    f.write("http://www.gvnqrkod.cz/kviz?kod=" + kod + "\n")

    db.session.add(hlas)
    db.session.commit()

f.write("\n 1.B\n\n")

for i in range(36):
    hlas = Hlasy()
    hlas.trida = "1.B"
    kod = generate_random_password(16)
    hlas.kod = kod
    hlas.voted = 0

    f.write("http://www.gvnqrkod.cz/kviz?kod=" + kod + "\n")

    db.session.add(hlas)
    db.session.commit()

f.write("\n 1.C\n\n")

for i in range(36):
    hlas = Hlasy()
    hlas.trida = "1.C"
    kod = generate_random_password(16)
    hlas.kod = kod
    hlas.voted = 0

    f.write("http://www.gvnqrkod.cz/kviz?kod=" + kod + "\n")

    db.session.add(hlas)
    db.session.commit()

f.close()