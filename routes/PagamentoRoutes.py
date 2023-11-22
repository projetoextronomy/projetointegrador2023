# routes/ProjetoRoutes.py
from typing import Optional
from fastapi import APIRouter, Form, Request, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Pagamento import Pagamento
from repositories.PagamentoRepo import PagamentoRepo
from repositories.UsuarioRepo import UsuarioRepo
from util.templatesFilters import formatarData, formatarIdParaImagem
from util.templatesFilters import formatarHora
from datetime import date, time
from util.validator import *
from util.security import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")

PagamentoRepo.criarTabela()

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem

@router.on_event("startup")
async def startup_event():
    templates.env.filters["time"] = formatarHora

@router.get("/pagamentos", response_class=HTMLResponse)
async def getPagamentos(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)
    pagamentos = PagamentoRepo.obterTodos()
    return templates.TemplateResponse("pagamento/pagamentos.html", {"request": request, "pagamentos": pagamentos , "usuario":usuario})

@router.get("/novoPagamento", response_class=HTMLResponse)
async def getPagamentos(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse("pagamento/novoPagamento.html", {"request": request, "usuario":usuario})


@router.get("/pagamentos_cartao", response_class=HTMLResponse)
async def getPagamentosCartao(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario = UsuarioRepo.obterUm(usuario.id)
    pagamentos = PagamentoRepo.obterTodos()
    return templates.TemplateResponse("pagamento/pagamentos_cartao.html", {"request": request, "pagamentos": pagamentos, "usuario": usuario})

@router.post("/novoPagamento")
async def postNovoPagamento(
    nome: str = Form(),
    sobrenome: str = Form(),
    email: str = Form(),
    endereco: str = Form(),
    pais: str = Form(),
    estado: str = Form(),
    cep: str = Form(),
    modo: str = Form(),
    nome_Titular: Optional[str] = Form(None),
    numero_Cartao: Optional[int] = Form(None),
    data_Expiracao: Optional[date] = Form(None),
    cvv: Optional[int] = Form(None),
    parcela: Optional[int] = Form(None)):

    PagamentoRepo.inserir(Pagamento(0, nome, sobrenome, email, endereco, pais, estado, cep, modo, nome_Titular, numero_Cartao, data_Expiracao, cvv, parcela))
    return RedirectResponse("/modificacaoRealizada", status_code=status.HTTP_303_SEE_OTHER)