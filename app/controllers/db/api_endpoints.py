# api_server.py
import json
from bottle import route, run, request, response, error
from app.controllers.ProductRecord import ProductRecord
from models.roupa import Roupa

# Instancia o nosso gerenciador de produtos.
# Ele vai carregar os dados do JSON ao ser iniciado.
product_db = ProductRecord()


# --- Helpers ---
def to_json(data):
    """Converte dados para uma resposta JSON com o header correto."""
    response.content_type = 'application/json'
    # Usamos um default para lidar com objetos que não são serializáveis por padrão
    return json.dumps(data, default=lambda o: o.__dict__, indent=4)


# --- Rotas da API ---

@route('/products', method='GET')
def get_all():
    """Endpoint para listar todos os produtos."""
    all_products = product_db.get_all_products()  # Usando o novo método
    return to_json(all_products)


@route('/products/<product_id>', method='GET')
def get_one(product_id):
    """Endpoint para buscar um produto específico pelo ID."""
    product = product_db.get_product(product_id)
    if product:
        return to_json(product)
    response.status = 404
    return to_json({"error": f"Produto com ID '{product_id}' não encontrado."})


@route('/products', method='POST')
def create_product():
    """Endpoint para adicionar um novo produto."""
    try:
        data = request.json
        if not data:
            response.status = 400
            return to_json({"error": "Corpo da requisição não pode ser vazio."})

        # Cria uma instância de Roupa a partir do JSON recebido
        new_product = Roupa(**data)

        if product_db.add_product(new_product):
            response.status = 201  # 201 Created
            return to_json(new_product)
        else:
            response.status = 409  # 409 Conflict
            return to_json({"error": f"Produto com ID '{new_product.id}' já existe."})

    except TypeError as e:
        response.status = 400  # 400 Bad Request
        return to_json({"error": f"Dados inválidos para o produto: {e}"})
    except Exception as e:
        response.status = 500  # 500 Internal Server Error
        return to_json({"error": f"Ocorreu um erro inesperado: {e}"})


@route('/products/<product_id>', method='PUT')
def update_product(product_id):
    """Endpoint para editar um produto existente."""
    try:
        data = request.json
        if not data:
            response.status = 400
            return to_json({"error": "Corpo da requisição não pode ser vazio."})

        # Garante que o ID na URL seja o mesmo do corpo da requisição
        data['id'] = product_id
        updated_product = Roupa(**data)

        if product_db.edit_product(updated_product):
            return to_json(updated_product)
        else:
            response.status = 404
            return to_json({"error": f"Produto com ID '{product_id}' não encontrado para edição."})

    except TypeError as e:
        response.status = 400
        return to_json({"error": f"Dados inválidos para o produto: {e}"})
    except Exception as e:
        response.status = 500
        return to_json({"error": f"Ocorreu um erro inesperado: {e}"})


@route('/products/<product_id>', method='DELETE')
def delete_product(product_id):
    """Endpoint para remover um produto."""
    if product_db.remove_product(product_id):
        return to_json({"message": f"Produto com ID '{product_id}' removido com sucesso."})

    response.status = 404
    return to_json({"error": f"Produto com ID '{product_id}' não encontrado para remoção."})


# --- Tratamento de Erros Genéricos ---
@error(404)
def error404(error):
    return to_json({'error': 'Nada aqui, verifique a URL.'})


# --- Iniciar o Servidor ---
if __name__ == '__main__':
    # host='0.0.0.0' permite acesso de outras máquinas na rede
    # reloader=True reinicia o servidor automaticamente quando o código muda (ótimo para desenvolvimento)
    run(host='localhost', port=8080, debug=True, reloader=True)