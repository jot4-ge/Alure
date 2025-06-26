import json
from models.roupa import Roupa
from typing import Optional


class ProductRecord():

    def __init__(self):
        self.__products = []
        self.read()

    def read(self):
        try:
            with open("app/controllers/db/products.json", "r") as arquivo_json:
                product_data = json.load(arquivo_json)
                self.__products = [Roupa(**roupa_data) for roupa_data in product_data]
        except FileNotFoundError:
            print("ERRO read() DataRecord: Json não achado, lista de produtos vazia na memoria.")
        except json.JSONDecodeError:
            print("ERRO read() DataRecord: Erro ao decodificar JSON. O arquivo pode estar corrompido.")
            self.__products = []

    def save(self):
        try:
            with open("app/controllers/db/products.json", "w") as arquivo_json:
                json.dump([roupa.__dict__ for roupa in self.__products], arquivo_json, indent=4)
        except FileNotFoundError:
            print("ERRO save(): Json não encontrado ou erro de permissão.")

    def add_product(self, product: Roupa) -> bool:

        if any(hasattr(p, 'id') and str(p.id) == str(product.id) for p in self.__products):
            print(f"AVISO: Produto com ID '{product.id}' já existe. Não adicionado.")
            return False

        self.__products.append(product)
        self.save()
        return True

    def get_product(self, product_id: str) -> Optional[Roupa]:
        for product in self.__products:
            if hasattr(product, 'id') and str(product.id) == str(product_id):
                return product
        return None

    def remove_product(self, product_id: str) -> bool:
        initial_len = len(self.__products)
        self.__products = [p for p in self.__products if not (hasattr(p, 'id') and str(p.id) == str(product_id))]

        if len(self.__products) < initial_len:
            self.save()
            return True
        else:
            print(f"AVISO: Produto com ID '{product_id}' não encontrado para remoção.")
            return False

    def edit_product(self, updated_product: Roupa) -> bool:
        found = False
        for i, product in enumerate(self.__products):
            if hasattr(product, 'id') and str(product.id) == str(updated_product.id):
                self.__products[i] = updated_product
                found = True
                break

        if found:
            self.save()
            return True
        else:
            print(f"AVISO: Produto com ID '{updated_product.id}' não encontrado para edição.")
            return False

    def get_all_products(self) -> list[Roupa]:
        """Retorna uma cópia da lista de todos os produtos."""
        return self.__products[:]