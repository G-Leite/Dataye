from flask import Flask, request, jsonify
from adapters.xposedornot_adapter import XposedOrNotAdapter
from adapters.sqlite_repository import SQLiteRepository
from casos_de_uso.consultar_email import ConsultarEmailUseCase
from flask import render_template 
import re
from datetime import datetime, timedelta

app = Flask(__name__)

fonte = XposedOrNotAdapter()
repositorio = SQLiteRepository()
use_case = ConsultarEmailUseCase(fonte, repositorio)

#regex de validação de email 
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

ultimas_consultas = {} # ip e data
INTERVALO_MINIMO = timedelta(seconds=5)

@app.route("/consultar", methods=["POST"])
def consultar():
    dados = request.get_json(silent=True) or {}
    email = dados.get("email", "").strip()
    ip = request.remote_addr
    agora = datetime.now()

    #evita abuso da API e flood
    if ip in ultimas_consultas and agora - ultimas_consultas[ip] < INTERVALO_MINIMO:
        return jsonify({"erro": "aguarde antes de consultar de novo"}), 429
    
    ultimas_consultas[ip] = agora

    # executa a validação de email
    if not email or not EMAIL_REGEX.match(email):
        return jsonify({"erro": "campo 'email' é obrigatório"}), 400

    consulta = use_case.executar(email)

   
    return jsonify({
        "email": consulta.email,
        "foi_vazado": consulta.foi_vazado,
        "vazamentos": [
            {"fonte": v.fonte, "nome": v.nome} for v in consulta.vazamentos
        ]
    })

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False)