import secrets

class TicTacToe:
    def __init__(self):
        self.id = secrets.token_urlsafe(6)
        self.players = {'X': None, 'O': None}
        self.game_state = [None] * 9
        self.current_turn = 'X'
        self.winner = None 
        self.draw = False
        self.isAI = False

    def add_player(self, websocket, mark):
        if self.players['X'] and self.players['O']:
            raise RuntimeError("Game session full!")
        self.players[mark] = websocket

    def play(self, index, websocket):
        if self.players[self.current_turn] != websocket:
            raise RuntimeError("Not your turn")
        
        self.game_state[index] = self.current_turn

        if self.winner is None and self.last_player_won:
            self.winner = self.current_turn
        
        if None not in self.game_state:
            self.draw = True

        self.current_turn = 'O' if self.current_turn == 'X' else 'X'

    @property
    def last_player_won(self):
        win_combos = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]
        for combo in win_combos:
            one, two, three = combo
            if self.game_state[one] and self.game_state[two] and self.game_state[three]:
                if self.game_state[one] == self.game_state[two] and self.game_state[one] == self.game_state[three]:
                    return True 
        return False
    
    @property
    def available_spots(self):
        spots = []
        for i in range(9):
            if self.game_state[i] is None:
                spots.append(i)
        return spots
    
    def __str__(self):
        return f"\nGame state - {self.game_state}\nWinner - {self.winner}\nDraw - {self.draw}\nTurn - {self.current_turn}"