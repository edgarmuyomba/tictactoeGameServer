import asyncio
import websockets
import json
from handlers import *
import time
import os

clients = {}

REQUEST_LIMIT = 5 
TIME_WINDOW = 10  
client_requests = {}

async def handler(websocket):
    try:
        client_id = websocket.remote_address  # or generate a unique ID
        clients[client_id] = websocket
        client_requests[client_id] = []

        # rate limiting
        now = time.time()
        client_requests[client_id] = [req for req in client_requests[client_id] if now - req < TIME_WINDOW]

        if len(client_requests[client_id]) >= REQUEST_LIMIT:
            await websocket.send("Rate limit exceeded. Try again later.")
            await websocket.close()
            return

        client_requests[client_id].append(now)

        async for message in websocket:
            event = json.loads(message)

            if event["type"] == "connect":
                await handleConnect(websocket)
            elif event["type"] == "new_game":
                await handleNewGame(websocket)
            elif event["type"] == "ai":
                await handleNewAIGame(websocket)
            elif event["type"] == "play_move":
                await handlePlayMove(websocket, event)
            elif event["type"] == "join_game":
                await handleJoinGame(websocket, event)
    except websockets.exceptions.ConnectionClosedError as e:
        print("Client closed connection!")
    except Exception as e:
        print(f"Error - {e}")
    finally:
        del clients[client_id]
        await handleClientLeft(websocket)


async def main():
    port = os.environ.get("PORT", 8001)
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
