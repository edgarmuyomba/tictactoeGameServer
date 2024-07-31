def checkWinner(array):
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
        if array[one] and array[two] and array[three]:
            if array[one] == array[two] and array[one] == array[three]:
                return array[one]
    return None 

def availableSpots(array):
    spots = []
    for i in range(9):
        if array[i] is None:
            spots.append(i)
    return spots