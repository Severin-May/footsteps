import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket):
    print("Client connected")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received from client (e.g. mqtt_listener): {message}")
            # Broadcast to all browser clients
            await broadcast_to_clients(message, sender=websocket)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def broadcast_to_clients(message, sender=None):
    """Send message to all clients except the sender (e.g., MQTT sender)."""
    if connected_clients:
        await asyncio.gather(*[
            client.send(message) for client in connected_clients
            if client != sender
        ])

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
