# models/Aluno.py
from dataclasses import dataclass
from datetime import date, time

@dataclass
class Cupom():
    id: int
    nome: str
    valor: float
    condicao: str
    dt_inicio: date
    dt_fim: date
    hr_inicio: time
    hr_fim: time