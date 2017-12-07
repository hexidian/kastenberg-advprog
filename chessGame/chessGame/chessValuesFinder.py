from chessGame import *
from generationalLearn import *

if __name__ == "__main__":
    genSize = 10
    randomness = 10
    chessPlayerA = Species(lambda x:x**2,[1000 for i in range(12)],genSize,randomness)
    chessPlayerB = Species(lambda x:x**2,[1000 for i in range(12)],genSize,randomness)
    generations = 1 #change this value for optimizing stuff
    thisGame = Competition(chessPlayerA,chessPlayerB,Game)
    for generation in range(generations):
        scoresA = [0 for i in range(genSize)]
        scoresB = [0 for i in range(genSize)]
        for a in range(genSize):
            for b in range(genSize):
                playerA = Game(chessPlayerA.currentGeneration[a],True)
                playerB = Game(chessPlayerB.currentGeneration[b],True)

                winner = thisGame.compete(playerA,playerB)#returns a 0 if A wins and a 1 if B wins

                if winner:
                    scoresB[b] += 1
                    scoresA[a] -= 1
                else:
                    scoresA[a] += 1
                    scoresB[b] += 1
        aBest = chessPlayerA.currentGeneration[scoresA.index(max(scoresA))]
        bBest = chessPlayerB.currentGeneration[scoresB.index(max(scoresB))]

        chessPlayerA.breedGen(aBest)
        chessPlayerB.breedGen(bBest)
    print "\nthe values for player A are:",chessPlayerA.currentGeneration
    print "\nthe values for player B are:",chessPlayerB.currentGeneration
