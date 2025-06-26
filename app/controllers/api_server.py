import json
from bottle import request, response
from app.controllers.ProductRecord import ProductRecord
from models.roupa import Roupa


class API:
    """
    Encapsula toda a lógica de negócio para a API de produtos.
    As rotas serão definidas em um arquivo separado e chamarão estes métodos.
    """

    def __init__(self):
        """Inicializa a API e sua conexão com o 'banco de dados' de produtos."""
        self.product_db = ProductRecord()

    @staticmethod
    def to_json(data):
        """Converte dados para uma resposta JSON com o header correto."""
        response.content_type = 'application/json'
        return json.dumps(data, default=lambda o: o.__dict__, indent=4)

    def get_all_products(self):
        """Retorna a lista de todos os produtos."""
        all_products = self.product_db.get_all_products()
        return self.to_json(all_products)

    def get_product_by_id(self, product_id):
        """Busca e retorna um produto específico pelo seu ID."""
        product = self.product_db.get_product(product_id)
        if product:
            return self.to_json(product)
        response.status = 404
        return self.to_json({"error": f"Produto com ID '{product_id}' não encontrado."})

    def create_product(self):
        """Cria um novo produto a partir dos dados da requisição."""
        try:
            data = request.json
            if not data:
                response.status = 400
                return self.to_json({"error": "Corpo da requisição não pode ser vazio."})

            new_product = Roupa(**data)

            if self.product_db.add_product(new_product):
                response.status = 201  # 201 Created
                return self.to_json(new_product)
            else:
                response.status = 409  # 409 Conflict
                return self.to_json({"error": f"Produto com ID '{new_product.id}' já existe."})

        except TypeError as e:
            response.status = 400  # 400 Bad Request
            return self.to_json({"error": f"Dados inválidos para o produto: {e}"})
        except Exception as e:
            response.status = 500  # 500 Internal Server Error
            return self.to_json({"error": f"Ocorreu um erro inesperado: {e}"})

    def update_product(self, product_id):
        """Atualiza um produto existente."""
        try:
            data = request.json
            if not data:
                response.status = 400
                return self.to_json({"error": "Corpo da requisição não pode ser vazio."})

            data['id'] = product_id
            updated_product = Roupa(**data)

            if self.product_db.edit_product(updated_product):
                return self.to_json(updated_product)
            else:
                response.status = 404
                return self.to_json({"error": f"Produto com ID '{product_id}' não encontrado para edição."})

        except TypeError as e:
            response.status = 400
            return self.to_json({"error": f"Dados inválidos para o produto: {e}"})
        except Exception as e:
            response.status = 500
            return self.to_json({"error": f"Ocorreu um erro inesperado: {e}"})

    def delete_product(self, product_id):
        """Remove um produto."""
        if self.product_db.remove_product(product_id):
            return self.to_json({"message": f"Produto com ID '{product_id}' removido com sucesso."})

        response.status = 404
        return self.to_json({"error": f"Produto com ID '{product_id}' não encontrado para remoção."})

    def handle_404_error(self, error):
        """Gera uma resposta padrão para rotas não encontradas (404)."""
        return self.to_json({'error': 'Nada aqui, verifique a URL.'})

