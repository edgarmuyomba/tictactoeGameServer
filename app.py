import asyncio
import websockets
import json
from handlers import *

async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)

        if event["type"] == "new_game":
            await handleNewGame(websocket)
        elif event["type"] == "ai":
            await handleNewAIGame(websocket)
        elif event["type"] == "play_move":
            await handlePlayMove(websocket, event)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
