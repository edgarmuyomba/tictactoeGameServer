from TicTacToe import TicTacToe
from helpers import *

def aiMove(game_instance: TicTacToe):
    if game_instance.winner is not None or game_instance.draw:
        return None
    else:
        best_move = None 
        best_score = float('-inf')

        array = game_instance.game_state

        for spot in availableSpots(array):
            array[spot] = 'O'
            score = minimax(array, 0, False)
            array[spot] = None 
            if score > best_score:
                best_move = spot 
                best_score = score 
        return best_move


def minimax(array: list, depth: int, isMax: bool):
    winner = checkWinner(array)
    if winner is not None:
        if winner == 'O':
            return 1
        return -1 
    
    freeSpots = availableSpots(array)

    if len(freeSpots) == 0:
        return 0
    
    if isMax:
        maxValue = float('-inf')
        for spot in freeSpots:
            array[spot] = 'O'
            value = minimax(array, depth + 1, False)
            array[spot] = None 
            maxValue = max(value, maxValue)
        return maxValue
    else:
        minValue = float('inf')
        for spot in freeSpots:
            array[spot] = 'X'
            value = minimax(array, depth + 1, True)
            array[spot] = None 
            minValue = min(value, minValue)
        return minValue