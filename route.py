from bottle import Bottle, redirect, static_file, HTTPResponse, TEMPLATE_PATH, request, response
from app.controllers.application import Application
from app.controllers.api_server import API
from app.controllers.api_users import UsersAPI
import os
from functools import wraps

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'app/views/html'))

app = Bottle()
api = API()
user_api = UsersAPI()
ctl = Application()

# ------------------ Login Requirement Decorator ------------------

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        session_id = request.get_cookie("session_id", secret='uma-chave-secreta-muito-forte')
        if session_id:
            user = user_api.user_db.get_current_user(session_id)
            if user:
                return f(user.to_dict_no_password(), *args, **kwargs)
        return redirect('/login')
    return wrapper

# ------------------ Static and Web Page Routes ------------------

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
@login_required
def checkout(user):
    return ctl.render_with_data("checkout", user=user)

@app.route("/carrinho", method=['GET'])
@login_required
def carrinho(user):
    return ctl.render_with_data("carrinho", user=user)

@app.route("/perfil", method=['GET'])
@login_required
def perfil(user):
    return ctl.render_with_data("perfil", user=user)

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

# ------------------ Account Routes ------------------

@app.route("/login", method=['GET'])
def login():
    return ctl.render("login")

@app.route("/register", method=['GET'])
def register():
    return ctl.render("register")

# ------------------ Admin Web Page Routes ------------------

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

# ------------------ Product API RESTful Routes ------------------

@app.route('/api/products', method='GET')
def api_get_all_products():
    return api.get_all_products()

@app.route('/api/products/<product_id>', method='GET')
def api_get_product(product_id):
    return api.get_product_by_id(product_id)

@app.route('/api/products/get-name/<product_name>', method='GET')
def api_get_product_by_name(product_name):
    return api.get_product_by_name(product_name)

@app.route('/api/products/category/<product_category>', method='GET')
def api_get_product_by_name(product_category):
    return api.get_products_by_category(product_category)

@app.route('/api/products', method='POST')
def api_create_product():
    return api.create_product()

@app.route('/api/products/<product_id>', method='PUT')
def api_update_product(product_id):
    return api.update_product(product_id)

@app.route('/api/products/<product_id>', method='DELETE')
def api_delete_product(product_id):
    return api.delete_product(product_id)

@app.route('/api/products/purchase', method='POST')
def api_process_purchase():
    return api.process_purchase()

# ------------------ Cart API Routes ------------------

@app.route('/api/cart', method='GET')
def api_get_cart():
    return user_api.get_cart()

@app.route('/api/cart/add', method='POST')
def api_add_to_cart():
    return user_api.add_to_cart()
@app.route('/api/cart/remove/<product_id>', method='DELETE')
def api_remove_from_cart(product_id):
    return user_api.remove_product_from_cart(product_id)

@app.route('/api/cart/clear', method='DELETE')
def api_clear_cart():
    return user_api.clear_cart()

# ------------------ User API RESTful Routes ------------------

@app.route('/api/users/register', method='POST')
def api_user_signin():
    return user_api.sign_in()

@app.route('/api/users/<user_id>', method='DELETE')
def api_delete_user(user_id):
    return user_api.delete_user(user_id)

@app.route('/api/users/login', method='POST')
def api_user_login():
    return user_api.login()

@app.route('/api/users/logout', method='POST')
def api_user_logout():
    return user_api.logout()

@app.route('/api/users/me', method='GET')
def api_get_user_info():
    return user_api.get_current_user_info()

# ------------------ Error Handling ------------------

@app.error(404)
def error404(_error):
    if request.path.startswith('/api/'):
        response.status = 404
        return api.to_json({"error": "Endpoint não encontrado."})
    else:
        print(f"Página não encontrada (404): {request.path}. Redirecionando...")
        return HTTPResponse(status=302, headers={'Location': '/initial_page'})
