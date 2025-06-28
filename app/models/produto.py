from __future__ import annotations
from typing import Dict, Any

class Produto:
    id: str
    nome: str
    descricao: str
    preco: float
    estoque: int
    image_filename: str
    categoria: str

    def __init__(self, id: str, nome: str, descricao: str, preco: float, estoque: int, image_filename: str, categoria: str) -> None:

        self._id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.image_filename = image_filename
        self.categoria = categoria

    # Properties para acesso limpo e controlado
    @property
    def id(self) -> str:
        return self._id

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, value: float) -> None:

        if value >= 0:
            self._preco = value
        else:
            raise ValueError("O preço não pode ser negativo.")

    @property
    def estoque(self) -> int:
        return self._estoque

    @estoque.setter
    def estoque(self, value: int) -> None:
        if value >= 0:
            self._estoque = value
        else:
            raise ValueError("O estoque não pode ser negativo.")

    def reduzir_estoque(self, quantidade: int) -> None:
        if 0 < quantidade <= self._estoque:
            self._estoque -= quantidade
        else:
            raise ValueError("Quantidade inválida ou estoque insuficiente.")

    def to_dict(self) -> Dict[str, Any]:
        """Cria um dicionário a partir do objeto, ideal para serialização JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "estoque": self.estoque,
            "image_filename": self.image_filename,
            "categoria": self.categoria
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Produto:
        """Cria uma instância de Produto a partir de um dicionário."""
        return Produto(**data)

    def __str__(self) -> str:
        return f"{self.nome} - R${self.preco:.2f} ({self.estoque} unidades disponíveis)"