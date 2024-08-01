from TicTacToe import TicTacToe
from AIPlayer import aiMove

game_instance = TicTacToe()

game_instance.add_player("me", "X")
game_instance.add_player("ai", "O")

while True:
    index = int(input("Index? "))
    game_instance.play(index, "me")
    ai = aiMove(game_instance)
    print("AI plays ", ai)
    game_instance.play(ai, "ai")