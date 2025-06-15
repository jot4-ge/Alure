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
# Rota da página inicial
@app.route("/initial_page", method=['GET'])
def initial_page(info=None):
    return ctl.render("initial_page")

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

