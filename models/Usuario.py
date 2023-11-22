from dataclasses import dataclass
from typing import List, Optional
from models.PreferenciaAlimentar import PreferenciaAlimentar
from datetime import date
from dataclasses import dataclass


@dataclass
class Usuario:
  id: int
  nome: str = ""
  email: str = ""
  senha: str = ""
  endereco: Optional[str] = ""
  dataNascimento: Optional[str] = ""
  sexo: Optional[str] = ""
  semgluten: Optional[bool] = None
  vegetariano: Optional[bool] = None
  lowcarb: Optional[bool] = None
  semfrutosdomar: Optional[bool] = None
  semlactose: Optional[bool] = None
  vegano: Optional[bool] = None
  integral: Optional[bool] = None
  semleite: Optional[bool] = None
  semacucar: Optional[bool] = None
  semovo: Optional[bool] = None
  semcacau: Optional[bool] = None
  organico: Optional[bool] = None
  token: Optional[str] = ""
  admin: Optional[bool] = False