from pydantic import BaseModel 
from models.Usuario import Usuario
from models.Postagem import Postagem

class CurtidaPostagem:
  usuario: Usuario
  postagem: Postagem
  positivo: bool