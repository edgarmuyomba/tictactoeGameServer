# TicTacToe Game Server
This is a simple implementation for a multiplayer game ([TicTacToe](https://playtictactoe.org/)) server using [python websockets](https://websockets.readthedocs.io/). It handles the game-logic and communication between clients and the server to ensure real-time game play. It also provides the option to play against an AI agent.
The front-end segment for this game can be found [here](https://github.com/edgarmuyomba/tic-tac-toe-v2).

## Events
1. ### Connect
   
   This is used to establish a connection between a client and a server

   Request
   ```json
    {
        "type": "connect"
    }
   ```
   Response
   ```json
    {
        "type": "connect"
    }
   ```
2. ### New Game
 
   This is used by the client to create a new game on the web server

   Request
    ```json
        {
            "type": "new_game",
        }
    ```

    Response
    ```json
        {
            "type": "new_game",
            "turn": "<game_session.current_turn>",
            "game_id": "<game_session.game_id>",
            "mark": "<player's_mark>",
            "player_id": "<player's_id>"
        }
    ```
4. ### AI
   
   This triggers the creation of a new game against the AI agent

   Request
    ```json
        {
            "type": "ai",
        }
    ```

    Response
    ```json
        {
            "type": "new_game",
            "turn": "<game_session.current_turn>",
            "game_id": "<game_session.game_id>",
            "mark": "X",
            "player_id": "<player's_id>"
        }
    ```
5. ### Play Move
   
   This is used to trigger a game play move in the specific game session. The event is used to update the game state on the server and if playing against an AI agent, a response is obtained and sent back otherwise, the event is sent to the second player in the game session ( if any ).

   Request
    ```json
        {
            "type": "play_move",
            "game_id": "<game_session.game_id>",
            "player_id": "<player's_id>",
            "index": "<move_index>"
        }
    ```

    Response
    
    - If the move that has been played results in a win
        ```json
            {
                "type": "win",
                "winner": "<game_session.current_turn>",
                "game_state": "<game_session.game_state>"
            }
        ```
    - If the move resulted in a draw
        ```json
            {
                "type": "draw",
                "game_state": "<game_session.game_state>"
            }
        ```
    - Otherwise a normal move is sent
        ```json
            {
                "type": "play_move",
                "turn": "<game_session.current_turn>",
                "game_state": "<game_session.game_state>"
            }
        ```

6. ### Join Game
   
   This is used by a player to join an existing game session using the `game_id`

   Request
   ```json
    {
        "type": "join_game",
        "game_id": "<game_session.game_id>"
    }
   ```

   Response
   - If the game_id is valid and the game session exists?
        ```json
        {
                "type": "new_game",
                "turn": "<game_session.current_turn>",
                "game_id": "<game_session.game_id>",
                "mark": "<player's_mark>",
                "player_id": "<player's_id>",
                "game_state": "<game_session.game_state>"
        }
        ```

## Error Handling
- In case of any error, a specialised event is sent out and displayed to the client in the form
    ```json
    {
        "type": "error",
        "message": "<error_message>"
    }
    ```
    These can occur in cases such as 
    - A client trying to join a game session with maximum number of players
    - A client trying to join a game session that doesnt exist
    - A client trying to play a move when its not their turn

- In the event that duing a Two-player game session one of the clients leaves, still, an event is sent out to the second player and the game_session terminated.
    ```json
    {
        "type": "player_left"
    }
    ```