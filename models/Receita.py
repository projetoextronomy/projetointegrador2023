from dataclasses import dataclass

@dataclass
class Receita():
  id: int
  titulo: str = ""
  tempoPreparo: int = ""
  rendimento: int = ""
  descricao: str = ""
  # midia: str = ""
  #qntCurtida: int
  #idAutor: int
  #autor: Usuario