from dataclasses import dataclass
from datetime import datetime

@dataclass
class Postagem():
  id: int
  conteudo: str  
  usuario: int
  curtida: int = 0
  deslike: int = 0
  data_hora: datetime = None
  nome_autor: str = None
  