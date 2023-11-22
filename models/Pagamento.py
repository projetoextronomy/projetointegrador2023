from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Pagamento:
  id: int
  nome: str
  sobrenome: str
  email: str
  endereco: str
  pais: str
  estado: str
  cep: str
  modo: str
  nome_Titular: Optional[str] = None
  numero_Cartao: Optional[int] = None
  data_Expiracao: Optional[date] = None
  cvv: Optional[int] = None
  parcela: Optional[int] = None