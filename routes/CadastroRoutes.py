from datetime import date
from io import BytesIO
import os
from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile
from PIL import Image
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import APIRouter, Depends, Form, Path, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi import Form, Request, status, Query
from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from util.templatesFilters import capitalizar_nome_proprio, formatarData, formatarIdParaImagem
from util.imageUtil import transformar_em_quadrada
from util.validator import *
from util.security import *

router = APIRouter()
# router = APIRouter(prefix="/usuario")

templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
  templates.env.filters["date"] = formatarData
  templates.env.filters["id_img"] = formatarIdParaImagem


"""@router.get("/cadastro", response_class=HTMLResponse)
async def getCadastro(request: Request):
    return templates.TemplateResponse("cadastro/cadastro.html", {"request": request})"""


# @router.get("/cadastro", response_class=HTMLResponse)
# async def getCadastro(request: Request):
#   return templates.TemplateResponse(
#     "cadastro/cadastro.html",
#     {
#       "request": request},
#   )

@router.get("/cadastro", response_class=HTMLResponse)
async def getCadastro(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "cadastro/cadastro.html",
        {"request": request, "usuario": usuario},
    )

@router.get("/preferencias", response_class=HTMLResponse)
async def getPreferencias(request: Request):
  usuarios = UsuarioRepo.obterTodos()
  return templates.TemplateResponse("cadastro/preferencias.html", {
    "request": request,
    "usuarios": usuarios
  })

