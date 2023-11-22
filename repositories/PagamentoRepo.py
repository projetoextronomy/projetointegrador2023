from typing import List
from models.Pagamento import Pagamento
from util.Database import Database

class PagamentoRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS pagamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            email TEXT NOT NULL,
            endereco TEXT NOT NULL,
            pais TEXT NOT NULL,
            estado TEXT NOT NULL,
            cep TEXT NOT NULL,
            modo TEXT NOT NULL, 
            nome_Titular TEXT,
            numero_Cartao INTEGER,
            data_Expiracao DATE,
            cvv INTEGER,
            parcela INTEGER)
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conexao.commit()
        conexao.close()
        return tableCreated
    
    @classmethod
    def inserir(cls, pagamento: Pagamento) -> Pagamento:
        sql = "INSERT INTO pagamento (nome, sobrenome, email, endereco, pais, estado, cep, modo, nome_Titular, numero_Cartao, data_Expiracao, cvv, parcela) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (pagamento.nome, pagamento.sobrenome, pagamento.email, pagamento.endereco, pagamento.pais, pagamento.estado, pagamento.cep, pagamento.modo, pagamento.nome_Titular, pagamento.numero_Cartao, pagamento.data_Expiracao, pagamento.cvv, pagamento.parcela))
        if (resultado.rowcount > 0):            
            pagamento.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return pagamento
    
    @classmethod
    def alterar(cls, pagamento: Pagamento) -> Pagamento:
        sql = "UPDATE pagamento SET nome=?, sobrenome=?, email=?, endereco=?, pais=?, estado=?, cep=?, modo=?, nome_Titular=?, numero_Cartao=?, data_Expiracao=?, cvv=?, parcela=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (pagamento.nome, pagamento.sobrenome, pagamento.email, pagamento.endereco, pagamento.pais, pagamento.estado, pagamento.cep, pagamento.modo, pagamento.nome_Titular, pagamento.numero_Cartao, pagamento.data_Expiracao, pagamento.cvv, pagamento.parcela))
        if (resultado.rowcount > 0):            
            conexao.commit()
            conexao.close()
            return pagamento
        else: 
            conexao.close()
            return None
        
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM pagamento WHERE id=?"
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
    def obterTodos(cls) -> List[Pagamento]:
        sql = "SELECT pagamento.id, pagamento.nome, pagamento.sobrenome, pagamento.email, pagamento.endereco, pagamento.pais, pagamento.estado, pagamento.cep, pagamento.modo, pagamento.nome_Titular, pagamento.numero_Cartao, pagamento.data_Expiracao, pagamento.cvv, pagamento.parcela FROM pagamento ORDER BY pagamento.id"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Pagamento(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterPagina(cls, pagina: int = 1, tamanhoPagina: int = 6) -> List[Pagamento]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT pagamento.nome, pagamento.sobrenome, pagamento.email, pagamento.endereco, pagamento.pais, pagamento.estado, pagamento.cep, pagamento.modo, pagamento.nome_Titular, pagamento.numero_Cartao, pagamento.data_Expiracao, pagamento.cvv, pagamento.parcela FROM pagamento ORDER BY pagamento.nome LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [Pagamento(*x) for x in resultado]
        return objetos

    @classmethod
    def obterTotalPaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM pagamento) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return resultado[0]
    
    @classmethod
    def obterPorId(cls, id: int) -> Pagamento:
        sql = "SELECT nome, sobrenome, email, endereco, pais, estado, cep, modo, nome_Titular, numero_Cartao, data_Expiracao, cvv, parcela FROM pagamento WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        objeto = Pagamento(*resultado)
        return objeto    