from bottle import Bottle, redirect, static_file, HTTPResponse, TEMPLATE_PATH
from app.controllers.application import Application
import os
import admin_routes

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'app/views/html'))

app = Bottle()
ctl = Application()

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

@app.error(404)
def error404(error_):
    print(f"Erro = {error_}")
    return HTTPResponse(status=302, headers={'Location': '/initial_page'})
