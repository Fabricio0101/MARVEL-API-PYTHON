from flask import Flask, render_template
import requests
from flask.globals import request
from models.heroesmarvel import Heroesmarvel
import hashlib
from time import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buscar", methods = ["GET", "post"])
def buscar():
    heroes = Heroesmarvel(request.form["nome"].lower(),"")
    try:
        public_key = "56c01993120d08033cfc59a1d2fc65f5"
        private_key = "029d750b7c91062d9d14235efc1006dc60ef947f"
        ts = str(int(time()))
        
        limit = 10
        hashing = hashlib.md5(ts.encode()+private_key.encode()+public_key.encode())
        result = requests.get(f"http://gateway.marvel.com/v1/public/characters?hash={hashing.hexdigest()}&apikey={public_key}&ts={ts}&limit={limit}&nameStartsWith={heroes.nome}")
        heroes.foto = result
    except:
        return "Heroi não encontrado"    
    return render_template("index.html", 
    nome = heroes.nome,
    foto = heroes.foto
    )


if __name__ == "__main__":
    app.run(debug=True)