from bottle import Bottle, redirect, static_file, HTTPResponse, TEMPLATE_PATH, request
from app.controllers.application import Application
from app.controllers.api_server import API
import os
TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'app/views/html'))

app = Bottle()
api = API()
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

# ---------------- API RESTful Routes -----------------------

@app.route('/api/products', method='GET')
def api_get_all_products():
    """Rota para listar todos os produtos."""
    return api.get_all_products()

@app.route('/api/products/<product_id>', method='GET')
def api_get_product(product_id):
    """Rota para buscar um produto específico pelo ID."""
    return api.get_product_by_id(product_id)

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

# ---------------- Error Handling -----------------------

@app.error(404)
def error404(error_):
    """
    Trata erros 404. Retorna JSON para rotas de API
    e redireciona para rotas de páginas web.
    """
    if request.path.startswith('/api/'):
        return api.handle_404_error(error_)
    else:
        print(f"Página não encontrada (404): {request.path}. Redirecionando...")
        return HTTPResponse(status=302, headers={'Location': '/initial_page'})