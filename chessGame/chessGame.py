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

    def isLegalMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        pieceType = move[1]

        if not (pieceType+move[0] == self.grid[move[2]][move[3]]): #the piece has to be there
            return False

        if move[2]==move[4] and move[3]==move[5]: return False

        if pieceType == "P":
            return self.isLegalPawnMove(move)

        if pieceType == "N":
            return self.isLegalKnightMove(move)#TODO

        if pieceType == "R":
            return self.isLegalRookMove(move)#TODO

        if pieceType == "K":
            return self.isLegalKingMove(move)#TODO

        if pieceType == "B":
            return self.isLegalBishopMove(move)#TODO

        if pieceType == "Q":
            return (self.isLegalBishopMove or self.isLegalRookMove)

    def isLegalBishopMove(self,move):
        pass #TODO NEXT CLASS

    def isLegalPawnMove(self,move): #move is being passed in the format: ["color","type",row,column,rowTo,columnTo]
        if move[0]=="w":#moving as a white piece is opposite of moving as a black piece, so it will be programmed seperately
            isStartingSpot = move[2]==1 #a boolean for if it is in the starting possition
            if ((move[4]-move[2] == 1) or (isStartingSpot and (move[4]-move[2] == 2))) and (move[3]==move[5]):#basically if it is moving forward by one, or by two if in the starting spot and staying in the same column
                return True
            elif (move[4]-move[2] == 1) and abs(move[3]-move[5]):#this is beautiful because 1 is true, and I want to see if it is moving one to the side
                try:
                    if self.grid[move[4]][move[5]][1] == "b":#if it is going to an enemy piece
                        return True
                except:
                    pass

        elif move[0]=="b":
            isStartingSpot = move[2]==6 #a boolean for if it is in the starting possition
            if ((move[2]-move[4] == 1) or (isStartingSpot and (move[2]-move[4] == 1)) and (move[3]==move[5])): #basically if it is moving forward by one, or by two if in the starting spot and staying in the same column
                return True
            elif (move[2]-move[4] == 1) and abs(move[3]-move[5]):#this is beautiful because 1 is true, and I want to see if it is moving one to the side
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
            if move[3] > move[5]:
                for i in range (move[3]+1,move[5]+1):
                    if self.grid[move[2]][i] != "":    #if the path is blocked by another piece
                        return False
            else:
                for i in range (move[2]+1,move[4]+1):
                    if self.grid[move[3]][i] != "":#if the path is blocked by another piece
                        return False
        try:
            if self.grid[move[4]][move[5]][1] == move[0]: return False  #if there is a same-colored piece where you want to go
        except:
            pass

        return True

    def printGrid(self):
        for i in self.grid:
            print i



class Game():

    def __init__(self,blackOrWhite):
        self.board = Board

def main():
    board = Board()

    board.printGrid()

if __name__ == "__main__":
    main()
    board = Board()
