#NOTE ALL KNIGHTS ARE REFERRED TO WITH THE LETTER N BECAUSE KING STARTS WITH K

#TODO: add only being able to castle when not in check;

class Board:

    def __init__(self):

        self.pieceStartOrder = ["R","N","B","Q","K","B","N","R"]

        self.grid = self.makeGrid()

        self.whiteCastleableSpots = [[0,0],[0,7]]
        self.blackCastleableSpots = [[7,0],[7,7]]

        self.gridCache = []

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

        posMoves = self.possibleColorMoves(("w" if whoseTurn == "b" else "b"),False)

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

        posMoves = self.possibleColorMoves(whoseTurn,False)

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

        self.grid = [i[:] for i in self.gridCache[-1]]

        self.gridCache.pop(-1)

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


    def possiblePieceMoves2(self,row,column):#all of the possible moves that a given piece can make
        pieceType = self.grid[row][column][0]
        pieceColor = self.grid[row][column][1]

        baseMove = [pieceColor,pieceType,row,column]

        foundMoves = []

        for rowTo in range(8):
            for columnTo in range(8):
                testingMove = baseMove[:]
                testingMove.append(rowTo)
                testingMove.append(columnTo)
                if self.isLegalMove(testingMove,False):
                    print testingMove,"was a duplicate"


        return foundMoves

    def possiblePieceMoves(self,row,col,safeMode):
        piece = self.grid[row][col]
        pieceType = piece[0]
        pieceColor = piece[1]
        if pieceType == "Q":
            moves = self.possibleRookMoves(pieceColor,row,col,safeMode)
            moves.extend(self.possibleBishopMoves(pieceColor,row,col,safeMode))
            return moves
        return {"R":self.possibleRookMoves(pieceColor,row,col,safeMode),"N":self.possibleKnightMoves(pieceColor,row,col,safeMode),"B":self.possibleBishopMoves(pieceColor,row,col,safeMode),"K":self.possibleKingMoves(pieceColor,row,col,safeMode),"P":self.possiblePawnMoves(pieceColor,row,col,safeMode)}[pieceType]

    def possiblePawnMoves(self,color,row,col,safeMode):
        returnList = []
        piece = self.grid[row][col]
        for a in range(row-2,row+3):
            for b in range(col-1,col+2):
                move = [piece[1],piece[0],row,col,a,b]
                if self.isLegalMove(move,safeMode):
                    returnList.append(move)
        return returnList

    def possibleBishopMoves(self,color,row,col,safeMode):
        returnList = []
        piece = self.grid[row][col]

        for a in range(8):
            for b in range(8):
                move = [piece[1],piece[0],row,col,a,b]
                if self.isLegalMove(move,safeMode):
                    returnList.append(move[:])
        return returnList

    def possibleRookMoves(self,color,row,col,safeMode):
        returnList = []
        piece = self.grid[row][col]

        for i in range(8):
            move = [piece[1],piece[0],row,col,i,col]
            if self.isLegalMove(move,safeMode):
                returnList.append(move[:])
            move[4] = row
            move[5] = i
            if self.isLegalMove(move,safeMode):
                returnList.append(move[:])

        return returnList

    def possibleKnightMoves(self,color,row,col,safeMode):
        returnList = []
        piece = self.grid[row][col]

        move = [piece[1],piece[0],row,col,row+1,col+2]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row-1,col+2]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row+1,col-2]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row-1,col-2]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row+2,col+1]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row+2,col-1]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row-2,col+1]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        move = [piece[1],piece[0],row,col,row-2,col-1]
        if self.isLegalMove(move,safeMode): returnList.append(move[:])

        return returnList

    def possibleKingMoves(self,color,row,col,safeMode):
        returnList = []
        piece = self.grid[row][col]

        for a in range(row-1,row+2):
            for b in range(col-1,col+2):
                move = [piece[1],piece[0],row,col,a,b]
                if self.isLegalMove(move,safeMode):
                    returnList.append(move)

        return returnList

    def possibleColorMoves(self,color,safeMode):#all of the possible moves that a player (specified by the color) can make
        foundMoves = []

        for row in range(8):
            for column in range(8):
                piece = self.grid[row][column]
                if len(piece) != 0:
                    if self.grid[row][column][1]==color:
                        pieceMoves = self.possiblePieceMoves(row,column,safeMode)
                        if len(pieceMoves)!=0:
                            foundMoves.extend(pieceMoves)

        return foundMoves


    def isLegalMove(self,move,safeMove): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        if move[4] > 7 or move[4] < 0 or move[5] > 7 or move[4] < 0:
            return False
        pieceType = move[1]
        if safeMove:
            if self.isCheck(move[0]):
                self.movePiece(move)
                if self.isCheck(move[0]):
                    return False
                self.undoMove()

            '''self.movePiece(move)
            if self.isCheck(move[0]):
                self.undoMove()
                return False
            self.undoMove()'''

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
        if move[4]>7 or move[5]>7 or move[4]<0 or move[5]<0: return False
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
        if move[4]>7 or move[5]>7 or move[4]<0 or move[5]<0: return False

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
        if move[4]>7 or move[5]>7 or move[4]<0 or move[5]<0: return False

        if move[2]-move[4] == 0:
            return False
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
        if move[4]>7 or move[5]>7 or move[4]<0 or move[5]<0: return False

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
        if move[4]>7 or move[5]>7 or move[4]<0 or move[5]<0: return False

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

        #first I am putting the code relevant to castling; NOTE: this function is not to be used for castling

        if move[1] == "R":
            if move[0] == "w":
                if [move[2],move[3]] in self.whiteCastleableSpots:
                    self.whiteCastleableSpots.remove([move[2],move[3]])
            elif [move[2],move[3]] in self.blackCastleableSpots:
                self.blackCastleableSpots.remove([move[2],move[3]])

        if move[1] == "K":
            if move[0] == "w":
                self.whiteCastleableSpots = []
            else:
                self.blackCastleableSpots = []

        self.gridCache.append([i[:] for i in self.grid])#because python takes over the control of pointers and such, this is the only way to make it not update with self.grid

        self.grid[move[2]][move[3]] = ""
        try:
            self.grid[move[4]][move[5]] = move[1]+move[0]
        except IndexError:
            print "I tried to do the move",move

    def isLegalCastle(self,color,move):#castles are in the format ["castle",withRookRow,withRookCol]

        #it is highly advised that you look at a chess board while reading this in order to understand it
        #I had to look at one the whole time I programmed it anyway

        if color == "w":
            if not ([move[1],move[2]] in self.whiteCastleableSpots):
                return False
        else:
            if not ([move[1],move[2]] in self.blackCastleableSpots):
                return False

        #now we know if the pieces have been moved

        row = (0 if color=="w" else 7)#the row that this will be happening on

        if move[2] == 0:#if it is the left rook
            for col in range(1,4):
                if not (self.grid[row][col] == ""):
                    print "in the way"
                    return False
        else:
            for col in range(5,7):
                if not (self.grid[row][col] == ""):
                    print "in the way"
                    return False

        return True

    def castleMove(self,move):#castles are in the format ["castle",withRookRow,withRookCol]

        #NOTE this function only gets called if it is already determined to be a legal move

        self.gridCache.append([i[:] for i in self.grid])#again, this is to get around python's stupid (not really stupid, still simpler than C) pointer stuff


        color = ("w" if move[1] == 0 else "b")

        kingCoords = [(2 if move[2] == 0 else 6),move[1]]
        rookCoords = [(3 if move[2] == 0 else 5),move[1]]

        self.grid[move[1]][kingCoords[0]] = "K"+color
        self.grid[move[1]][4] = ""
        self.grid[move[1]][rookCoords[0]] = "R"+color
        self.grid[move[1]][move[2]] = ""


    def takePlayerMove(self,colorsTurn):
        while 1: #because python doesn't have any heckin' do while loops
            print "it is "+colorsTurn+"'s turn\n"
            rawMove = raw_input("input move in the format:\nPieceAbbreviation (Knights are 'N') row column rowTo columnTo\n\n>>>").split() #currently in the format ['piece',row,column,rowTo,columnTo]

            if rawMove[0].lower() == "castle":#castles are in the format ["castle",withRookRow,withRookCol]
                rawMove[1],rawMove[2] = int(rawMove[1]),int(rawMove[2])
                if self.isLegalCastle(colorsTurn,rawMove):
                    self.castleMove(rawMove)
                    break
                else:
                    print "that move was not a legal move, please check how you formated it"


            else:

                move = [colorsTurn]
                for i in range(1,5):
                    rawMove[i] = int(rawMove[i])
                move.extend(rawMove)
                if self.isLegalMove(move,True):
                    self.movePiece(move)
                    break
                else:
                    print "that move was not a legal move, please check how you formated it"


    def printGrid(self):

        top = "   0  1  2  3  4  5  6  7"
        print top

        for i in range(8)[::-1]:
            row = self.grid[i]
            printRow = str(i)+" "
            for square in row:
                if len(square)>1:
                    printRow = printRow + square + " "
                else:
                    printRow = printRow + " - "
            print printRow


