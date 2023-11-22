# repositories/AlunoRepo.py
from typing import List
from models.Postagem import Postagem
from util.Database import Database

class PostagemRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS postagem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conteudo TEXT NOT NULL,
            usuario INTEGER NOT NULL,
            curtida INTEGER,
            deslike INTEGER,
            data_hora DATETIME
            )
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conexao.commit()
        conexao.close()
        return tableCreated
    
    @classmethod
    def inserir(cls, postagem: Postagem) -> Postagem:
        sql = "INSERT INTO postagem (conteudo, usuario, curtida, deslike, data_hora) VALUES (?, ?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (postagem.conteudo, postagem.usuario, postagem.curtida, postagem.deslike, postagem.data_hora))
        if (resultado.rowcount > 0):            
            postagem.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return postagem
    
    @classmethod
    def alterar(cls, postagem: Postagem) -> Postagem:
        sql = "UPDATE postagem SET conteudo=?, usuario=?, curtida=?, deslike=? data_hora=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (postagem.conteudo, postagem.usuario, postagem.curtida, postagem.deslike, postagem.data_hora))
        if (resultado.rowcount > 0):            
            conexao.commit()
            conexao.close()
            return postagem
        else: 
            conexao.close()
            return None
        
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM postagem WHERE id=?"
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
    def obterTodos(cls) -> List[Postagem]:
        sql = "SELECT postagem.id, postagem.conteudo, postagem.usuario, postagem.curtida, postagem.deslike, postagem.data_hora, usuario.nome as nome_autor FROM postagem INNER JOIN usuario ON postagem.usuario = usuario.id ORDER BY postagem.data_hora DESC"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Postagem(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterPorAutor(cls, id_autor: int) -> List[Postagem]:
        sql = "SELECT postagem.id, postagem.conteudo, postagem.usuario, postagem.curtida, postagem.deslike, postagem.data_hora, usuario.nome as nome_autor FROM postagem INNER JOIN usuario ON postagem.usuario = usuario.id WHERE postagem.usuario = ? ORDER BY postagem.data_hora DESC"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id_autor, )).fetchall()
        objetos = [Postagem(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Postagem]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = f"SELECT postagem.id, postagem.conteudo, postagem.usuario, postagem.curtida, postagem.deslike, postagem.data_hora FROM postagem ORDER BY postagem.data_hora DESC LIMIT {inicio}, {tamanhoPagina}"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Postagem(*x) for x in resultado]
        return objetos


    @classmethod
    def obterTotalPaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM postagem) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])
    
    @classmethod
    def obterPorId(cls, id: int) -> Postagem:
        sql = "SELECT conteudo, usuario, curtida, deslike, data_hora FROM postagem WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        objeto = Postagem(*resultado)
        return objeto    