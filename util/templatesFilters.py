# util/templateFilters.py
from datetime import datetime, time

def formatarData(dataStr: str) -> str:
    if dataStr is None:
        return ""
    ano, mes, dia = dataStr.split('-')
    return f"{dia}/{mes}/{ano}"

def formatarData2(dataStr):
    if dataStr is None:
        return ""

    if isinstance(dataStr, str):
        # If the input is a string, split it and format the date
        ano, mes, dia = dataStr.split('-')
        return f"{dia}/{mes}/{ano}"
    elif isinstance(dataStr, datetime):
        # If the input is a datetime object, format the date accordingly
        return dataStr.strftime("%d/%m/%Y")
    else:
        return "Invalid input format"

def capitalizar_nome_proprio(nome: str) -> str:
    nome = nome.lower()
    ignoradas = ['de', 'da', 'do', 'di', 'das', 'com', 'dos']    
    palavras = nome.split()    
    palavras_capitalizadas = [
        palavra.capitalize() if palavra.lower() not in ignoradas else palavra.lower()
        for palavra in palavras
    ]
    return ' '.join(palavras_capitalizadas)

def formatarHora(hora: time) -> str:
    return hora.strftime('%H:%M:%S')

def formatarIdParaImagem(id: str) -> str:
    if not id:
        return ""
    formatado = f"{id:0{4}}"
    return formatado
