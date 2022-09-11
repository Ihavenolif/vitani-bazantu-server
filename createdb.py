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

class Odpovedi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trida = db.Column(db.String(256))
    otazka = db.Column(db.String(256))
    odpoved = db.Column(db.String(256))
    jmeno = db.Column(db.String(256))
    kod = db.Column(db.String(256))

db.create_all()