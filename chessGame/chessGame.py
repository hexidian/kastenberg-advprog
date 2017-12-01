#NOTE ALL KNIGHTS ARE REFERRED TO WITH THE LETTER N BECAUSE KING STARTS WITH K

class Board:

    def __init__(self):

        self.pieceStartOrder = ["R","N","B","K","Q","B","N","R"]

        self.grid = self.makeGrid()

    def makeGrid(self):

        grid = [["" for i in range(8)] for i in range(8)] #makes an 8 by 8 grid

        for i in range(8):
            grid[1][i] = "Pw"   #makes the second row full of white pawns
            grid[6][i] = "Pb"   #makes the second row from the back full of black pawns

            grid[0][i] = self.pieceStartOrder[i]+"w"    #fills it up with the pieces in the correct order
            grid[7][i] = self.pieceStartOrder[i]+"b"    #same as above but the black pieces

        return grid

    def isCheck(self,whoseTurn):

        #row and column are the row and column of the piece that I am finding the possible moves of

        #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]

        posMoves = self.possibleColorMoves(("w" if whoseTurn == "b" else "b"))

        for i in range(len(posMoves)):
            move = posMoves[i][:]
            if move[1] == "P":
                pawnThreat = self.pawnThreatening(move[2],move[3])
                posMoves[i] = [move[0],move[1],move[2],move[3],pawnThreat[0][0],pawnThreat[0][1]]
                if len(pawnThreat) > 1:#if there is a second possible move for the pawns
                    posMoves.append([move[0],move[1],move[2],move[3],pawnThreat[1][0],pawnThreat[1][1]])

        #posMoves has now been transformed into a list of moves which are not all possible,
        #but do represent the threatened spaces

        threatenedTiles = [[move[4],move[5]] for move in posMoves] #creates a list of all the threatened tiles

        for row in range(8):
            for column in range(8):
                if (self.grid[row][column]=="K"+whoseTurn) and ([row,column] in threatenedTiles):
                    return True

        return False

    def isCheckmate(self,whoseTurn):

        if not self.isCheck(whoseTurn):
            return False

        posMoves = self.possibleColorMoves(whoseTurn)

        for move in posMoves:
            self.movePiece(move)
            if not self.isCheck(whoseTurn):     #if the move has fixed the situation
                self.undoMove()
                print "one possible move is",move
                print "\nCHECK\n"
                return False
            self.undoMove()

        return True

    def undoMove(self):

        self.grid = self.lastGrid[:][:]

    def pawnThreatening(self,row,column):
        color = self.grid[row][column][1]
        returnList = []
        if color == "w":
            try:
                if self.grid[row+1][column-1] == "just get IndexError":
                    pass
                returnList.append([row+1,column-1])
            except IndexError:
                pass

            try:
                if self.grid[row+1][column+1] == "just get IndexError":
                    pass
                returnList.append([row+1,column+1])
            except IndexError:
                pass

        else:
            try:
                if self.grid[row-1][column-1] == "just get IndexError":
                    pass
                returnList.append([row-1,column-1])
            except IndexError:
                pass

            try:
                if self.grid[row-1][column+1] == "just get IndexError":
                    pass
                returnList.append([row-1,column+1])
            except IndexError:
                pass

        return returnList


    def possiblePieceMoves(self,row,column):#all of the possible moves that a given piece can make
        pieceType = self.grid[row][column][0]
        pieceColor = self.grid[row][column][1]

        baseMove = [pieceColor,pieceType,row,column]

        foundMoves = []

        for rowTo in range(8):
            for columnTo in range(8):
                testingMove = baseMove[:]
                testingMove.append(rowTo)
                testingMove.append(columnTo)
                if self.isLegalMove(testingMove):
                    foundMoves.append(testingMove)

        return foundMoves

    def possibleColorMoves(self,color):#all of the possible moves that a player (specified by the color) can make
        foundMoves = []

        for row in range(8):
            for column in range(8):
                try:
                    if self.grid[row][column][1]==color:
                        foundMoves.extend(self.possiblePieceMoves(row,column))
                except:
                    pass

        return foundMoves


    def isLegalMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        pieceType = move[1]

        if not (pieceType+move[0] == self.grid[move[2]][move[3]]): #the piece has to be there
            return False

        if move[2]==move[4] and move[3]==move[5]: return False

        if pieceType == "P":
            return self.isLegalPawnMove(move)

        if pieceType == "N":
            return self.isLegalKnightMove(move)

        if pieceType == "R":
            return self.isLegalRookMove(move)

        if pieceType == "K":
            return self.isLegalKingMove(move)

        if pieceType == "B":
            return self.isLegalBishopMove(move)

        if pieceType == "Q":
            return (self.isLegalBishopMove(move) or self.isLegalRookMove(move))

    def isLegalKingMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        deltaRow = abs(move[2]-move[4])
        deltaCol = abs(move[3]-move[5])
        movementCorrect = False
        movetoSafe = False
        if (deltaRow==1 and (deltaCol==0 or deltaCol==1)) or (deltaCol==1 and (deltaRow==0 or deltaRow==1)):
            movementCorrect = True
        try:
            if self.grid[move[4]][move[5]][1] == move[0]:
                movetoSafe = False
            else:
                movetoSafe = True
        except IndexError:
            movetoSafe = True

        return movetoSafe and movementCorrect

    def isLegalKnightMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        deltaRow,deltaCol = abs(move[2]-move[4]),abs(move[3]-move[5])
        movementCorrect = False#they need to be false by default, if they should be true I will make them true
        gotoSafe = False
        if ((deltaRow==1 and deltaCol==2) or (deltaRow==2 and deltaCol==1)):
            movementCorrect = True

        try:
            if (move[0] == "w") and (self.grid[move[4]][move[5]][0] == "b"):
                gotoSafe = True
            elif (move[0] == "b") and (self.grid[move[4]][move[5]][0] == "w"):
                gotoSafe = True
        except IndexError:
            gotoSafe = True

        return (movementCorrect and gotoSafe)


    def isLegalBishopMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        if not (abs(move[2]-move[4]) == abs(move[3]-move[5])):
            return False


        distance = abs(move[2]-move[4])

        rowDirection = distance/(move[4]-move[2])
        columnDirection = distance/(move[5]-move[3])

        for i in range(1,distance):
            if self.grid[move[2] + (i*rowDirection)][move[3] + (i*columnDirection)]!="":
                return False

        try:
            if self.grid[move[4]][move[5]][1] == move[0]:
                return False  #if there is a same-colored piece where you want to go
        except:
            pass

        return True

    def isLegalPawnMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        if move[0]=="w":#moving as a white piece is opposite of moving as a black piece, so it will be programmed seperately
            isStartingSpot = move[2]==1 #a boolean for if it is in the starting possition
            if ((move[4]-move[2] == 1) or (isStartingSpot and (move[4]-move[2] == 2))) and (move[3]==move[5]):#basically if it is moving forward by one, or by two if in the starting spot and staying in the same column
                if len(self.grid[move[4]][move[5]]) > 1:#if there is a piece there, because the pawn cannot take a piece by doing this type of move
                    return False
                return True
            elif (move[4]-move[2] == 1) and (abs(move[3]-move[5])==1):
                try:
                    if self.grid[move[4]][move[5]][1] == "b":#if it is going to an enemy piece
                        return True
                except:
                    pass

        elif move[0]=="b":
            isStartingSpot = move[2]==6 #a boolean for if it is in the starting possition
            if ((move[2]-move[4] == 1) or (isStartingSpot and (move[2]-move[4] == 2)) and (move[3]==move[5])): #basically if it is moving forward by one, or by two if in the starting spot and staying in the same column
                if len(self.grid[move[4]][move[5]]) > 1:#if there is a piece there, because the pawn cannot take a piece by doing this type of move
                    return False
                return True
            elif (move[2]-move[4] == 1) and (abs(move[3]-move[5])==2):#this is beautiful because 1 is true, and I want to see if it is moving one to the side
                try:
                    if self.grid[move[4]][move[5]][1] == "w":#if it is going to an enemy piece
                        return True
                except:
                    pass
        return False

    def isLegalRookMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]

        if not ((move[2]==move[4]) or (move[3]==move[5])): #makes sure that it is either the same row or column
            return False
        if move[2] == move[4]: #if we are doing a
            if move[5] > move[3]:
                for i in range (move[3]+1,move[5]):
                    if self.grid[move[2]][i] != "":    #if the path is blocked by another piece
                        return False
            else:
                for i in range (move[5]+1,move[3]):
                    if self.grid[move[2]][i] != "":    #if the path is blocked by another piece
                        return False
                    #alsd

        else:
            if move[2]>move[4]:
                for i in range(move[4]+1,move[2]):
                    if self.grid[i][move[3]] != "": return False
            else:
                for i in range(move[2]+1,move[4]):
                    if self.grid[i][move[3]] != "": return False

        try:
            if self.grid[move[4]][move[5]][1] == move[0]: return False  #if there is a same-colored piece where you want to go
        except:
            pass

        return True

    def movePiece(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]

        #NOTE only call this function if you have already checked if the move is a legal move

        self.lastGrid = [self.grid[i][:] for i in range(8)]#because python takes over the control of pointers and such, this is the only way to make it not update with self.grid

        self.grid[move[2]][move[3]] = ""
        self.grid[move[4]][move[5]] = move[1]+move[0]

    def takePlayerMove(self,colorsTurn):
        while 1: #because python doesn't have any heckin' do while loops
            print "it is "+colorsTurn+"'s turn\n"
            rawMove = raw_input("input move in the format:\nPieceAbbreviation (Knights are 'N') row column rowTo columnTo\n\n>>>").split() #currently in the format ['piece',row,column,rowTo,columnTo]

            move = [colorsTurn]
            for i in range(1,5):
                rawMove[i] = int(rawMove[i])
            move.extend(rawMove)
            if self.isLegalMove(move):
                break
            else:
                print "that move was not a legal move, please check how you formated it"

        self.movePiece(move)

    def printGrid(self): #temporary, not a very nice looking print; TODO make more nice looking
        print "  " + str([(" "+str(i)+" ") for i in range(8)])+"\n"
        for y in range(8)[::-1]:
            row = self.grid[y]
            print str(y)+" "+str([(row[i]+" " if len(row[i])>0 else "   ") for i in range(8)])+"\n"

class Game():

    def __init__(self):
        self.board = Board()

        if input("how many players?")==1:
            self.gameType = 1
            self.blackOrWhite = raw_input("black or white? (b/w):")
            self.playSinglePlayer()
        else:
            self.gameType = 2
            self.playGame()

    def playGame(self):
        whoseTurn = "w"
        while (not self.board.isCheckmate(whoseTurn)):
            self.board.printGrid()
            self.board.takePlayerMove(whoseTurn)
            whoseTurn = ("w" if whoseTurn == "b" else "b")


        self.board.printGrid()
        print "checkmate"

    def playSinglePlayer(self):#TODO
        pass
def main():
    game = Game()

if __name__ == "__main__":
    main()
