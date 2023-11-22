from pydantic import BaseModel 
from models import Usuario
from models import Receita
from models.Receita import Receita

class CurtidaReceita(BaseModel):
  usuario: Usuario
  receita: Receita
  positivo: bool