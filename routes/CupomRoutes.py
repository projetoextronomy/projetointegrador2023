# routes/ProjetoRoutes.py
from io import BytesIO
from PIL import Image
from anyio import Path
from click import File
from fastapi import APIRouter, Form, HTTPException, Request, UploadFile, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Cupom import Cupom
from repositories.CupomRepo import CupomRepo
from util.imageUtil import transformar_em_quadrada
from util.templatesFilters import capitalizar_nome_proprio, formatarData, formatarIdParaImagem
from util.templatesFilters import formatarHora
from datetime import date, time
from util.validator import *
from util.security import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")

CupomRepo.criarTabela()

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem


@router.on_event("startup")
async def startup_event():
    templates.env.filters["time"] = formatarHora
    templates.env.filters["id_img"] = formatarIdParaImagem


@router.get("/cupons", response_class=HTMLResponse)
async def getCupons(request: Request, pn: int = 1, ps: int = 3, usuario: Usuario = Depends(validar_usuario_logado)):
    usuario =  UsuarioRepo.obterUm(usuario.id)  
    cupons = CupomRepo.obterPagina(pn, ps)
    totalPaginas = CupomRepo.obterTotalPaginas(ps)
    return templates.TemplateResponse("cupom/cupons.html", {"request": request, "cupons": cupons, "totalPaginas": totalPaginas, "tamanhoPagina": ps, "paginaAtual": pn, "usuario":usuario})
  
@router.get("/criarCupom", response_class=HTMLResponse)
async def getCriarCupom(request: Request):
    # if usuario:
    #   if usuario.admin:
      return templates.TemplateResponse("cupom/criarCupom.html", {"request": request})
    #   else:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    # else:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.post("/criarCupom")
async def postcriarCupom(
    request: Request,
    nome: str = Form(),
    valor: float = Form(),
    condicao: str = Form(),
    dt_inicio: date = Form(),
    dt_fim: date = Form(),
    hr_inicio: time = Form(),
    hr_fim: time = Form(),
    arquivoImagem: UploadFile = File(...)
):
    usuario: Usuario = Depends(validar_usuario_logado),

    if usuario:
            # normalização de dados
            nome = capitalizar_nome_proprio(nome).strip()

            # tratamento de erros
            erros = {}
            # validação do campo nome
            is_not_empty(nome, "nome", erros)
            is_size_between(nome, "nome", 4, 32, erros)
            is_project_name(nome, "nome", erros)

            # se tem erro, mostra o formulário novamente
            if len(erros) > 0:
                valores = {}
                valores["nome"] = nome
                return templates.TemplateResponse(
                    "projeto/novo.html",
                    {
                        "request": request,
                        "usuario": usuario,
                        "erros": erros,
                        "valores": valores,
                    },
                )


    conteudo_arquivo = await arquivoImagem.read()
    imagem = Image.open(BytesIO(conteudo_arquivo))
    if not imagem:
      add_error("arquivoImagem", "Nenhuma imagem foi enviada.", erros)

    dt_inicio_str = formatarHora(dt_inicio)
    dt_fim_str = formatarHora(dt_fim)
    hr_inicio_str = formatarHora(hr_inicio)
    hr_fim_str = formatarHora(hr_fim)
    
  
    cupom = CupomRepo.inserir(Cupom(0, nome, valor, condicao, dt_inicio_str, dt_fim_str, hr_inicio_str, hr_fim_str))
    
    if (cupom):
        imagem.save(f"static/imagens/cupons/{cupom.id:04d}.jpg", "JPEG")
    
    return RedirectResponse("/cupons", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/excluir_cupom/{id:int}", response_class=HTMLResponse)
async def getExcluirCupom(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Path(),
):
    usuario = UsuarioRepo.obterUm(usuario.id)
    if usuario.admin:
            cupom = CupomRepo.obterPorId(id)
            return templates.TemplateResponse(
                "cupom/excluir_cupom.html",
                {"request": request, "usuario": usuario, "cupom": cupom},
            )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.post("/excluir_cupom/{id:int}", response_class=HTMLResponse)
async def postExcluirCupom(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = 0,
):
    usuario = UsuarioRepo.obterUm(usuario.id)
    if usuario.admin:
            if CupomRepo.excluir(id):  # Atualize para o método de seu repositório Receita
                return RedirectResponse(
                    "/cupons", status_code=status.HTTP_303_SEE_OTHER
                )
            else:
                raise Exception("Não foi possível excluir o cupom.")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)