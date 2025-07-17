import asyncio
import websockets

connected_clients = set()

async def handle_connection(websocket, path):
    connected_clients.add(websocket)
    print("Cliente conectado.")

    try:
        async for message in websocket:
            print(f"Mensagem recebida: {message}")
            # Aqui você processaria a mensagem recebida
    except websockets.exceptions.ConnectionClosed:
        print("Cliente desconectado.")
    finally:
        connected_clients.remove(websocket)

async def start_websocket_server():
    print("Servidor WebSocket ouvindo na porta 8765...")
    async with websockets.serve(handle_connection, "localhost", 8765):
        await asyncio.Future()  # Mantém o servidor rodando indefinidamente

