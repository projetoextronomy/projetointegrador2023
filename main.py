from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from repositories.CupomRepo import CupomRepo
from repositories.ReceitaRepo import ReceitaRepo
from repositories.PostagemRepo import PostagemRepo
from repositories.UsuarioRepo import UsuarioRepo
from routes.MainRoutes import router as mainRoutes
from routes.CadastroRoutes import router as cadastroRoutes
from routes.ReceitaRoutes import router as receitaRoutes
from routes.CupomRoutes import router as cupomRoutes
from routes.PagamentoRoutes import router as pagamentoRoutes
from routes.OutrosRoutes import router as outrosRoutes
from routes.UsuarioRoutes import router as usuarioRoutes
from routes.PostagemRoutes import router as postagemRoutes


UsuarioRepo.criarTabela()
CupomRepo.criarTabela()
ReceitaRepo.criarTabela()
PostagemRepo.criarTabela()
UsuarioRepo.criarUsuarioAdmin()

app = FastAPI()

app.mount(path="/static", app=StaticFiles (directory="static"), name="static")

app.include_router(mainRoutes)
app.include_router(cadastroRoutes)
app.include_router(receitaRoutes)
app.include_router(cupomRoutes)
app.include_router(pagamentoRoutes)
app.include_router(outrosRoutes)
app.include_router(usuarioRoutes)
app.include_router(postagemRoutes)


#if __name__ =="__main__":
    #uvicorn.run(app="main:app", reload=True, port=8000)