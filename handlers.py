from TicTacToe import TicTacToe
import json
import websockets
from AIPlayer import aiMove

game_sessions = {}


async def handleNewGame(websocket):
    game_instance = TicTacToe()
    game_instance.add_player(websocket, 'X')
    game_sessions[game_instance.id] = game_instance
    event = {
        "type": "new_game",
        "turn": game_instance.current_turn,
        "game_id": game_instance.id,
        "mark": "X"
    }

    await websocket.send(json.dumps(event))


async def handleNewAIGame(websocket):
    game_instance = TicTacToe()
    game_instance.add_player(websocket, 'X')
    game_instance.add_player('AI', 'O')
    game_instance.isAI = True
    game_sessions[game_instance.id] = game_instance
    event = {
        "type": "new_game",
        "turn": game_instance.current_turn,
        "game_id": game_instance.id,
        "mark": "X"
    }
    await websocket.send(json.dumps(event))


async def handlePlayMove(websocket, event):
    # expect the game_id and an index
    game_instance: TicTacToe = game_sessions[event['game_id']]

    # get second player and send the game state
    players = game_instance.players
    try:
        game_instance.play(event['index'], websocket)
    except RuntimeError:
        event = {
            "type": "error",
            "message": "Not your turn",
            "game_state": game_instance.game_state
        }
        await websocket.send(json.dumps(event))
    else:
        print(game_instance)
        if not game_instance.isAI:
            other_player = players[game_instance.current_turn]

            if game_instance.winner or game_instance.draw:
                if game_instance.winner:
                    # send win event
                    event = {
                        "type": "win",
                        "winner": 'X' if game_instance.current_turn == 'O' else 'O',
                        "game_state": game_instance.game_state
                    }
                else:
                    # send draw event
                    event = {
                        "type": "draw",
                        "game_state": game_instance.game_state
                    }
                websockets.broadcast(players.values(), json.dumps(event))
            else:
                # send normal move
                event = {
                    "type": "play_move",
                    "game_state": game_instance.game_state
                }
                await other_player.send(json.dumps(event))
        else:
            if game_instance.winner or game_instance.draw:
                if game_instance.winner:
                    # send win event
                    event = {
                        "type": "win",
                        "winner": 'X' if game_instance.current_turn == 'O' else 'O',
                        "game_state": game_instance.game_state
                    }
                else:
                    # send draw event
                    event = {
                        "type": "draw",
                        "game_state": game_instance.game_state
                    }
                await websocket.send(json.dumps(event))
            else:
                # wait for ai move
                index = aiMove(game_instance)
                if index is not None:
                    try:
                        game_instance.play(index, 'AI')
                        print(game_instance)
                    except RuntimeError as e:
                        pass
                    else:
                        if game_instance.winner or game_instance.draw:
                            if game_instance.winner:
                                # send win event
                                event = {
                                    "type": "win",
                                    "winner": 'X' if game_instance.current_turn == 'O' else 'O',
                                    "game_state": game_instance.game_state
                                }
                            else:
                                # send draw event
                                event = {
                                    "type": "draw",
                                    "game_state": game_instance.game_state
                                }
                            await websocket.send(json.dumps(event))
                        else:
                            # send normal move
                            event = {
                                "type": "play_move",
                                "game_state": game_instance.game_state,
                                "turn": game_instance.current_turn
                            }
                            await websocket.send(json.dumps(event))
