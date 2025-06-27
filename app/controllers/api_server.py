import json
import os
import traceback
from uuid import uuid4
from bottle import request, response
from app.controllers.ProductRecord import ProductRecord
from app.models.roupa import Roupa

# --- Configuração do Diretório de Upload ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'app', 'static', 'img', 'clothes')

# Garante que o diretório de upload exista. Se não existir, ele será criado.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class API:
    """
    Encapsula toda a lógica de negócio para a API de produtos.
    """

    def __init__(self):
        """Inicializa a API e sua conexão com o 'banco de dados' de produtos."""
        self.product_db = ProductRecord()

    @staticmethod
    def to_json(data):
        """Converte dados para uma resposta JSON com o header correto."""
        response.content_type = 'application/json'
        # Adicionado um to_dict() para serializar objetos de forma mais controlada, se o método existir.
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
        """Cria um novo produto a partir de um formulário com upload de imagem."""
        try:
            nome = request.forms.get('productName')
            descricao = request.forms.get('productDescription')
            preco_str = request.forms.get('productPrice').replace(",", ".")
            estoque_str = request.forms.get('productStock')
            tamanho = request.forms.get('productSize')
            categoria = request.forms.get('productCategory')

            # 2. Lidar com o upload do arquivo
            upload = request.files.get('productImage')
            if not (upload and upload.filename):
                response.status = 400
                return self.to_json({"error": "Nenhuma imagem foi enviada."})

            # Validação do tipo de arquivo
            allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
            if not upload.filename.lower().endswith(allowed_extensions):
                response.status = 400
                return self.to_json({"error": "Formato de imagem inválido. Use PNG, JPG, JPEG, GIF ou WEBP."})

            # Gerar um nome de arquivo único para evitar conflitos e problemas de segurança
            file_extension = os.path.splitext(upload.filename)[1]
            image_filename = f"{uuid4()}{file_extension}"
            save_path = os.path.join(UPLOAD_FOLDER, image_filename)

            # Salvar o arquivo no disco
            upload.save(save_path)

            # 3. Validar e converter os dados de texto
            if not all([nome, descricao, preco_str, estoque_str, tamanho, categoria]):
                os.remove(save_path)  # Remove a imagem se outros dados estiverem faltando
                response.status = 400
                return self.to_json({"error": "Todos os campos de texto são obrigatórios."})


            # 4. Criar a instância de Roupa e salvar
            product_id = self.product_db.get_NumOfProducts() + 1

            new_product = Roupa(
                id=str(product_id),
                nome=nome,
                descricao=descricao,
                preco=float(preco_str),
                estoque=int(estoque_str),
                image_filename=image_filename,
                tamanho=tamanho,
                categoria=categoria
            )

            self.product_db.add_product(new_product)
            response.status = 201  # 201 Created
            return self.to_json(new_product)
        except Exception as e:
            # Log do erro completo no console do servidor para depuração
            traceback.print_exc()
            response.status = 500  # 500 Internal Server Error
            return self.to_json({"error": f"Ocorreu um erro inesperado no servidor: {e}"})

    def update_product(self, product_id):
        """Atualiza um produto existente."""
        # Nota: O upload de imagem na edição não está implementado aqui.
        # Seria necessário usar a mesma lógica de multipart/form-data.
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
        """Remove um produto e sua imagem associada."""
        product_to_delete = self.product_db.get_product(product_id)
        if not product_to_delete:
            response.status = 404
