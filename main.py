import threading
import asyncio
from bottle import run
from route import app
from app.controllers.websocket_server import start_websocket_server, loop


def run_websocket_server():
    """
    Define o loop de eventos para esta thread e inicia o servidor WebSocket.
    """
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_websocket_server())


if __name__ == '__main__':
    # 1. Cria uma thread para o servidor WebSocket
    websocket_thread = threading.Thread(target=run_websocket_server)
    # Define como 'daemon' para que a thread feche junto com o programa principal
    websocket_thread.daemon = True

    # 2. Inicia a thread do WebSocket em segundo plano
    websocket_thread.start()
    print("Thread do WebSocket iniciada.")

    # 3. Inicia o servidor Bottle na thread principal
    print("Servidor HTTP (Bottle) iniciando na porta 8080...")
    run(app, host='0.0.0.0', port=8080, debug=True, reloader=False)