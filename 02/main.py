with open('input.txt') as f:
    lines = f.readlines()

encoding = {
    'X': 'R',
    'Y': 'P',
    'Z': 'S',
    'A': 'R',
    'B': 'P',
    'C': 'S'
}
encoding2 = {
    'X': "LOSE",
    'Y': "DRAW",
    'Z': "WIN"
}
points = {
    'R': 1,
    'P': 2,
    'S': 3
}
POINTS_WIN = 6
POINTS_DRAW = 3
POINTS_LOST = 0
win_conditions = [('R', 'S'), ('S', 'P'), ('P', 'R')]
total_score = 0
for line in lines:
    opponent, outcome = line.split(' ')
    opponent = encoding[opponent.strip()]
    outcome = encoding2[outcome.strip()]
    if outcome == 'WIN':
        outcome_score = POINTS_WIN
        yourself = [win for (win, lose)
                    in win_conditions if lose == opponent][0]
    elif outcome == 'LOSE':
        outcome_score = POINTS_LOST
        yourself = [lose for (win, lose)
                    in win_conditions if win == opponent][0]
    else:
        outcome_score = POINTS_DRAW
        yourself = opponent
    total_score += outcome_score + points[yourself]


print(total_score)
