from dataclasses import dataclass, field
from datetime import date

@dataclass
class Vazamento:
    fonte: str  #fonte dos vazamentos, HIBP, DesHashed, etc
    nome: str   # fonte do vazamento
    data_vazamento: date | None
    campos_expostos: list[str] = field(default_factory=list) # ex: ["email", "senha"]

@dataclass
class Consulta:
    email: str
    data_consulta: date
    vazamentos: list[Vazamento] = field(default_factory=list)

    @property
    def foi_vazado(self) -> bool:
        return len(self.vazamentos) > 0

