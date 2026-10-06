from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models import tiposCanal, tiposPerfil, tiposStatusPedido


class FidelidadeBase(BaseModel):
    pontos: int
    usuarioId: int


class FidelidadeCreate(FidelidadeBase):
    pass


class FidelidadeResponse(FidelidadeBase):
    fidelidadeId: int

    class Config:
        from_attributes = True


class UsuarioBase(BaseModel):
    nomeUsuario: str
    email: EmailStr
    perfil: tiposPerfil
    lgpd: bool


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioResponse(UsuarioBase):
    usuarioId: int
    fidelidade: Optional[FidelidadeResponse] = None

    class Config:
        from_attributes = True


class ProdutoBase(BaseModel):
    nomeProduto: str
    preco: float


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoResponse(ProdutoBase):
    produtoId: int

    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    produtoId: int
    quantidade: int


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    itemId: int
    pedidoId: int
    valorUnidade: float

    class Config:
        from_attributes = True


class EstoqueBase(BaseModel):
    quantidade: int
    produtoId: int
    unidadeId: int


class EstoqueCreate(EstoqueBase):
    pass


class EstoqueResponse(EstoqueBase):
    estoqueId: int

    class Config:
        from_attributes = True


class PagamentoBase(BaseModel):
    pedidoId: int
    statusPagamento: tiposStatusPedido

class PagamentoCreate(PagamentoBase):
    pass

class PagamentoResponse(PagamentoBase):
    pagamentoId: int

    class Config:
        from_attributes = True

class UnidadeBase(BaseModel):
    nomeUnidade: str
    localUnidade: str


class UnidadeCreate(UnidadeBase):
    pass


class UnidadeResponse(UnidadeBase):
    unidadeId: int

    class Config:
        from_attributes = True


class PedidoBase(BaseModel):
    usuarioId: int
    unidadeId: int
    canalPedido: tiposCanal
    status: tiposStatusPedido
    valorTotal: float


class PedidoCreate(BaseModel):
    usuarioId: int
    unidadeId: int
    canalPedido: tiposCanal
    itens: List[ItemCreate]

class PedidoResponse(PedidoBase):
    pedidoId: int
    unidade: Optional[UnidadeResponse] = None
    itens: List[ItemResponse] = []
    pagamento: Optional[PagamentoResponse] = None

    class Config:
        from_attributes = True
