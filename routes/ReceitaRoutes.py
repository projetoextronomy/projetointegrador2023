from importlib.metadata import PathDistribution
from fastapi import APIRouter, Form, Request, status, Depends, HTTPException, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Receita import Receita
from repositories.ReceitaRepo import ReceitaRepo
from repositories.UsuarioRepo import UsuarioRepo
from util.templatesFilters import formatarData, formatarIdParaImagem
from util.validator import *
from util.security import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem

@router.get("/criarReceita", response_class=HTMLResponse)
async def getCriarReceita(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse("receita/criarReceita.html", {"request": request, "usuario":usuario})

# """@router.get("/minhasReceitas", response_class=HTMLResponse)
# async def getMinhasReceitas(request: Request):
#     receitas = ReceitaRepo.obterTodos()
#     return templates.TemplateResponse("receita/minhasReceitas.html", {"request": request, "receitas": receitas})"""

@router.get("/minhasReceitas", response_class=HTMLResponse)
async def getMinhasReceitas(request: Request, pn: int = 1, ps: int = 3, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)
    receitas = ReceitaRepo.obterPagina(pn, ps)
    totalPaginas = ReceitaRepo.obterTotalPaginas(ps)
    return templates.TemplateResponse("receita/minhasReceitas.html", {"request": request, "receitas": receitas, "totalPaginas": totalPaginas, "tamanhoPagina": ps, "paginaAtual": pn , "usuario": usuario})


@router.get("/receitasSalvas", response_class=HTMLResponse)
async def getReceitasSalvas(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)     
    return templates.TemplateResponse("receita/receitasSalvas.html", {"request": request,     "usuario": usuario})


@router.post("/criarReceita")
async def postCriarReceita(
    titulo: str = Form(),
    tempoPreparo: int = Form(),
    rendimento: int = Form(), 
    descricao: str = Form()):
    # midia: str = Form(),
    # qntCurtida: int = Form(),
    # idAutor: int = Form()):
    ReceitaRepo.inserir(Receita(0, titulo=titulo, tempoPreparo=tempoPreparo, rendimento=rendimento, descricao=descricao))
    return RedirectResponse("/minhasReceitas", status_code=status.HTTP_303_SEE_OTHER)
    

@router.get("/excluir_receita/{id:int}", response_class=HTMLResponse)
async def getExcluirReceita(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Path(),
):
    usuario = UsuarioRepo.obterUm(usuario.id)
    if usuario:
            receita = ReceitaRepo.obterPorId(id)  # Atualize para o método de seu repositório Receita
            return templates.TemplateResponse(
                "receita/excluir_receita.html",
                {"request": request, "usuario": usuario, "receita": receita},
            )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.post("/excluir_receita/{id:int}", response_class=HTMLResponse)
async def postExcluirReceita(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = 0,
):
    usuario = UsuarioRepo.obterUm(usuario.id)
    if usuario:
            if ReceitaRepo.excluir(id):  # Atualize para o método de seu repositório Receita
                return RedirectResponse(
                    "/minhasReceitas", status_code=status.HTTP_303_SEE_OTHER
                )
            else:
                raise Exception("Não foi possível excluir a receita.")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
