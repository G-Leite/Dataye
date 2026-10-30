from datetime import date
from domain.portas import BreachSourcePort, RepositoryPort
from domain.entidades import Consulta

class ConsultarEmailUseCase:
    def __init__(self, fonte: BreachSourcePort, repositorio: RepositoryPort):
        self.fonte = fonte
        self.repositorio = repositorio

    def executar(self, email: str) -> Consulta:
        vazamentos = self.fonte.buscar(email)

        consulta = Consulta(
            email=email,
            data_consulta=date.today(),
            vazamentos=vazamentos
        )

        self.repositorio.salvar(consulta)
        return consulta