# adapters/sqlite_repository.py
import sqlite3
from datetime import date
from domain.portas import RepositoryPort
from domain.entidades import Consulta, Vazamento

class SQLiteRepository(RepositoryPort):
    def __init__(self, caminho_db: str = "vazamentos.db"):
        self.caminho_db = caminho_db
        self._criar_tabelas()

    def _criar_tabelas(self):
        with sqlite3.connect(self.caminho_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS consultas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    data_consulta TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vazamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    consulta_id INTEGER NOT NULL,
                    fonte TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    FOREIGN KEY (consulta_id) REFERENCES consultas(id)
                )
            """)

    def salvar(self, consulta: Consulta) -> None:
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.execute(
                "INSERT INTO consultas (email, data_consulta) VALUES (?, ?)",
                (consulta.email, consulta.data_consulta.isoformat())
            )
            consulta_id = cursor.lastrowid
            for v in consulta.vazamentos:
                conn.execute(
                    "INSERT INTO vazamentos (consulta_id, fonte, nome) VALUES (?, ?, ?)",
                    (consulta_id, v.fonte, v.nome)
                )

    def buscar_historico(self, email: str) -> list[Consulta]:
        with sqlite3.connect(self.caminho_db) as conn:
            conn.row_factory = sqlite3.Row
            linhas = conn.execute(
                "SELECT * FROM consultas WHERE email = ? ORDER BY data_consulta DESC",
                (email,)
            ).fetchall()

            resultado = []
            for linha in linhas:
                vazamentos_linhas = conn.execute(
                    "SELECT fonte, nome FROM vazamentos WHERE consulta_id = ?",
                    (linha["id"],)
                ).fetchall()
                vazamentos = [Vazamento(fonte=v["fonte"], nome=v["nome"], data_vazamento=None) for v in vazamentos_linhas]
                resultado.append(Consulta(
                    email=linha["email"],
                    data_consulta=date.fromisoformat(linha["data_consulta"]),
                    vazamentos=vazamentos
                ))
            return resultado