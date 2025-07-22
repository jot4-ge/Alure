import json
import os
import traceback
import random
import string
import asyncio
import websockets
from uuid import uuid4
from bottle import request, response
from app.controllers.ProductRecord import ProductRecord
from app.models.roupa import Roupa

# --- Diretório de Upload ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'app', 'static', 'img', 'clothes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class API:
    def __init__(self):
        self.product_db = ProductRecord()

    def _generate_unique_product_id(self, length: int = 5) -> str:
        chars = string.ascii_lowercase + string.digits
        while True:
            candidate_id = ''.join(random.choices(chars, k=length))
            if not self.product_db.get_product(candidate_id):
                return candidate_id

    @staticmethod
    def to_json(data: any) -> str:
        response.content_type = 'application/json'
        return json.dumps(
            data,
            default=lambda o: o.to_dict() if hasattr(o, 'to_dict') else o.__dict__,
            indent=4,
            ensure_ascii=False
        )

    def get_all_products(self):
        all_products = self.product_db.get_all_products()
        return self.to_json(all_products)

    def get_product_by_id(self, product_id):
        product = self.product_db.get_product(product_id)
        if product:
            return self.to_json(product)
        response.status = 404
        return self.to_json({"error": f"Produto com ID '{product_id}' não encontrado."})

    def get_product_by_name(self, product_name):
        product = self.product_db.get_product_by_name(product_name)
        if product:
            return self.to_json(product)
        response.status = 404
        return self.to_json({"error": f"Produto com nome '{product_name}' não encontrado."})

    def get_products_by_category(self, categoria):
        produtos = self.product_db.get_products_by_category(categoria)
        return self.to_json(produtos)

    def create_product(self):
        try:
            nome = request.forms.get('productName')
            descricao = request.forms.get('productDescription')
            preco_str = request.forms.get('productPrice').replace(",", ".")
            estoque_str = request.forms.get('productStock')
            tamanho = request.forms.get('productSize')
            categoria = request.forms.get('productCategory')
            upload = request.files.get('productImage')

            if not (upload and upload.filename):
                response.status = 400
                return self.to_json({"error": "Nenhuma imagem foi enviada."})

            allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
            if not upload.filename.lower().endswith(allowed_extensions):
                response.status = 400
                return self.to_json({"error": "Formato de imagem inválido."})

            file_extension = os.path.splitext(upload.filename)[1]
            image_filename = f"{uuid4()}{file_extension}"
            save_path = os.path.join(UPLOAD_FOLDER, image_filename)
            upload.save(save_path)

            if not all([nome, descricao, preco_str, estoque_str, tamanho, categoria]):
                os.remove(save_path)
                response.status = 400
                return self.to_json({"error": "Todos os campos são obrigatórios."})

            product_id = self._generate_unique_product_id()

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
            response.status = 201
            return self.to_json(new_product)
        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Erro no servidor: {e}"})

    def update_product(self, product_id):
        try:
            original_product = self.product_db.get_product(product_id)
            if not original_product:
                response.status = 404
                return self.to_json({"error": "Produto não encontrado."})

            upload = request.files.get('productImage')
            new_image_filename = None
            if upload and upload.filename:
                allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
                if not upload.filename.lower().endswith(allowed_extensions):
                    response.status = 400
                    return self.to_json({"error": "Formato de imagem inválido."})

                file_extension = os.path.splitext(upload.filename)[1]
                new_image_filename = f"{uuid4()}{file_extension}"
                save_path = os.path.join(UPLOAD_FOLDER, new_image_filename)
                upload.save(save_path)

            nome = request.forms.get('productName')
            descricao = request.forms.get('productDescription')
            preco_str = request.forms.get('productPrice')
            estoque_str = request.forms.get('productStock')
            tamanho = request.forms.get("productSize")
            categoria = request.forms.get("productCategory")

            image_filename = new_image_filename if new_image_filename else original_product.image_filename

            if not all([nome, descricao, preco_str, estoque_str, tamanho, categoria]):
                response.status = 400
                return self.to_json({"error": "Campos obrigatórios ausentes."})

            updated_product = Roupa(
                id=str(product_id),
                nome=nome,
                descricao=descricao,
                preco=float(preco_str),
                estoque=int(estoque_str),
                image_filename=image_filename,
                tamanho=tamanho,
                categoria=categoria
            )

            if new_image_filename and original_product.image_filename:
                old_path = os.path.join(UPLOAD_FOLDER, original_product.image_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)

            if self.product_db.edit_product(updated_product):
                return self.to_json(updated_product)
            else:
                response.status = 500
                return self.to_json({"error": "Erro ao salvar alterações."})
        except ValueError as e:
            response.status = 400
            return self.to_json({"error": str(e)})
        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Erro inesperado: {e}"})

    def delete_product(self, product_id):
        product_to_delete = self.product_db.get_product(product_id)
        if not product_to_delete:
            response.status = 404
            return self.to_json({"error": f"Produto com ID '{product_id}' não encontrado."})

        try:
            image_path = os.path.join(UPLOAD_FOLDER, product_to_delete.image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"Erro ao remover imagem: {e}")

        self.product_db.remove_product(product_id)
        return self.to_json({"message": f"Produto com ID '{product_id}' removido com sucesso."})

    def buy_product(self, product_id):
        try:
            product = self.product_db.get_product(product_id)
            if not product:
                response.status = 404
                return self.to_json({"error": "Produto não encontrado."})

            if product.estoque <= 0:
                response.status = 400
                return self.to_json({"error": "Produto esgotado."})

            product.estoque -= 1
            self.product_db.edit_product(product)

            if product.estoque == 0:
                asyncio.run(self._emit_websocket_estoque_esgotado(product.id, product.nome))

            return self.to_json({"message": "Compra realizada com sucesso.", "produto": product.to_dict()})
        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Erro ao processar compra: {e}"})

    async def _emit_websocket_estoque_esgotado(self, product_id, product_name):
        uri = "ws://localhost:8765"
        try:
            async with websockets.connect(uri) as websocket:
                payload = {
                    "event": "estoque_esgotado",
                    "product_id": product_id,
                    "message": f"O produto '{product_name}' esgotou!"
                }
                await websocket.send(json.dumps(payload))
        except Exception as e:
            print(f"[WebSocket] Erro ao notificar: {e}")

        
    
