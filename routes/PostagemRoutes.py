# routes/ProjetoRoutes.py
from io import BytesIO
from PIL import Image
from fastapi import APIRouter, File, Form, Request, UploadFile, status, Depends, HTTPException, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Postagem import Postagem
from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from repositories.PostagemRepo import PostagemRepo
from util.templatesFilters import formatarData, formatarIdParaImagem
from util.templatesFilters import formatarHora
from datetime import date, time
from util.validator import *
from util.security import *
from datetime import datetime

router = APIRouter()

templates = Jinja2Templates(directory="templates")

PostagemRepo.criarTabela()

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem

@router.on_event("startup")
async def startup_event():
    templates.env.filters["time"] = formatarHora

@router.get("/minhasPostagens", response_class=HTMLResponse)
async def getMinhasPostagens(request: Request, pn: int = 1, ps: int = 3, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario =  UsuarioRepo.obterUm(usuario.id)  
    postagens = PostagemRepo.obterPorAutor(usuario.id)
    postagens = PostagemRepo.obterPagina(pn, ps)
    totalPaginas = PostagemRepo.obterTotalPaginas(ps)
    return templates.TemplateResponse("postagem/minhasPostagens.html", {"request": request, "postagens": postagens, "totalPaginas": totalPaginas, "tamanhoPagina": ps, "paginaAtual": pn, "usuario": usuario})
  
@router.get("/feed", response_class=HTMLResponse)
async def getFeed(request: Request,
                           usuario: Usuario = Depends(validar_usuario_logado)):
  usuario = UsuarioRepo.obterUm(usuario.id)  
  postagens = PostagemRepo.obterTodos()
  return templates.TemplateResponse("postagem/feed.html", {
    "request": request,
    "usuario": usuario,
    "postagens": postagens
  })

@router.post("/feed")
async def postFeed(
    request: Request,
    conteudo: str = Form(),
    usuario: Usuario = Depends(validar_usuario_logado),
    curtida: int = 0,
    deslike: int = 0,
    data_hora: datetime = None,
    arquivoImagem: UploadFile = File(...)
):
    erros = {}
    # validação da imagem
    conteudo_arquivo = await arquivoImagem.read()
    imagem = Image.open(BytesIO(conteudo_arquivo))
    if not imagem:
      add_error("arquivoImagem", "Nenhuma imagem foi enviada.", erros)

    if data_hora is None:
        data_hora = datetime.now()
  
    postagem = PostagemRepo.inserir(Postagem(id=0, conteudo=conteudo, usuario=usuario.id, curtida=curtida, deslike=deslike, data_hora=data_hora))

    if (postagem):
        imagem.save(f"static/imagens/postagens/{postagem.id:04d}.jpg", "JPEG")
    return RedirectResponse("/feed", status_code=status.HTTP_303_SEE_OTHER)



@router.get("/excluir_postagem/{id:int}", response_class=HTMLResponse)
async def getExcluirPostagem(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Path(),
):
    usuario = UsuarioRepo.obterUm(usuario.id)
    if usuario:
            postagem = PostagemRepo.obterPorId(id)  # Atualize para o método de seu repositório Receita
            return templates.TemplateResponse(
                "postagem/excluir_postagem.html",
                {"request": request, "usuario": usuario, "postagem": postagem},
            )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.post("/excluir_postagem/{id:int}", response_class=HTMLResponse)
async def postExcluirPostagem(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = 0,
):
    usuario = UsuarioRepo.obterUm(usuario.id)
    if usuario:
            if PostagemRepo.excluir(id):  # Atualize para o método de seu repositório Receita
                return RedirectResponse(
                    "/minhasPostagens", status_code=status.HTTP_303_SEE_OTHER
                )
            else:
                raise Exception("Não foi possível excluir a postagem.")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)