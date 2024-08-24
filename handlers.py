from TicTacToe import TicTacToe
import json
from AIPlayer import aiMove
import secrets

game_sessions = {}

async def handleConnect(websocket):
    event = {
        "type": "connect"
    }
    await websocket.send(json.dumps(event))


async def handleNewGame(websocket):
    game_instance = TicTacToe()
    player_id = secrets.token_urlsafe(8)
    game_instance.add_player(player_id, 'X')
    game_instance.player_connections[player_id] = websocket
    game_sessions[game_instance.id] = game_instance
    event = {
        "type": "new_game",
        "turn": game_instance.current_turn,
        "game_id": game_instance.id,
        "mark": "X",
        "player_id": player_id
    }

    await websocket.send(json.dumps(event))


async def handleNewAIGame(websocket):
    game_instance = TicTacToe()
    player_id = secrets.token_urlsafe(8)
    game_instance.add_player(player_id, 'X')
    game_instance.player_connections[player_id] = websocket
    game_instance.add_player('AI', 'O')
    game_instance.isAI = True
    game_sessions[game_instance.id] = game_instance
    event = {
        "type": "new_game",
        "turn": game_instance.current_turn,
        "game_id": game_instance.id,
        "mark": "X",
        "player_id": player_id
    }
    await websocket.send(json.dumps(event))


async def handlePlayMove(websocket, event):
    # expect the game_id and an index
    game_instance: TicTacToe = game_sessions.get(event['game_id'], None)
    player_id = event['player_id']

    # get second player and send the game state
    try:
        game_instance.play(event['index'], player_id)
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
            other_player = game_instance.player_connections.get(
                game_instance.players.get(game_instance.current_turn, None), None)

            if other_player is not None:
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
                    player_sockets = game_instance.player_connections.values()
                    for player in player_sockets:
                        await player.send(json.dumps(event))
                    del game_sessions[game_instance.id]
                else:
                    # send normal move
                    event = {
                        "type": "play_move",
                        "game_state": game_instance.game_state,
                        "turn": game_instance.current_turn
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
                        # print(game_instance)
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


async def handleJoinGame(websocket, event):
    # expect the game_id and an index
    game_instance: TicTacToe = game_sessions.get(event['game_id'], None)
    if game_instance is not None:
        try:
            player_id = secrets.token_urlsafe(8)
            game_instance.add_player(player_id, 'O')
            game_instance.player_connections[player_id] = websocket
        except RuntimeError as e:
            event = {
                "type": "error",
                "message": "Game session full!"
            }
            await websocket.send(json.dumps(event))
        else:

            event = {
                "type": "new_game",
                "turn": game_instance.current_turn,
                "game_id": game_instance.id,
                "mark": "O",
                "player_id": player_id,
                "game_state": game_instance.game_state
            }
            await websocket.send(json.dumps(event))

            first_player_id = game_instance.players['X']
            first_player_ws = game_instance.player_connections[first_player_id]
            await first_player_ws.send(json.dumps({"type": "player_joined", "game_state": game_instance.game_state}))

    else:
        event = {
            "type": "error",
            "message": f"Session with ID - {event['game_id']} does not exist!"
        }
        await websocket.send(json.dumps(event))


async def handleClientLeft(websocket):
    game_id = None
    # find the game instance
    for id, game_instance in game_sessions.items():
        if len(game_instance.player_connections) == 2:
            for player_id, _websocket in game_instance.player_connections.items():
                if _websocket != websocket:
                    # send other player notification
                    event = {
                        "type": "player_left"
                    }
                    await _websocket.send(json.dumps(event))
                    game_id = id 
                    
    if game_id is not None:
        del game_sessions[game_id]
