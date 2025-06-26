class Produto:
    def __init__(self, id, nome, descricao, preco, estoque, image_name=None):
        self._id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.image_path = f"/static/img/clothes/{image_name}" if image_name else None

    # Properties para acesso limpo e controlado
    @property
    def id(self):
        return self._id

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, value):
        if value >= 0:
            self._preco = value
        else:
            raise ValueError("O preço não pode ser negativo.")

    @property
    def estoque(self):
        return self._estoque

    @estoque.setter
    def estoque(self, value):
        if value >= 0:
            self._estoque = value
        else:
            raise ValueError("O estoque não pode ser negativo.")

    def reduzir_estoque(self, quantidade):
        if 0 < quantidade <= self._estoque:
            self._estoque -= quantidade
        else:
            raise ValueError("Quantidade inválida ou estoque insuficiente.")

    def to_dict(self):
        """Cria um dicionário a partir do objeto, ideal para serialização JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "estoque": self.estoque,
            "image_path": self.image_path
        }

    @staticmethod
    def from_dict(data: dict):
        """Cria uma instância de Produto a partir de um dicionário."""
        return Produto(**data)

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} ({self.estoque} unidades disponíveis)"
