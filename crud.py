from sqlalchemy.orm import Session
from models import Usuario, Produto, Unidade, Estoque, Pedido, tiposCanal, Item, tiposStatusPedido, Pagamento
from schemas import UsuarioCreate, ProdutoCreate, UnidadeCreate, EstoqueCreate, PedidoCreate

def buscarUsuarioPorEmail(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def buscarUsuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.usuarioId == usuario_id).first()

def buscarUsuarios(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Usuario).offset(skip).limit(limit).all()

def criarUsuario(db: Session, payload: UsuarioCreate):
    from auth import get_password_hash
    senha_hash = get_password_hash(payload.senha)

    db_usuario = Usuario(
        nomeUsuario=payload.nomeUsuario,
        email=payload.email,
        senha=senha_hash,
        perfil=payload.perfil,
        lgpd=payload.lgpd
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def apagarUsuarioPorId(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.usuarioId == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario

def buscarProduto(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.produtoId == produto_id).first()

def buscarProdutos(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Produto).offset(skip).limit(limit).all()

def criarProduto(db: Session, payload: ProdutoCreate):
    db_produto = Produto(
        nomeProduto=payload.nomeProduto,
        preco=payload.preco
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def apagarProdutoPorId(db: Session, produto_id: int):
    db_produto = db.query(Produto).filter(Produto.produtoId == produto_id).first()
    if db_produto:
        db.delete(db_produto)
        db.commit()
    return db_produto

def buscarUnidades(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Unidade).offset(skip).limit(limit).all()

def criarUnidade(db: Session, payload: UnidadeCreate):
    db_unidade = Unidade(
        nomeUnidade=payload.nomeUnidade,
        localUnidade=payload.localUnidade
    )
    db.add(db_unidade)
    db.commit()
    db.refresh(db_unidade)
    return db_unidade

def apagarUnidadePorId(db: Session, unidade_id: int):
    db_unidade = db.query(Unidade).filter(Unidade.unidadeId == unidade_id).first()
    if db_unidade:
        db.delete(db_unidade)
        db.commit()
    return db_unidade

def buscarEstoque(db: Session, estoque_id: int):
    return db.query(Estoque).filter(Estoque.estoqueId == estoque_id).first()

def criarEstoque(db: Session, payload: EstoqueCreate):
    db_estoque = Estoque(
        quantidade=payload.quantidade,
        produtoId=payload.produtoId,
        unidadeId=payload.unidadeId
    )
    db.add(db_estoque)
    db.commit()
    db.refresh(db_estoque)
    return db_estoque

def buscarPedidos(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Pedido).offset(skip).limit(limit).all()

def buscarPedidosPorCanal(db: Session, canal: tiposCanal):
    return db.query(Pedido).filter(Pedido.canalPedido == canal).all()

def criarPedido(db: Session, payload: PedidoCreate):
    valorTotalCalculado = 0.0
    itensCalculados = []

    for itemNaLista in payload.itens:
        produto = db.query(Produto).filter(Produto.produtoId == itemNaLista.produtoId).first()
        if not produto:
            raise ValueError(f"Produto com ID {itemNaLista.produtoId} não encontrado.")

        subtotal = produto.preco * itemNaLista.quantidade
        valorTotalCalculado += subtotal

        itensCalculados.append({
            "produtoId": produto.produtoId,
            "quantidade": itemNaLista.quantidade,
            "valorUnidade": produto.preco
        })

    db_pedido = Pedido(
        usuarioId=payload.usuarioId,
        unidadeId=payload.unidadeId,
        canalPedido=payload.canalPedido,
        status=tiposStatusPedido.aguardandoPagamento,
        valorTotal=valorTotalCalculado
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)

    for itemGuardado in itensCalculados:
        db_item = Item(
            pedidoId=db_pedido.pedidoId,
            produtoId=itemGuardado["produtoId"],
            quantidade=itemGuardado["quantidade"],
            valorUnidade=itemGuardado["valorUnidade"]
        )
        db.add(db_item)

    db_pagamento = Pagamento(
        pedidoId=db_pedido.pedidoId,
        statusPagamento=tiposStatusPedido.aguardandoPagamento
    )
    db.add(db_pagamento)

    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def apagarPedido(db: Session, pedido_id: int):
    db_pedido = db.query(Pedido).filter(Pedido.pedidoId == pedido_id).first()
    if db_pedido:
        db.delete(db_pedido)
        db.commit()
    return db_pedido