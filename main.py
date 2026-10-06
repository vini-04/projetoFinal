from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from database import engine, get_db, Base
import models
import schemas
import crud
from auth import authenticate_user, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Raizes do Nordeste",
    version="1.0.0",
)


@app.post("/token", summary="Gerar token de acesso JWT", tags=["autenticacao"])
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    usuario = authenticate_user(db, email=form_data.username, password=form_data.password)
    if usuario:
        access_token = create_access_token(data={"sub": usuario.email})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post(
    "/usuarios/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo usuário",
    tags=["usuarios"]
)
def criarUsuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    novoUsuario = crud.criarUsuario(db, usuario)
    return {
        "mensagem": "Usuário criado com sucesso!",
        "usuario": novoUsuario
    }


@app.get(
    "/usuarios/",
    response_model=List[schemas.UsuarioResponse],
    summary="Buscar todos os usuários",
    tags=["usuarios"]
)
def buscarUsuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return crud.buscarUsuarios(db=db, skip=skip, limit=limit)


@app.get(
    "/usuarios/{usuario_id}",
    response_model=schemas.UsuarioResponse,
    summary="Buscar usuário por ID",
    tags=["usuarios"]
)
def buscarUsuario(usuario_id: int, db: Session = Depends(get_db)):
    bancoDadosUsuario = crud.buscarUsuario(db=db, usuario_id=usuario_id)
    if bancoDadosUsuario:
        return bancoDadosUsuario
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")


@app.delete(
    "/usuarios/{usuario_id}",
    summary="Apagar usuario por ID",
    tags=["usuarios"]
)
def apagarUsuario(usuario_id: int, db: Session = Depends(get_db)):
    bancoDadosUsuario = crud.apagarUsuarioPorId(db=db, usuario_id=usuario_id)
    if bancoDadosUsuario:
        return {
            "mensagem": "Usuário apagado com sucesso!",
            "usuario": bancoDadosUsuario
        }
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.post(
    "/produtos/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar produto",
    tags=["produtos"]
)
def criarProduto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    novoProduto = crud.criarProduto(db, produto)
    return {
        "mensagem": "Produto criado com sucesso!",
        "produto": novoProduto
    }

@app.get(
    "/produtos/",
    response_model=List[schemas.ProdutoResponse],
    summary="Buscar todos produtos",
    tags=["produtos"]
)
def buscarProdutos(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return crud.buscarProdutos(db=db, skip=skip, limit=limit)


@app.get(
    "/produtos/{produto_id}",
    response_model=schemas.ProdutoResponse,
    summary="Buscar produto por ID",
    tags=["produtos"]
)
def buscarProduto(produto_id: int, db: Session = Depends(get_db)):
    bancoDeDadosDoProduto = crud.buscarProduto(db=db, produto_id=produto_id)
    if bancoDeDadosDoProduto:
        return bancoDeDadosDoProduto
    else:
        raise HTTPException(status_code=404, detail="Produto não encontrado")


@app.delete(
    "/produtos/{produto_id}",
    summary="Excluir produto por ID",
    tags=["produtos"]
)
def apagarProduto(produto_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    bancoDeDadosDoProduto = crud.apagarProdutoPorId(db=db, produto_id=produto_id)
    if bancoDeDadosDoProduto:
        return {
            "mensagem": "Produto apagado com sucesso!",
            "produto": bancoDeDadosDoProduto
        }
    else:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.post(
    "/unidades/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova unidade",
    tags=["unidades"]
)
def criarUnidade(unidade: schemas.UnidadeCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    novaUnidade = crud.criarUnidade(db, unidade)
    return {
        "mensagem": "Unidade criada com sucesso!",
        "unidade": novaUnidade
    }

@app.get(
    "/unidades/",
    response_model=List[schemas.UnidadeResponse],
    summary="Buscar todas as unidades",
    tags=["unidades"]
)
def buscarUnidades(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return crud.buscarUnidades(db=db, skip=skip, limit=limit)


@app.delete(
    "/unidades/{unidade_id}",
    summary="Excluir unidade por ID",
    tags=["unidades"]
)
def apagarUnidade(unidade_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    bancoDeDadosDaUnidade = crud.apagarUnidadePorId(db=db, unidade_id=unidade_id)
    if bancoDeDadosDaUnidade:
        return {
            "mensagem": "Unidade apagada com sucesso!",
            "unidade": bancoDeDadosDaUnidade
        }
    else:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

@app.post(
    "/estoque/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar estoque",
    tags=["estoque"]
)
def criarEstoque(estoque: schemas.EstoqueCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    novoEstoque = crud.criarEstoque(db, estoque)
    return {
        "mensagem": "Estoque criado com sucesso!",
        "estoque": novoEstoque
    }

@app.post(
    "/pedidos/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar pedido",
    tags=["pedidos"]
)
def criarPedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    novoPedido = crud.criarPedido(db, pedido)
    return {
        "mensagem": "Pedido criado!",
        "pedido": novoPedido
    }

@app.get(
    "/pedidos/",
    response_model=List[schemas.PedidoResponse],
    summary="Buscar todos os pedidos",
    tags=["pedidos"]
)
def buscarPedidos(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return crud.buscarPedidos(db=db, skip=skip, limit=limit)


@app.get(
    "/pedidos/canal/{canal}",
    response_model=List[schemas.PedidoResponse],
    summary="Buscar pedidos por canal",
    tags=["pedidos"]
)
def buscarPedidosPorCanal(canal: models.tiposCanal, db: Session = Depends(get_db)):
    return crud.buscarPedidosPorCanal(db=db, canal=canal)


@app.delete(
    "/pedidos/{pedido_id}",
    summary="Excluir pedido por ID",
    tags=["pedidos"]
)
def apagarPedido(pedido_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    bancoDeDadosDoPedido = crud.apagarPedido(db=db, pedido_id=pedido_id)
    if bancoDeDadosDoPedido:
        return {
            "mensagem": "Pedido apagado com sucesso!",
            "pedido": bancoDeDadosDoPedido
        }
    else:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")