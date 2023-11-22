from models.Usuario import Usuario
from models.Receita import Receita
from datetime import date
from datetime import time

class ComentarioReceita:
  id: int 
  texto: str
  hora: time
  data: date
  usuario: Usuario
  receita: Receita 
  
  