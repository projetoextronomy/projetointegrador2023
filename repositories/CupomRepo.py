# repositories/AlunoRepo.py
from typing import List
from models.Cupom import Cupom
from util.Database import Database

class CupomRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS cupom (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor INTEGER NOT NULL,
            condicao TEXT NOT NULL,
            dt_inicio DATE NOT NULL,
            dt_fim DATE NOT NULL,
            hr_inicio TIME NOT NULL,
            hr_fim TIME NOT NULL)
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conexao.commit()
        conexao.close()
        return tableCreated
    
    @classmethod
    def inserir(cls, cupom: Cupom) -> Cupom:
        sql = "INSERT INTO cupom (nome, valor, condicao, dt_inicio, dt_fim, hr_inicio, hr_fim) VALUES (?, ?, ?, ?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (cupom.nome, cupom.valor, cupom.condicao, cupom.dt_inicio, cupom.dt_fim, cupom.hr_inicio, cupom.hr_fim))
        if (resultado.rowcount > 0):            
            cupom.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return cupom
    
    @classmethod
    def alterar(cls, cupom: Cupom) -> Cupom:
        sql = "UPDATE cupom SET nome=?, valor=?, condicao=?, dt_inicio=?, dt_fim=?, hr_inicio=?, hr_fim=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (cupom.nome, cupom.valor, cupom.condicao, cupom.dt_inicio, cupom.dt_fim, cupom.hr_inicio, cupom.hr_fim))
        if (resultado.rowcount > 0):            
            conexao.commit()
            conexao.close()
            return cupom
        else: 
            conexao.close()
            return None
        
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM cupom WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, ))
        if (resultado.rowcount > 0):
            conexao.commit()
            conexao.close()
            return True
        else: 
            conexao.close()
            return False
        
    @classmethod
    def obterTodos(cls) -> List[Cupom]:
        sql = "SELECT cupom.id, cupom.nome, cupom.valor, cupom.condicao, cupom.dt_inicio, cupom.dt_fim, cupom.hr_inicio, cupom.hr_fim FROM cupom ORDER BY cupom.dt_inicio"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Cupom(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Cupom]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT cupom.id, cupom.nome, cupom.valor, cupom.condicao, cupom.dt_inicio, cupom.dt_fim, cupom.hr_inicio, cupom.hr_fim FROM cupom ORDER BY cupom.dt_inicio LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [Cupom(*x) for x in resultado]
        return objetos

    @classmethod
    def obterTotalPaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM cupom) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])
    
    @classmethod
    def obterPorId(cls, id: int) -> Cupom:
        sql = "SELECT cupom.id, cupom.nome, cupom.valor, cupom.condicao, cupom.dt_inicio, cupom.dt_fim, cupom.hr_inicio, cupom.hr_fim FROM cupom WHERE cupom.id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchone()

        if resultado:
            # Desempacotar o resultado e criar uma instância de Cupom
            objeto = Cupom(*resultado)
            return objeto

