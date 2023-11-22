from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Form, Request, status, Query
from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from util.security import obter_hash_senha, validar_usuario_logado
from util.security import gerar_token
from util.templatesFilters import capitalizar_nome_proprio, formatarData, formatarIdParaImagem
from util.validator import *
from util.security import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem

@router.get("/ajuda", response_class=HTMLResponse)
async def getAjuda(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
  usuario = UsuarioRepo.obterUm(usuario.id)  
  return templates.TemplateResponse("outros/ajuda.html", {"request": request, "usuario": usuario})

@router.get("/sobre", response_class=HTMLResponse)
async def getSobre(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)  
    return templates.TemplateResponse("outros/sobre.html", {"request": request,     "usuario": usuario})



@router.get("/filtragem", response_class=HTMLResponse)
async def getFiltragem(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)
    return templates.TemplateResponse("outros/filtragem.html", {"request": request,     "usuario": usuario})

@router.get("/chat", response_class=HTMLResponse)
async def getChat(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)     
    return templates.TemplateResponse("outros/chat.html", {"request": request,     "usuario": usuario})


@router.get("/comentario", response_class=HTMLResponse)
async def getComentario(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)     
    return templates.TemplateResponse("outros/comentario.html", {"request": request,     "usuario": usuario})



@router.get("/editarPostagem", response_class=HTMLResponse)
async def getEditarPostagem(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)     
    return templates.TemplateResponse("outros/editarPostagem.html", {"request": request,     "usuario": usuario})

@router.get("/receita", response_class=HTMLResponse)
async def getReceita(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)     
    return templates.TemplateResponse("outros/receita.html", {"request": request,     "usuario": usuario})

@router.get("/recuperacao", response_class=HTMLResponse)
async def getRecuperacao(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)     
    return templates.TemplateResponse("outros/recuperacao.html", {"request": request,     "usuario": usuario})

@router.get("/recuperacao2", response_class=HTMLResponse)
async def getRecuperacao(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)     
    return templates.TemplateResponse("outros/recuperacao2.html", {"request": request,     "usuario": usuario})

@router.get("/resultadoFiltragem", response_class=HTMLResponse)
async def getResultadoFiltragem(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)     
    return templates.TemplateResponse("outros/resultadoFiltragem.html", {"request": request,     "usuario": usuario})

@router.get("/editarReceita", response_class=HTMLResponse)
async def getEditarReceita(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
  usuario = UsuarioRepo.obterUm(usuario.id)  
  return templates.TemplateResponse("outros/editarReceita.html", {"request": request, "usuario": usuario})