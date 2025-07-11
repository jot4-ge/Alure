import json
from app.models.roupa import Roupa
from typing import Optional
import os


class ProductRecord:

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        db_dir = os.path.join(script_dir, 'db')
        os.makedirs(db_dir, exist_ok=True)
        self.file_path = os.path.join(db_dir, 'products.json')

        self.__products = []
        self.read()

    def read(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as arquivo_json:
                product_data = json.load(arquivo_json)
                self.__products = [
                    Roupa(
                        id=str(produto.get("id")),
                        nome=produto.get("nome", "None"),
                        descricao=produto.get("descricao", ""),
                        preco=float(produto.get("preco", 0.0)),
                        estoque=int(produto.get("estoque", 0)),
                        image_filename=produto.get("image_filename", ""),
                        tamanho=produto.get("tamanho", ""),
                        categoria=produto.get("categoria", "")
                    )
                    for produto in product_data
                ]
        except FileNotFoundError:
            print("ERRO read() ProductRecord: Json não achado, lista de produtos vazia na memória.")
            with open(self.file_path, "w", encoding="utf-8") as arquivo_json:
                json.dump([], arquivo_json)
            return
        except json.JSONDecodeError:
            print("ERRO read() ProductRecord: Erro ao decodificar JSON. O arquivo pode estar corrompido.")
            with open(self.file_path, "w", encoding="utf-8") as arquivo_json:
                json.dump([], arquivo_json)

    def save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as arquivo_json:
                json.dump(
                    [roupa.to_dict() for roupa in self.__products],
                    arquivo_json,
                    indent=4,
                    ensure_ascii=False
                )
        except Exception as e:
            print(f"ERRO save(): {e}")

    def add_product(self, product: Roupa) -> None:
        self.__products.append(product)
        self.save()

    def get_product(self, product_id: str) -> Optional[Roupa]:
        for product in self.__products:
            if hasattr(product, 'id') and str(product.id) == str(product_id):
                return product
        return None
    def get_product_by_name(self,product_name):
        for product in self.__products:
            if product.nome == product_name:
                return product
        return None


    def remove_product(self, product_id: str) -> bool:
        initial_len = len(self.__products)
        self.__products = [
            p for p in self.__products if not (hasattr(p, 'id') and str(p.id) == str(product_id))
        ]

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
        return self.__products[:]

    def get_NumOfProducts(self) -> int:
        return len(self.__products)
