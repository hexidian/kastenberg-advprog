from chessGame import *
from generationalLearn import *

if __name__ == "__main__":
    genSize = 10
    randomness = 10
    chessPlayerA = Species(lambda x:x**2,[1000 for i in range(12)],genSize,randomness)
    chessPlayerB = Species(lambda x:x**2,[1000 for i in range(12)],genSize,randomness)
    generations = 1 #change this value for optimizing stuff
    thisGame = Competition(chessPlayerA,chessPlayerB,Game)
    for generation in generations:
        scoresA = [0 for i in range(genSize)]
        scoresB = [0 for i in range(genSize)]
        for a in range(genSize):
            for b in range(genSize):
                playerA = chessPlayerA.currentGeneration[a]
                playerB = chessPlayerB.currentGeneration[b]

                winner = thisGame.compete(playerA,playerB)#returns a 0 if A wins and a 1 if B wins

                if winner:
                    scoresB[b] += 1
                    scoresA[a] -= 1
                else:
                    scoresA[a] += 1
                    scoresB[b] += 1
        #now need to test it and breed them; I will find the index of the best score and then do Species.breedGeneration(best) with the best one
