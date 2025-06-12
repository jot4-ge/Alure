from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response, TEMPLATE_PATH
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
# Rota da página de ajuda
@app.route('/helper')
def helper(info=None):
    return ctl.render('helper')

@app.route('/')
def index():
    return redirect('/initial_page')

#-----------------------------------------------------------------------------
# Rota da página inicial
@app.route("/initial_page", method=['GET'])
def initial_page(info=None):
    return ctl.render("initial_page")

#-----------------------------------------------------------------------------
# Inicialização do servidor
if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)

