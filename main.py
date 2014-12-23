__author__ = 'Rui'

from flask import Flask

app = Flask(__name__)

URL = "http://app.metrolisboa.pt/status/estado_Linhas.php"


@app.route("/status")
def status():
    return "Ola"


if __name__ == "__main__":
    app.run()
