from typing import List
from models.Usuario import Usuario
from util.Database import Database

class UsuarioRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        endereco TEXT,
        dataNascimento DATE,
        sexo TEXT,
        semgluten BOOLEAN,
        vegetariano BOOLEAN,
        lowcarb BOOLEAN,
        semfrutosdomar BOOLEAN,
        semlactose BOOLEAN,
        vegano BOOLEAN,
        integral BOOLEAN,
        semleite BOOLEAN,
        semacucar BOOLEAN,
        semovo BOOLEAN,
        semcacau BOOLEAN,
        organico BOOLEAN,
        token TEXT,
        admin BOOLEAN) 
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        cursor.execute(sql)
        tableCreated = (cursor.execute(sql).rowcount > 0) 
        conexao.commit()
        conexao.close()
        return tableCreated
  
    
    @classmethod
    def inserir(cls, usuario: Usuario) -> Usuario:
      sql = "INSERT INTO usuario (nome, email, senha, endereco, dataNascimento, sexo, semgluten, vegetariano, lowcarb, semfrutosdomar, semlactose, vegano, integral, semleite, semacucar, semovo, semcacau, organico, token, admin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
      conexao = Database.criarConexao()
      cursor = conexao.cursor()
      result = cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha, usuario.endereco, usuario.dataNascimento, usuario.sexo, usuario.semgluten, usuario.vegetariano, usuario.lowcarb, usuario.semfrutosdomar, usuario.semlactose, usuario.vegano, usuario.integral, usuario.semleite, usuario.semacucar, usuario.semovo, usuario.semcacau, usuario.organico, usuario.token, usuario.admin))
      if (result.rowcount > 0):
        usuario.id = result.lastrowid
        conexao.commit()
        conexao.close()
        return usuario

    @classmethod
    def alterar(cls, usuario: Usuario) -> Usuario: 
        sql = "UPDATE usuario SET nome=?, email=?, senha=?, endereco=?, dataNascimento=?, sexo=?, semgluten=?, vegetariano=?, lowcarb=?, semfrutosdomar=?, semlactose=?, vegano=?, integral=?, semleite=?, semacucar=?, semovo=?, semcacau=?, organico=?, token=?, admin=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        result = cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha, usuario.endereco, usuario.dataNascimento, usuario.sexo,   usuario.semgluten, usuario.vegetariano, usuario.lowcarb, usuario.semfrutosdomar, usuario.semlactose, usuario.vegano, usuario.integral, usuario.semleite, usuario.semacucar, usuario.semovo, usuario.semcacau, usuario.organico, usuario.token, usuario.admin))
        if (result.rowcount>0):
            conexao.commit()
            conexao.close()
            return usuario
        else:
            conexao.close()
            return None
    
    @classmethod
    def alterarAdmin(cls, id: int, admin: bool) -> bool:
        sql = "UPDATE usuario SET admin=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (admin, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
    
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM usuario WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        result = cursor.execute(sql, (id, ))
        if (result.rowcount>0):
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
    
    @classmethod
    def obterTodos(cls) -> List[Usuario]:
        sql = "SELECT id, nome, email, senha, endereco, dataNascimento, sexo,  semgluten, vegetariano, lowcarb, semfrutosdomar, semlactose, vegano, integral, semleite, semacucar, semovo, semcacau, organico, token, admin FROM usuario"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        result = cursor.execute(sql).fetchall()
        usuarios = [Usuario(*x) for x in result]
        return usuarios
    
    @classmethod
    def obterUm(cls, id: int) -> Usuario:
        sql = ("SELECT id, nome, email,  senha, endereco, dataNascimento, sexo, semgluten, vegetariano, lowcarb, semfrutosdomar, semlactose, vegano, integral, semleite, semacucar, semovo, semcacau, organico, token, admin FROM usuario WHERE id=?")
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchone() 
        usuario = Usuario(*resultado)
        return usuario
       


    @classmethod
    def ordenarNome(cls) -> List[Usuario]:
        sql = "SELECT nome, email, senha, endereco, dataNascimento, sexo, semgluten, vegetariano, lowcarb, semfrutosdomar, semlactose, vegano, integral, semleite, semacucar, semovo, semcacau, organico, token, admin FROM usuario ORDER BY nome ASC"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Usuario(*x) for x in result]
        return objects
    
    @classmethod
    def obterPorId(cls, id: int) -> Usuario | None:
       sql = "SELECT usuario.id, usuario.nome, usuario.email, usuario.senha FROM usuario WHERE usuario.id=?"
       conexao = Database.criarConexao()
       cursor = conexao.cursor()
       resultado = cursor.execute(sql, (id,)).fetchone()

       if resultado:
        objeto = Usuario(
            id=resultado[0],
            nome=resultado[1],
            email=resultado[2],
            senha=resultado[3],)
        return objeto
       else:
        return None

        # objeto = Usuario(*resultado)
        # return objeto

    @classmethod
    def obterUsuarioPorToken(cls, token: str) -> Usuario:
        sql = "SELECT id, nome, email, senha, endereco, dataNascimento, sexo,  semgluten, vegetariano, lowcarb, semfrutosdomar, semlactose, vegano, integral, semleite, semacucar, semovo, semcacau, organico,  token, admin FROM usuario WHERE token=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        # quando se executa fechone em um cursor sem resultado, ele retorna None
        resultado = cursor.execute(sql, (token,)).fetchone()
        if resultado:
            objeto = Usuario(*resultado)
            return objeto
        else:
            return None


    @classmethod
    def obterSenhaDeEmail(cls, email: str) -> str | None:
        sql = "SELECT senha FROM usuario WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        if resultado:
            return str(resultado[0])
        else:
            return None

    @classmethod
    def alterarToken(cls, email: str, token: str) -> bool:
        sql = "UPDATE usuario SET token=? WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token, email))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def emailExiste(cls, email: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM usuario WHERE email=?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()        
        return bool(resultado[0])

    @classmethod
    def obterUsuarioPorToken(cls, token: str) -> Usuario:
        sql = "SELECT id, nome, email, admin FROM usuario WHERE token=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token, )).fetchone()
        if resultado:
            objeto = Usuario(*resultado)
            return objeto
        else:
            return None
          
    @classmethod
    def alterarAdmin(cls, id: int, admin: bool) -> bool:
        sql = "UPDATE usuario SET admin=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (admin, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def alterarSenha(cls, id: int, senha: str) -> bool:
        sql = "UPDATE usuario SET senha=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (senha, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
  
    @classmethod
    def criarUsuarioAdmin(cls) -> bool:
          sql = "INSERT OR IGNORE INTO usuario (nome, email, senha, admin) VALUES (?, ?, ?, ?)"
          # hash da senha 123456
          hash_senha = "$2b$12$WU9pnIyBUZOJHN7hgkhWtew8hI0Keiobr8idjIxYDwCyiSb5zh0iq"
          conexao = Database.criarConexao()
          cursor = conexao.cursor()
          resultado = cursor.execute(
              sql, ("Administrador do Sistema", "admin@email.com", hash_senha, True))
          if resultado.rowcount > 0:
              conexao.commit()
              conexao.close()
              return True
          else:
              conexao.close()
              return False
   
