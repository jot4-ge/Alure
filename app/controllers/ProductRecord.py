from app.models.user_account import UserAccount
import json
from models.roupa import Roupa


class ProductRecord():
    """Banco de dados JSON para o recurso dos Produtos"""

    def __init__(self):

        self.__products = []

    def read(self):
        try:
            with open("app/controllers/db/products.json", "r") as arquivo_json:
                product_data = json.load(arquivo_json)
                self.__products = [Roupa(**roupa_data) for roupa_data in product_data]
        except FileNotFoundError:
            print("ERRO read() DataRecord: Json não achado, lista de produtos vazia na memoria.")

