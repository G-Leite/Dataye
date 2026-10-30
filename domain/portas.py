from abc import ABC, abstractmethod 
from domain.entidades import Vazamento, Consulta 

class BreachSourcePort(ABC):
    # faz conexão com qualquer fonte de dados de vazamento

    @abstractmethod
    def buscar(self,email: str) -> list[Vazamento]:
        ...

class RepositoryPort(ABC):
    #persistência do histórico de consulta

    @abstractmethod
    def salvar(self, consulta: Consulta) -> None:
        ...
    
    @abstractmethod
    def buscar_historico(self, email: str) -> list[Consulta]:
        ...

