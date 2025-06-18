class Produto:
    def __init__(self, id, nome, descricao, preco, estoque, image_name=None):
        self.__id = id
        self.__nome = nome
        self.__descricao = descricao
        self.__preco = preco
        self.__estoque = estoque
        self.image_path = "/static/img/clothes/" + image_name

    # Getters
    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def get_descricao(self):
        return self.__descricao

    def get_preco(self):
        return self.__preco

    def get_estoque(self):
        return self.__estoque

    # Setters
    def set_nome(self, nome):
        self.__nome = nome

    def set_descricao(self, descricao):
        self.__descricao = descricao

    def set_preco(self, preco):
        if preco >= 0:
            self.__preco = preco
        else:
            print("Preço inválido!")

    def set_estoque(self, estoque):
        if estoque >= 0:
            self.__estoque = estoque
        else:
            print("Estoque inválido!")

    def reduzir_estoque(self, quantidade):
        if quantidade <= self.__estoque:
            self.__estoque -= quantidade
        else:
            print("Estoque insuficiente.")
    def to_dict(self):
        return self.__dict__
    @staticmethod
    def from_dict(data: dict):
        return Produto(**data)


    def __str__(self):
        return f"{self.__nome} - R${self.__preco:.2f} ({self.__estoque} unidades disponíveis)"