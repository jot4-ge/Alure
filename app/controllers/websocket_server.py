import asyncio
import websockets
import json


loop = asyncio.get_event_loop()

connected_clients = set()

def schedule_broadcast(message: dict):
    """
    Função SEGURA PARA CHAMAR DE OUTRAS THREADS.
    Ela agenda a transmissão da mensagem para todos os clientes.
    """
    async def _broadcast():
        if connected_clients:
            payload = json.dumps(message)
            # Envia a mensagem para todos os clientes conectados
            await asyncio.wait([client.send(payload) for client in connected_clients])

    loop.call_soon_threadsafe(asyncio.create_task, _broadcast())

# --- Lógica do Servidor WebSocket ---

async def handle_connection(websocket):
    """Gerencia uma nova conexão de cliente."""
    connected_clients.add(websocket)
    print(f"Cliente conectado. Total de clientes: {len(connected_clients)}")
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        print(f"Cliente removido. Total de clientes: {len(connected_clients)}")

async def start_websocket_server():
    """Inicia o servidor WebSocket."""
    host = "0.0.0.0"
    port = 8765
    print(f"Servidor WebSocket ouvindo em ws://{host}:{port}...")

    async with websockets.serve(handle_connection, host, port):
        await asyncio.Future()  # Mantém o servidor rodando indefinidamente