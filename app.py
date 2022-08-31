from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/podrobnosti")
def podrobnosti():
    return render_template("podrobnosti.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")