from typing import List
from models.Receita import Receita
from util.Database import Database


class ReceitaRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS receita (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            tempoPreparo INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            rendimento INTEGER NOT NULL)
            
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conexao.commit()
        conexao.close()
        return tableCreated
    
    @classmethod
    def inserir(cls, receita: Receita) -> Receita:        
        sql = "INSERT INTO receita (titulo, tempoPreparo, rendimento, descricao) VALUES (?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (receita.titulo, receita.tempoPreparo, receita.rendimento, receita.descricao))
        if (resultado.rowcount > 0):            
            receita.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return receita
    
    @classmethod
    def alterar(cls, receita: Receita) -> Receita:
        sql = "UPDATE receita SET titulo=? tempoPreparo=? rendimento=? descricao=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (receita.titulo, receita.tempoPreparo, receita.rendimento, receita.descricao))
        if (resultado.rowcount > 0):            
            conexao.commit()
            conexao.close()
            return receita
        else: 
            conexao.close()
            return None

        
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM receita WHERE id=?"
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
    def obterTodos(cls) -> List[Receita]:
        sql = "SELECT receita.id, receita.titulo, receita.tempoPreparo, receita.rendimento, receita.descricao FROM receita"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Receita(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Receita]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT id, titulo, tempoPreparo, rendimento, descricao FROM receita ORDER BY titulo LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [Receita(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterTotalPaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM receita) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])

    @classmethod
    def obterPorId(cls, id: int) -> Receita:
        sql = "SELECT receita.id, receita.titulo, receita.tempoPreparo, receita.rendimento, receita.descricao FROM receita WHERE receita.id = ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        objeto = Receita(*resultado)
        return objeto