@router.get("/alterarSenha", response_class=HTMLResponse)
async def getAlterarSenha(request: Request,
                          usuario: Usuario = Depends(validar_usuario_logado)):
  if usuario:
    return templates.TemplateResponse("cadastro/alterarSenha.html", {
      "request": request,
      "usuario": usuario
    })
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/usuarios", response_class=HTMLResponse)
async def getUsuarios(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    # Obtenha a lista atualizada de usuários
  usuario = UsuarioRepo.obterUm(usuario.id)
  if usuario:
    if usuario.admin:
      usuarios = UsuarioRepo.obterTodos()
      # usuario = UsuarioRepo.obterUm(usuario.id)
      return templates.TemplateResponse("cadastro/usuarios.html",
                                      {"request": request, "usuarios": usuarios, "usuario": usuario})
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
  else:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  


@router.get("/configuracoes", response_class=HTMLResponse)
async def getConfiguracoes(request: Request,
                           usuario: Usuario = Depends(validar_usuario_logado)):
  usuario = UsuarioRepo.obterUm(usuario.id)
  return templates.TemplateResponse("cadastro/configuracoes.html", {
    "request": request,
    "usuario": usuario
  })

@router.get("/modificacaoRealizada", response_class=HTMLResponse)
async def getModificacaoRealizada(request: Request,
                           usuario: Usuario = Depends(validar_usuario_logado)):
  usuario = UsuarioRepo.obterUm(usuario.id)
  return templates.TemplateResponse("cadastro/modificacaoRealizada.html", {
    "request": request,
    "usuario": usuario
  })

@router.post("/cadastro")
async def postUsuario(request: Request,
                      usuario: Usuario = Depends(validar_usuario_logado),
                      nome: str = Form(),
                      email: str = Form(),
                      senha: str = Form(),
                      endereco: str = Form(),
                      dataNascimento: date = Form(),
                      sexo: str = Form(),
                      confSenha: str = Form(),
                      semgluten: Optional[bool] = Form(False),
                      vegetariano: Optional[bool] = Form(False),
                      lowcarb: Optional[bool] = Form(False),
                      semfrutosdomar: Optional[bool] = Form(False),
                      semlactose: Optional[bool] = Form(False),
                      vegano: Optional[bool] = Form(False),
                      integral: Optional[bool] = Form(False),
                      semleite: Optional[bool] = Form(False),
                      semacucar: Optional[bool] = Form(False),
                      semovo: Optional[bool] = Form(False),
                      semcacau: Optional[bool] = Form(False),
                      organico: Optional[bool] = Form(False),
                      arquivoImagem: UploadFile = File(...)):

  # normalização dos dados
  nome = capitalizar_nome_proprio(nome).strip()
  email = email.lower().strip()
  senha = senha.strip()
  confSenha = confSenha.strip()

  # verificação de erros
  erros = {}
  # validação do campo nome
  is_not_empty(nome, "nome", erros)
  is_person_fullname(nome, "nome", erros)
  # validação do campo email
  is_not_empty(email, "email", erros)
  if is_email(email, "email", erros):
    if UsuarioRepo.emailExiste(email):
      add_error("email", "Já existe um usuário cadastrado com este e-mail.",
                erros)
  # validação do campo senha
  is_not_empty(senha, "senha", erros)
  is_password(senha, "senha", erros)
  # validação do campo confSenha
  is_not_empty(confSenha, "confSenha", erros)
  is_matching_fields(confSenha, "confSenha", senha, "Senha", erros)
  # validação da imagem
  conteudo_arquivo = await arquivoImagem.read()
  imagem = Image.open(BytesIO(conteudo_arquivo))
  if not imagem:
      add_error("arquivoImagem", "Nenhuma imagem foi enviada.", erros)

  # se tem erro, mostra o formulário novamente
  if len(erros) > 0:
    valores = {}
    valores["nome"] = nome
    valores["email"] = email.lower()
    valores["endereco"] = endereco
    valores["dataNascimento"] = str(dataNascimento)  
    return templates.TemplateResponse(
      "cadastro/cadastro.html",
      {
        "request": request,
        "usuario": usuario,
        "erros": erros,
        "valores": valores,
      },
    )
  
 # grava os dados no banco e redireciona para a listagem
  usuario = UsuarioRepo.inserir(
  Usuario(id=0, nome=nome, email=email, senha=obter_hash_senha(senha), endereco=endereco, dataNascimento=dataNascimento, sexo=sexo, semgluten=semgluten, vegetariano=vegetariano, lowcarb=lowcarb, semfrutosdomar=semfrutosdomar, semlactose=semlactose, vegano=vegano, integral=integral, semleite=semleite, semacucar=semacucar, semovo=semovo, semcacau=semcacau, organico=organico
         ))
  if (usuario):
        imagem_quadrada = transformar_em_quadrada(imagem)
        imagem_quadrada.save(f"static/imagens/usuarios/{usuario.id:04d}.jpg", "JPEG")


  # mostra página de sucesso
  return templates.TemplateResponse(
    "cadastro/modificacaoRealizada.html",
    {
      "request": request,
      "usuario": usuario
    },
  )
  
@router.post("/alterarSenha", response_class=HTMLResponse)
async def postAlterarSenha(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    senhaAtual: str = Form(""),
    novaSenha: str = Form(""),
    confNovaSenha: str = Form(""),
):
  # normalização dos dados
  senhaAtual = senhaAtual.strip()
  novaSenha = novaSenha.strip()
  confNovaSenha = confNovaSenha.strip()

  # verificação de erros
  erros = {}
  # validação do campo senhaAtual
  is_not_empty(senhaAtual, "senhaAtual", erros)
  is_password(senhaAtual, "senhaAtual", erros)

  # validação do campo novaSenha
  is_not_empty(novaSenha, "novaSenha", erros)
  is_password(novaSenha, "novaSenha", erros)
  # validação do campo confNovaSenha
  is_not_empty(confNovaSenha, "confNovaSenha", erros)
  is_matching_fields(confNovaSenha, "confNovaSenha", novaSenha, "Nova Senha",
                     erros)

  # só verifica a senha no banco de dados se não houverem erros de validação
  if len(erros) == 0:
    hash_senha_bd = UsuarioRepo.obterSenhaDeEmail(usuario.email)
    if hash_senha_bd:
      if not verificar_senha(senhaAtual, hash_senha_bd):
        add_error("senhaAtual", "Senha atual está incorreta.", erros)

  # se tem erro, mostra o formulário novamente
  if len(erros) > 0:
    valores = {}
    return templates.TemplateResponse(
      "main/login.html",
      {
        "request": request,
        "usuario": usuario,
        "erros": erros,
        "valores": valores,
      },
    )

  # se passou pelas validações, altera a senha no banco de dados
  hash_nova_senha = obter_hash_senha(novaSenha)
  if usuario:
    UsuarioRepo.alterarSenha(usuario.id, hash_nova_senha)

  # mostra página de sucesso
  return templates.TemplateResponse(
    "cadastro/modificacaoRealizada.html",
    {
      "request": request,
      "usuario": usuario
    },
  )

  if usuario:
    if usuario.admin:
      return templates.TemplateResponse(
        "adm/paginas.html",
        {
          "request": request,
          "usuario": usuario
        },
      )
    else:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/excluir/{id:int}", response_class=HTMLResponse)
async def getExcluir(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Path(),
):
  usuario = UsuarioRepo.obterUm(usuario.id)
  if usuario:
    if usuario.admin:
      usuario = UsuarioRepo.obterPorId(id)
      return templates.TemplateResponse(
        "cadastro/excluir.html",
        {
          "request": request,
          "usuario": usuario
        },
      )
    else:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



@router.post("/excluir/{id:int}", response_class=HTMLResponse)
async def postExcluir(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = 0,
):
  usuario = UsuarioRepo.obterUm(usuario.id)
  if usuario:
    if usuario.admin:
      if UsuarioRepo.excluir(id):
        return RedirectResponse("/usuarios",
                                status_code=status.HTTP_303_SEE_OTHER)
      else:
        raise Exception("Não foi possível excluir o usuario.")
    else:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



@router.post("/configuracoes", response_class=HTMLResponse)
async def postAlterarDados(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    nomeAtual: str = Form(),
    emailAtual: str = Form(),
    enderecoAtual: str = Form(),
    dataNascimentoAtual: str = Form(),
    sexoAtual: str = Form(),
    semglutenAtual: Optional[bool] = Form(),
    vegetarianoAtual: Optional[bool]  = Form(),
    lowcarbAtual: Optional[bool]  = Form(),
    semfrutosdomarAtual: Optional[bool]  = Form(),
    semlactoseAtual: Optional[bool]  = Form(),
    veganoAtual: Optional[bool]  = Form(),
    integralAtual: Optional[bool]  = Form(),
    semleiteAtual: Optional[bool] = Form(),
    semacucarAtual: Optional[bool]  = Form(),
    semovoAtual: Optional[bool]  = Form(),
    semcacauAtual: Optional[bool] = Form(),
    organicoAtual: Optional[bool] = Form()
):
  nomeAtual = capitalizar_nome_proprio(nomeAtual).strip()
  emailAtual = emailAtual.lower().strip()

  # verificação de erros
  erros = {}
  # validação do campo nome
  is_not_empty(nomeAtual, "nome", erros)
  is_person_fullname(nomeAtual, "nome", erros)
  # validação do campo email
  is_not_empty(emailAtual, "email", erros)  


  if usuario:

    usuario_atualizado = Usuario(
        id=usuario.id,
        nome=nomeAtual,
        email=emailAtual,
        endereco=enderecoAtual,
        dataNascimento=dataNascimentoAtual,
        sexo=sexoAtual,
        semgluten=semglutenAtual,
        vegetariano=vegetarianoAtual,
        lowcarb=lowcarbAtual,
        semfrutosdomar=semfrutosdomarAtual,
        semlactose=semlactoseAtual,
        vegano=veganoAtual,
        integral=integralAtual,
        semleite=semleiteAtual,
        semacucar=semacucarAtual,
        semovo=semovoAtual,
        semcacau=semcacauAtual,
        organico=organicoAtual
    )
    # Chame o método alterar com o objeto Usuario
    UsuarioRepo.alterar(usuario_atualizado)

# mostra página de sucesso
    return templates.TemplateResponse(
        "cadastro/modificacaoRealizada.html",
        {
            "request": request,
            "usuario": usuario
        },
    )
