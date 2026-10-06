import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, Boolean
from sqlalchemy.orm import relationship

from database import Base

class tiposCanal(str, enum.Enum):
    app = "APP"
    totem = "TOTEM"
    balcao = "BALCAO"
    pickup = "PICKUP"
    web = "WEB"

class tiposPerfil(str, enum.Enum):
    cliente = "CLIENTE"
    atendente = "ATENDENTE"
    gerente = "GERENTE"

class tiposStatusPedido(str, enum.Enum):
    aguardandoPagamento = "AGUARDANDO PAGAMENTO"
    preparando = "PREPARANDO"
    pronto = "PRONTO"
    entregue = "ENTREGUE"
    cancelado = "CANCELADO"
    pagamentoNegado = "PAGAMENTO NEGADO"

class Usuario(Base):
    __tablename__ = "usuarios"

    usuarioId = Column(Integer, primary_key=True, index=True)
    nomeUsuario = Column(String, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(150), nullable=False)
    perfil = Column(Enum(tiposPerfil), nullable=False)
    lgpd = Column(Boolean, nullable=False, default=False)
    fidelidade = relationship("Fidelidade", back_populates="usuario", uselist=False)


class Pedido(Base):
    __tablename__ = "pedidos"

    pedidoId = Column(Integer, primary_key=True, index=True)
    usuarioId = Column(Integer, ForeignKey("usuarios.usuarioId"), nullable=False)
    unidadeId = Column(Integer, ForeignKey("unidades.unidadeId"), index=True)
    canalPedido = Column(Enum(tiposCanal), nullable=False)
    itens = relationship("Item", back_populates="pedido")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False)
    status = Column(Enum(tiposStatusPedido), nullable=False)
    unidade = relationship("Unidade", back_populates="pedidos")
    valorTotal = Column(Float, nullable=False)

class Produto(Base):
    __tablename__ = "produtos"

    produtoId = Column(Integer, primary_key=True, index=True)
    nomeProduto = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoques = relationship("Estoque", back_populates="produto")
    itens = relationship("Item", back_populates="produto")

class Item(Base):
    __tablename__ = "itens"

    itemId = Column(Integer, primary_key=True, index=True)
    pedidoId = Column(Integer, ForeignKey("pedidos.pedidoId"), nullable=False)
    produtoId = Column(Integer, ForeignKey("produtos.produtoId"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valorUnidade = Column(Float, nullable=False)
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")

class Unidade(Base):
    __tablename__ = "unidades"
    unidadeId = Column(Integer, primary_key=True, index=True)
    nomeUnidade = Column(String, nullable=False, index=True)
    localUnidade = Column(String, nullable=False)
    estoque = relationship("Estoque", back_populates="unidade")
    pedidos = relationship("Pedido", back_populates="unidade")

class Estoque(Base):
    __tablename__ = "estoque"
    estoqueId = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer, nullable=False)
    produtoId = Column(Integer, ForeignKey("produtos.produtoId"))
    unidadeId = Column(Integer, ForeignKey("unidades.unidadeId"))
    produto = relationship("Produto", back_populates="estoques")
    unidade = relationship("Unidade", back_populates="estoque")


class Pagamento(Base):
    __tablename__ = "pagamentos"
    pagamentoId = Column(Integer, primary_key=True, index=True)
    pedidoId = Column(Integer, ForeignKey("pedidos.pedidoId"), nullable=False)
    pedido = relationship("Pedido", back_populates="pagamento", uselist=False)
    statusPagamento = Column(Enum(tiposStatusPedido), nullable=False)

class Fidelidade(Base):
    __tablename__ = "fidelidade"
    fidelidadeId = Column(Integer, primary_key=True, index=True)
    pontos = Column(Integer, nullable=False)
    usuarioId = Column(Integer, ForeignKey("usuarios.usuarioId"))
    usuario = relationship("Usuario", back_populates="fidelidade")