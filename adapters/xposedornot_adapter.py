import requests
from datetime import date
from domain.portas import BreachSourcePort
from domain.entidades import Vazamento

class XposedOrNotAdapter (BreachSourcePort):
    BASE_URL = "https://api.xposedornot.com/v1/check-email"

    def buscar(self, email: str) -> list[Vazamento]:
        resp = requests.get (f"{self.BASE_URL}/{email}", timeout = 10)
        print("STATUS:", resp.status_code)
        print("EMAIL ENVIADO:", email)

        if resp.status_code == 404:
            return [] # sem vazamento, API da 404 quando nao acha nada
        
        resp.raise_for_status() # erro se der 4xx ou 5xx
        dados = resp.json()
        print("RESPOSTA CRUA:", dados)

        nomes_vazamentos = dados.get("breaches", [[]])[0] # lista aninhada de vazamentos
        return [
            Vazamento(fonte = "XposedOrNot", nome = nome, data_vazamento = None)
            for nome in nomes_vazamentos
        ]