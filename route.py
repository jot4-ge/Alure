from bottle import Bottle, redirect, static_file, HTTPResponse, TEMPLATE_PATH, request,response
from app.controllers.application import Application
from app.controllers.api_server import API
from app.controllers.api_users import UsersAPI
import os
TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'app/views/html'))

app = Bottle()
api = API()
user_api = UsersAPI()
ctl = Application()

# ---------------- Static and Web Page Routes -----------------------

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/')
def index():
    return redirect('/initial_page')

@app.route("/initial_page", method=['GET'])
def initial_page():
    return ctl.render("initial_page")

@app.route("/checkout", method=['GET'])
def checkout():
    return ctl.render("checkout")

@app.route("/carrinho", method=['GET'])
def carrinho():
    return ctl.render("carrinho")

@app.route("/perfil", method=['GET'])
def perfil():
    return ctl.render("perfil")

@app.route("/admin", method=['GET'])
def admin():
    return ctl.render("admin")

@app.route("/streetwear", method=['GET'])
def streetwear():
    return ctl.render("streetwear")

@app.route("/acessorios", method=['GET'])
def acessorios():
    return ctl.render("acessorios")

@app.route("/camisetas", method=['GET'])
def camisetas():
    return ctl.render("camisetas")

@app.route('/favicon.ico', method='GET')
def favicon():
    return static_file('favicon.ico', root='./app/static/img/')

# ---------------- Admin Web Page Routes -----------------------

@app.route("/admin/add-product", method=["GET"])
def add_product():
    return ctl.render("add_product", isAdmin=True)

@app.route("/admin/remove-product", method=["GET"])
def remove_product():
    return ctl.render("remove_product", isAdmin=True)

@app.route("/admin/edit-product", method=["GET"])
def edit_product():
    return ctl.render("edit_product", isAdmin=True)

@app.route("/admin/view-products", method=["GET"])
def view_products():
    return ctl.render("view_products", isAdmin=True)

# ----------------  Product API RESTful Routes -----------------------

@app.route('/api/products', method='GET')
def api_get_all_products():
    """Rota para listar todos os produtos."""
    return api.get_all_products()

@app.route('/api/products/<product_id>', method='GET')
def api_get_product(product_id):
    """Rota para buscar um produto específico pelo ID."""
    return api.get_product_by_id(product_id)

@app.route('/api/products/get-name/<product_name>', method='GET')
def api_get_product(product_name):
    """Rota para buscar um produto específico pelo nome."""
    return api.get_product_by_name(product_name)

@app.route('/api/products', method='POST')
def api_create_product():
    """Rota para adicionar um novo produto."""
    return api.create_product()

@app.route('/api/products/<product_id>', method='PUT')
def api_update_product(product_id):
    """Rota para editar um produto existente."""
    return api.update_product(product_id)

@app.route('/api/products/<product_id>', method='DELETE')
def api_delete_product(product_id):
    """Rota para remover um produto."""
    return api.delete_product(product_id)

# ---------------- User API RESTful Routes -----------------------

@app.route('/api/users/signin', method='POST')
def api_user_signin():
    """Rota para registrar (criar) um novo usuário."""
    return user_api.sign_in()

@app.route('/api/users/<user_id>', method='DELETE')
def api_delete_user(user_id):
    """Rota para deletar um usuario."""
    return user_api.delete_user(user_id)

@app.route('/api/users/login', method='POST')
def api_user_login():
    """Rota para autenticar um usuário e obter uma sessão."""
    return user_api.login()

@app.route('/api/users/logout', method='POST')
def api_user_logout():
    """Rota para desconectar um usuário (invalidar sessão)."""
    return user_api.logout()

@app.route('/api/users/me', method='GET')
def api_get_user_info():
    """Rota para obter informações do usuário logado."""
    return user_api.get_current_user_info()

# ---------------- Error Handling -----------------------

@app.error(404)
def error404(error_):
    """
    Trata erros 404. Retorna JSON para rotas de API
    e redireciona para rotas de páginas web.
    """
    # O handle de erro da API de produtos pode ser generalizado ou
    # você pode criar um específico para a API de usuários.
    # Por enquanto, usaremos o da API de produtos como exemplo.
    if request.path.startswith('/api/'):
        response.status = 404
        return api.to_json({"error": "Endpoint não encontrado."})
    else:
        print(f"Página não encontrada (404): {request.path}. Redirecionando...")
        return HTTPResponse(status=302, headers={'Location': '/initial_page'})