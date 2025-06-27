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
        """
        Atualiza um produto existente. Aceita dados de formulário (multipart/form-data)
        e permite a atualização parcial dos dados, incluindo a imagem.
        """
        try:
            # 1. Buscar o produto existente
            original_product = self.product_db.get_product(product_id)
            if not original_product:
                response.status = 404
                return self.to_json({"error": f"Produto com ID '{product_id}' não encontrado ou não existe no banco de dados."})

            # 2. Lidar com o upload de uma nova imagem (se houver)
            upload = request.files.get('productImage')
            new_image_filename = None
            if upload and upload.filename:
                # Validação do tipo de arquivo
                allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
                if not upload.filename.lower().endswith(allowed_extensions):
                    response.status = 400
                    return self.to_json({"error": "Formato de imagem inválido. Use PNG, JPG, JPEG, GIF ou WEBP."})

                # Gerar um nome de arquivo único e salvar
                file_extension = os.path.splitext(upload.filename)[1]
                new_image_filename = f"{uuid4()}{file_extension}"
                save_path = os.path.join(UPLOAD_FOLDER, new_image_filename)
                upload.save(save_path)

            # 3. Coletar os dados do formulário, usando os dados originais como fallback
            nome = request.forms.get('productName')
            descricao = request.forms.get('productDescription')
            preco_str = request.forms.get('productPrice')
            estoque_str = request.forms.get('productStock')
            image_filename = new_image_filename
            tamanho = request.forms.get("productSize")
            categoria = request.forms.get("productCategory")

            if (not nome) or (not descricao) or (not preco_str) or (not estoque_str) or (not tamanho) or (not categoria):
                response.status = 400
                return self.to_json({"error": "Um ou mais campos estão vazios."})
            

            # 4. Criar uma nova instância de Roupa com os dados atualizados
            updated_product = Roupa(
                id=str(product_id),
                nome=nome,
                descricao=descricao,
                preco=float(preco_str),
                estoque=int(estoque_str),
                image_filename=image_filename,
                tamanho=tamanho,
                categoria=categoria)

            # 5. Se uma nova imagem foi salva, remover a antiga
            if new_image_filename and original_product.image_filename:
                old_image_filename = original_product.image_filename
                if old_image_filename:
                    try:
                        old_image_path = os.path.join(UPLOAD_FOLDER, old_image_filename)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    except Exception as e:
                        # Logar o erro, mas não impedir a atualização do produto
                        print(f"AVISO: Não foi possível remover a imagem antiga '{old_image_filename}': {e}")

            # 6. Passar a nova instância para o método de edição do "banco de dados"
            if self.product_db.edit_product(updated_product):
                return self.to_json(updated_product)
            else:
                response.status = 500
                return self.to_json({"error": "Ocorreu um erro ao salvar as alterações do produto."})

        except ValueError as e:
            # Erro na conversão de preço/estoque
            response.status = 400
            return self.to_json({"error": f"Valor inválido fornecido: {e}"})
        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Ocorreu um erro inesperado no servidor: {e}"})

    def delete_product(self, product_id):
        """Remove um produto e sua imagem associada."""
        product_to_delete = self.product_db.get_product(product_id)
        if not product_to_delete:
            response.status = 404
            return self.to_json({"error": f"Produto com ID '{product_id}' não encontrado."})

        # Tentar remover imagem associada (se existir)
        try:
            image_path = os.path.join(UPLOAD_FOLDER, product_to_delete.image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"Erro ao tentar remover a imagem do produto: {e}")

        # Remover produto do banco
        self.product_db.remove_product(product_id)
        return self.to_json({"message": f"Produto com ID '{product_id}' removido com sucesso."})
