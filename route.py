from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response, TEMPLATE_PATH
from bottle import error, HTTPResponse
import os

# Configura o caminho dos templates
TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'app/views/html'))

app = Bottle()
ctl = Application()

#-----------------------------------------------------------------------------
# Rota para arquivos estáticos
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

#-----------------------------------------------------------------------------

@app.route('/')
def index():
    return redirect('/initial_page')

#-----------------------------------------------------------------------------
# Rota das páginas
@app.route("/initial_page", method=['GET'])
def initial_page(info=None):
    return ctl.render("initial_page")
@app.route("/checkout", method=['GET'])
def checkout(info=None):
    return ctl.render("checkout")
@app.route("/carrinho", method=['GET'])
def carrinho(info=None):
    return ctl.render("carrinho")
@app.route("/perfil", method=['GET'])
def perfil(info=None):
    return ctl.render("perfil")
@app.route("/admin", method=['GET'])
def admin(info=None):
    return ctl.render("admin")

#-----------------------------------------------------------------------------
# Admin Routes

@app.route("admin/add-product", method=['GET'])
def add_product():
    # In a real implementation, you would pass any necessary data to the template
    return ctl.render("admin_pages/add_product", isAdmin = True)

@app.route("admin/remove-product", method=['GET'])
def remove_product():
    # In a real implementation, you would fetch the list of products from the database
    return ctl.render("admin_pages/remove_product", isAdmin = True)

@app.route("admin/edit-product", method=['GET'])
def edit_product(product_id):
    # In a real implementation, you would fetch the product details using product_id
    return ctl.render("admin_pages/edit_product", isAdmin = True)

@app.route("admin/view-products", method=['GET'])
def view_products():
    # In a real implementation, you would fetch the paginated list of products
    return ctl.render("admin_pages/view_products", isAdmin = True)

#-----------------------------------------------------------------------------
# Se tentar abrir uma pagina que não existe redireciona para a pagina inicial

@app.error(404)
def error404(error_):
    print(f"Erro = {error_}")
    return HTTPResponse(status=302, headers={'Location': '/initial_page'})
#-----------------------------------------------------------------------------

# Inicialização do servidor
if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)