'''        print "  " + str([(" "+str(i)+" ") for i in range(8)])+"\n"
        for y in range(8)[::-1]:
            row = self.grid[y]
            print str(y)+" "+str([(row[i]+" " if len(row[i])>0 else "   ") for i in range(8)])+"\n"
'''
class Game():

    def __init__(self,tuningValues,testing):
        self.board = Board()
        self.pieceValues = [tuningValues[i] for i in range(6)]
        self.movementCoefficients = [tuningValues[i] for i in range(6,12)]
        if testing:
            self.playOther()
        else:
            if input("how many players?")==1:
                self.gameType = 1
                self.playSinglePlayer()
            else:
                self.gameType = 2
                self.playGame()

    def playOther(self):
        pass

    def playGame(self):
        whoseTurn = "w"
        while (not self.board.isCheckmate(whoseTurn)):
            self.board.printGrid()
            self.board.takePlayerMove(whoseTurn)
            whoseTurn = ("w" if whoseTurn == "b" else "b")


        self.board.printGrid()
        print "checkmate"

    def playSinglePlayer(self):
        playerColor = raw_input("\nwhat color do you want to play as?\n>>>")
        compColor = ("b" if playerColor == "w" else "w")

        whoseTurn = "b"#start as black because it switches colors at the start of the loop

        while (not self.board.isCheckmate(whoseTurn)):
            whoseTurn = ("b" if whoseTurn == "w" else "w")
            if whoseTurn == playerColor:
                self.board.printGrid()
                self.board.takePlayerMove(whoseTurn)
            else:
                self.board.movePiece(self.bestMove(compColor))

    def evaluateMove(self,move,movesLeft,isComp):

        #all that is done in this function is call itself recursively and take the worst or best case depending on if it is the computer's turn or the player's turn

        if movesLeft > 0:
            self.board.movePiece(move)
            if isComp:
                if self.board.isCheck(move[0]):
                    self.board.undoMove()
                    return -10000
            color = ("b" if move[0] == "w" else "w")
            possMoves = self.board.possibleColorMoves(color,False)
            if isComp:
                best = self.evaluateMove(possMoves[0],movesLeft-1,(not isComp))
                for nextMove in possMoves:
                    curEval = self.evaluateMove(nextMove,movesLeft-1,(not isComp))
                    if curEval > best: best = curEval
                self.board.undoMove()
                return best
            else:
                worst = self.evaluateMove(possMoves[0],movesLeft-1,(not isComp))
                for nextMove in possMoves:
                    curEval = self.evaluateMove(nextMove,movesLeft-1,(not isComp))
                    if curEval < worst:
                        worst = curEval
                self.board.undoMove()
                return worst
        else:#this is now if there are no more moves to look into the future
            self.board.movePiece(move)
            compColor = (move[0] if isComp else ("w" if move[0]=="b" else "b"))
            evaluation = self.evaluateBoard(compColor)
            self.board.undoMove()
            return evaluation

    def evaluateBoard(self,forColor):#evaluates the worth of the board for a given color

        value = 0
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if len(piece)==0:
                    continue
                elif piece[1] == forColor:
                    value += self.evaluatePieceValue(row,col)
                else:
                    value -= self.evaluatePieceValue(row,col)
        return value

    def evaluatePieceValue(self,row,col):
        piece = self.board.grid[row][col]

        distance = (row if piece[1]=="w" else (7-row))

        #TODO: get better values for the following values from machine learning

        startVals = {"P":self.pieceValues[0],"Q":self.pieceValues[1],"B":self.pieceValues[2],"K":100000,"R":self.pieceValues[4],"N":self.pieceValues[5]}
        distanceCoefficients = {"P":self.movementCoefficients[0],"Q":self.movementCoefficients[1],"B":self.movementCoefficients[2],"K":self.movementCoefficients[3],"R":self.movementCoefficients[4],"N":self.movementCoefficients[5]}

        return (startVals[piece[0]]+(distanceCoefficients[piece[0]]*distance))


    def bestMove(self,color):#compTurn is boolean for if it is the computer's turn
        possMoves = self.board.possibleColorMoves(color,False)
        best = [self.evaluateMove(possMoves[0],2,True),possMoves[0]]
        for move in possMoves:
            curEval = self.evaluateMove(move,2,True)
            if curEval > best[0]:
                best = [curEval,move]
        return best[1]


if __name__ == "__main__":
    #order is: Pawn, Queen, Bishop, King, Rook, Knight
    game = Game([1,10,4,1000,5,3,0.3,0.1,0.3,-1,0.3,0.5],False)
