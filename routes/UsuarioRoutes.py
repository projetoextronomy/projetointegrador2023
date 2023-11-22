from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import APIRouter, Depends, Form, Path, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi import Form, Request, status, Query
from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from util.templatesFilters import capitalizar_nome_proprio, formatarData, formatarIdParaImagem
from util.validator import *
from util.security import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
  templates.env.filters["date"] = formatarData
  templates.env.filters["id_img"] = formatarIdParaImagem


"""@router.get("/cadastro", response_class=HTMLResponse)
async def getCadastro(request: Request):
    return templates.TemplateResponse("cadastro/cadastro.html", {"request": request})"""


@router.get("/cadastro", response_class=HTMLResponse)
async def getCadastro(request: Request,
                      usuario: Usuario = Depends(validar_usuario_logado)):
  return templates.TemplateResponse(
    "cadastro/cadastro.html",
    {
      "request": request,
      "usuario": usuario
    },
  )
  


@router.get("/preferencias", response_class=HTMLResponse)
async def getPreferencias(request: Request):
  usuarios = UsuarioRepo.obterTodos()
  return templates.TemplateResponse("cadastro/preferencias.html", {
    "request": request,
    "usuarios": usuarios
  })

@router.get("/alterarSenha", response_class=HTMLResponse)
async def getAlterarSenha(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return templates.TemplateResponse(
            "cadastro/alterarSenha.html", {"request": request, "usuario": usuario}
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/usuarios", response_class=HTMLResponse)
async def getUsuarios(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    usuarios = UsuarioRepo.obterTodos()
    if usuario:
      if usuario.admin:
         return templates.TemplateResponse("cadastro/usuarios.html", {
          "request": request,
          "usuarios": usuarios
          })
      else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  

@router.get("/configuracoes", response_class=HTMLResponse)
async def getConfiguracoes(request: Request,
                           usuario: Usuario = Depends(validar_usuario_logado)):
  usuario = UsuarioRepo.obterUm(usuario.id)
  if (not (usuario and usuario.admin)):
    return templates.TemplateResponse("cadastro/configuracoes.html", {
      "request": request,
      "usuario": usuario
    })
  else:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# @router.post("/novo_json")
# async def postNovoJson(
#     nome: str = Form(
#         ..., min_length=3, max_length=50, regex=r"^((\b[A-zÀ-ú']{2,40}\b)\s*){2,}$"
#     ),
#     email: str = Form(
#         ...,
#         regex=r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
#     ),
#     senha: str = Form(..., min_length=6, max_length=20),
#     confSenha: str = Form(..., min_length=6, max_length=20),
#     idProjeto: int = Form(..., gt=0),
# ):
#     if senha.strip() != confSenha.strip():
#         listaErros = []
#         listaErros.append(
#             {
#                 "type": "field_dont_match",
#                 "loc": ("body", "senha"),
#                 "msg": "Senhas não conferem.",
#             }
#         )
#         listaErros.append(
#             {
#                 "type": "field_dont_match",
#                 "loc": ("body", "confSenha"),
#                 "msg": "Senhas não conferem.",
#             }
#         )
#         raise RequestValidationError(listaErros)
#     else:
#       UsuarioRepo.inserir(
#           Usuario(
#               id=0,
#               nome=nome.strip(),
#               email=email.strip(),
#               senha=senha.strip(),
#           )
#       )
#       return JSONResponse({"ok": True, "returnUrl": "/"}, status_code=status.HTTP_200_OK)


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
                      semgluten: Optional[bool] = Form(None),
                      vegetariano: Optional[bool] = Form(None),
                      lowcarb: Optional[bool] = Form(None),
                      semfrutosdomar: Optional[bool] = Form(None),
                      semlactose: Optional[bool] = Form(None),
                      vegano: Optional[bool] = Form(None),
                      integral: Optional[bool] = Form(None),
                      semleite: Optional[bool] = Form(None),
                      semacucar: Optional[bool] = Form(None),
                      semovo: Optional[bool] = Form(None),
                      semcacau: Optional[bool] = Form(None),
                      organico: Optional[bool] = Form(None),
                      token: Optional[str] = Form(""),
                      admin: Optional[bool] = Form(None)):

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
  # validação do campo id

  # se tem erro, mostra o formulário novamente
  if len(erros) > 0:
    valores = {}
    valores["nome"] = nome
    valores["email"] = email.lower()
    return templates.TemplateResponse(
      "cadastro/cadastro.html",
      {
        "request": request,
        "usuario": usuario,
        "erros": erros,
        "valores": valores,
      },
    )

  UsuarioRepo.inserir(
    Usuario(0, nome, email, obter_hash_senha(senha), endereco, dataNascimento, sexo, semgluten, vegetariano, lowcarb, semfrutosdomar, semlactose, vegano, integral, semleite, semacucar, semovo, semcacau, organico,  gerar_token(token), admin))

  # mostra página de sucesso
  return templates.TemplateResponse(
    "cadastro/login.html",
    {
      "request": request,
      "usuario": usuario
    },
  )

# @router.post("/alterarsenha", response_class=HTMLResponse)
# async def postAlterarSenha(
#     request: Request,
#     usuario: Usuario = Depends(validar_usuario_logado),
#     senhaAtual: str = Form(""),
#     novaSenha: str = Form(""),
#     confNovaSenha: str = Form(""),    
# ):
#     # normalização dos dados
#     senhaAtual = senhaAtual.strip()
#     novaSenha = novaSenha.strip()
#     confNovaSenha = confNovaSenha.strip()    

#     # verificação de erros
#     erros = {}
#     # validação do campo senhaAtual
#     is_not_empty(senhaAtual, "senhaAtual", erros)
#     is_password(senhaAtual, "senhaAtual", erros)    
#     # validação do campo novaSenha
#     is_not_empty(novaSenha, "novaSenha", erros)
#     is_password(novaSenha, "novaSenha", erros)
#     # validação do campo confNovaSenha
#     is_not_empty(confNovaSenha, "confNovaSenha", erros)
#     is_matching_fields(confNovaSenha, "confNovaSenha", novaSenha, "Nova Senha", erros)
    
#     # só verifica a senha no banco de dados se não houverem erros de validação
#     if len(erros) == 0:    
#         hash_senha_bd = UsuarioRepo.obterSenhaDeEmail(usuario.email)
#         if hash_senha_bd:
#             if not verificar_senha(senhaAtual, hash_senha_bd):            
#                 add_error("senhaAtual", "Senha atual está incorreta.", erros)
    
#     # se tem erro, mostra o formulário novamente
#     if len(erros) > 0:
#         valores = {}        
#         return templates.TemplateResponse(
#             "cadastro/alterarSenha.html",
#             {
#                 "request": request,
#                 "usuario": usuario,                
#                 "erros": erros,
#                 "valores": valores,
#             },
#         )

#     # se passou pelas validações, altera a senha no banco de dados
#     hash_nova_senha = obter_hash_senha(novaSenha)
#     UsuarioRepo.alterarSenha(usuario.id, hash_nova_senha)
    
#     # mostra página de sucesso
#     return templates.TemplateResponse(
#         "main/login.html",
#         {"request": request, "usuario": usuario},
#     )

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
    is_matching_fields(
        confNovaSenha, "confNovaSenha", novaSenha, "Nova Senha", erros)

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
            "cadastro/alterarSenha.html",
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
        "cadastro/senhaAlterada.html",
        {"request": request, "usuario": usuario},
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
    if usuario:
        if usuario.admin:
            usuario = UsuarioRepo.obterPorId(id)
            return templates.TemplateResponse(
                "cadastro/excluir.html",
                {"request": request, "usuario": usuario, "usuario": usuario},
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/excluir", response_class=HTMLResponse)
async def postExcluir(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    id: int = Form(0),
):
    if usuario:
        if usuario.admin:
            if UsuarioRepo.excluir(id):
                return RedirectResponse(
                    "/cadastro/usuarios", status_code=status.HTTP_303_SEE_OTHER
                )
            else:
                raise Exception("Não foi possível excluir o usuario.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


