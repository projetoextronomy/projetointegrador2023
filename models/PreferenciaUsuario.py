from pydantic import BaseModel 
from models import Usuario
from models import PreferenciaAlimentar


class PreferenciaUsuario(BaseModel):
  preferencia: PreferenciaAlimentar
  usuario: Usuario