scores = {"player1": 10, "player2": 0}
x=2

if ("player"+str(x+1)) in scores.keys():
    print("player"+str(x+1), scores["player"+str(x+1)])
else:
    print("player"+str(x+1), "not in dict")