from graphics import *
import copy
import time
from collections import OrderedDict
import random
import math
import numpy as np

pieces = {}
squares = [[Point(0,0) for x in range(8)] for y in range(8)]
letters = {}

def main():
    window = GraphWin("Checkers", 640, 640)
    window.setBackground("black")
    drawWindowBoard(Point(0,0), 640, window)
    drawStartingPos(Point(0,0), 640, window)
    b = Board()
    drawBoard(b, window)
    n = MCNode(b)
    monteCarlo(n, 3)
    n = n.getChild()
    drawBoard(n.boardrep, window)
    while len(n.children) > 0:
        monteCarlo(n, 3)
        n = n.getChild()
        drawBoard(n.boardrep, window)
    window.getMouse()
    window.close()

def monteCarlo(node, secs):
    starttime = time.time()
    while time.time() - starttime < secs:
        node.selection()


#draws out the board for the checkers game but none of the pieces
def drawWindowBoard(s_point, size, g):
    sizeSq = size / 8
    for i in range(8):
        for j in range(8):
            if i % 2 == 0 and j % 2 == 0 or i % 2 != 0 and j % 2 != 0:
                rect = Rectangle(Point(s_point.getX() + sizeSq*i, s_point.getY() + sizeSq*j), Point(s_point.getX() + sizeSq*(i+1), s_point.getY() + sizeSq*(j+1)))
                rect.setFill(color_rgb(230, 20, 20))
                squares[j][i] = rect.getCenter()
                rect.draw(g)
            else:
                rect = Rectangle(Point(s_point.getX() + sizeSq*i, s_point.getY() + sizeSq*j), Point(s_point.getX() + sizeSq*(i+1), s_point.getY() + sizeSq*(j+1)))
                rect.setFill(color_rgb(0, 0, 0))
                squares[j][i] = rect.getCenter()
                rect.draw(g)

#method for drawing a checker, including color, size, window
def drawChecker(c_point, color, size, g):
    c_piece_size = int(size / 8 * 7 / 10 / 2)
    check_piece = Circle(Point(c_point.getX(), c_point.getY()), c_piece_size)
    if color.lower() == "red":
        check_piece.setFill(color_rgb(230, 20, 20))
    else:
        check_piece.setFill(color_rgb(0, 0, 0))
    check_piece.setOutline(color_rgb(255, 255, 255))
    check_piece.draw(g)
    piecenum = len(pieces)
    pieces.update({check_piece: piecenum})
    
#draws the starting position of a board of checkers
def drawStartingPos(s_point, size, g):
    sizeSq = size / 8
    for j in range(7, 4, -1):
        for i in range(8):
            if i % 2 != 0 and j % 2 == 0 or i % 2 == 0 and j % 2 != 0:
                p1 = s_point.getX() + sizeSq * i + sizeSq / 2
                p2 = s_point.getX() + sizeSq * j + sizeSq / 2
                drawChecker(Point(p1, p2), "red", 640, g)
    for j in range(2, -1, -1):
        for i in range(8):
            if i % 2 != 0 and j % 2 == 0 or i % 2 == 0 and j % 2 != 0:
                p1 = s_point.getX() + sizeSq * i + sizeSq / 2
                p2 = s_point.getX() + sizeSq * j + sizeSq / 2
                drawChecker(Point(p1, p2), "black", 640, g)

#clears the current board of pieces and king lettering then reletters all the board
def drawBoard(inboard, g):
    for piece in pieces:
        piece.undraw()
    pieces.clear()
    for letter in letters:
        letter.undraw()
    letters.clear()
    bs = inboard.boardstate
    for i in range(0,8):
        for j in range(0,8):
            if bs[i][j] == "r":
                drawChecker(squares[i][j], "red", 640, g)
            if bs[i][j] == "b":
                drawChecker(squares[i][j], "black", 640, g)
            if bs[i][j] == "R":
                drawChecker(squares[i][j], "red", 640, g)
                t = Text(squares[i][j], "K")
                t.setTextColor("white")
                t.draw(g)
                letters.update({t: len(letters)})
            if bs[i][j] == "B":
                drawChecker(squares[i][j], "black", 640, g)
                t = Text(squares[i][j], "K")
                t.setTextColor("white")
                t.draw(g)
                letters.update({t: len(letters)})

class Board:
    turn = "red"
    originalturn = ""
    redmen = 0
    blackmen = 0
    redkings = 0
    blackkings = 0
    boardstate = 0

    #initializes a board with a set board state (i.e. the next move in a sequence)
    def __init__(self, turn=None, boardpos=None):
        if boardpos is None:
            self.boardstate = [["-", "b", "-", "b", "-", "b", "-", "b"],
            ["b", "-", "b", "-", "b", "-", "b", "-"],
            ["-", "b", "-", "b", "-", "b", "-", "b"],
            ["-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-"],
            ["r", "-", "r", "-", "r", "-", "r", "-"],
            ["-", "r", "-", "r", "-", "r", "-", "r"],
            ["r", "-", "r", "-", "r", "-", "r", "-"]]
        else:
            self.boardstate = boardpos
        if turn is None:
            self.turn = "red"
        else:
            self.turn = turn
        originalturn = copy.copy(turn)
    
    #counts up the red pieces and corrects the king and men counts
    def countRedPieces(self):
        self.redmen = 0
        self.redkings = 0
        for i in range(8):
            for j in range(8):
                if self.boardstate[i][j] == "r":
                    self.redmen = self.redmen + 1
                elif self.boardstate[i][j] == "R":
                    self.redkings = self.redkings + 1
        return self.redmen + self.redkings

    #counts up the black pieces and corrects the king and men counts
    def countBlackPieces(self):
        self.blackmen = 0
        self.blackkings = 0
        for i in range(8):
            for j in range(8):
                if self.boardstate[i][j] == "b":
                    self.blackmen = self.blackmen + 1
                elif self.boardstate[i][j] == "B":
                    self.blackkings = self.blackkings + 1
        return self.blackmen + self.blackkings

    #returns available moves as new boards
    def availableMoves(self):
        possibleMoves = self.availableJumps()
        if len(possibleMoves) != 0:
            return possibleMoves
        else:
            if self.turn == "black":
                nextturn = "red"
            if self.turn == "red":
                nextturn = "black"
            for i in range(8):
                for j in range(8):
                    if self.turn == "red":
                        if self.boardstate[i][j].lower() == "r":
                            if i >= 1:
                                if j >= 1:
                                    if self.boardstate[i-1][j-1] == "-":
                                        newpos = self.replicateBoardState()
                                        newpos[i-1][j-1] = newpos[i][j]
                                        newpos[i][j] = "-"
                                        possibleMoves.append(Board(nextturn, newpos))
                                if j <= 6:
                                    if self.boardstate[i-1][j+1] == "-":
                                        newpos = self.replicateBoardState()
                                        newpos[i-1][j+1] = newpos[i][j]
                                        newpos[i][j] = "-"
                                        possibleMoves.append(Board(nextturn, newpos))
                        if self.boardstate[i][j] == "R":
                            if i <= 6:
                                if j >= 1:
                                    if self.boardstate[i+1][j-1] == "-":
                                        newpos = self.replicateBoardState()
                                        newpos[i+1][j-1] = newpos[i][j]
                                        newpos[i][j] = "-"
                                        possibleMoves.append(Board(nextturn, newpos))
                                if j <= 6:
                                    if self.boardstate[i+1][j+1] == "-":
                                        newpos = self.replicateBoardState()
                                        newpos[i+1][j+1] = newpos[i][j]
                                        newpos[i][j] = "-"
                                        possibleMoves.append(Board(nextturn, newpos))
                    else:
                        if self.boardstate[i][j] == "B":
                            if i >= 1:
                                if j >= 1:
                                    if self.boardstate[i-1][j-1] == "-":
                                        newpos = self.replicateBoardState()
                                        newpos[i-1][j-1] = newpos[i][j]
                                        newpos[i][j] = "-"
                                        possibleMoves.append(Board(nextturn, newpos))
                                if j <= 6:
                                    if self.boardstate[i-1][j+1] == "-":
                                        newpos = self.replicateBoardState()
                                        newpos[i-1][j+1] = newpos[i][j]
                                        newpos[i][j] = "-"
                                        possibleMoves.append(Board(nextturn, newpos))
                        if self.boardstate[i][j].lower() == "b":
                            if i <= 6:
                                if j >= 1:
                                    if self.boardstate[i+1][j-1] == "-":
                                        newpos = self.replicateBoardState()
                                        newpos[i+1][j-1] = newpos[i][j]
                                        newpos[i][j] = "-"
                                        possibleMoves.append(Board(nextturn, newpos))
                                if j <= 6:
                                    if self.boardstate[i+1][j+1] == "-":
                                        newpos = self.replicateBoardState()
                                        newpos[i+1][j+1] = newpos[i][j]
                                        newpos[i][j] = "-"
                                        possibleMoves.append(Board(nextturn, newpos))
            if len(possibleMoves) > 0:
                for boards in possibleMoves:
                    boards.makeKings()
            return possibleMoves

    #returns all available jumps as new boards
    def availableJumps(self, xy = None):
        possibleJumps = []
        if xy == None:
            for i in range(8):
                for j in range(8):
                    if self.turn == "red":
                        if self.boardstate[i][j].lower() == "r":
                            if i >= 2:
                                if j >= 2:
                                    if self.boardstate[i-1][j-1].lower() == "b":
                                        if self.boardstate[i-2][j-2] == "-":
                                            newpos = self.replicateBoardState()
                                            newpos[i-2][j-2] = newpos[i][j]
                                            newpos[i-1][j-1] = "-"
                                            newpos[i][j] = "-"
                                            possibleJumps.append(Board(self.turn, newpos))
                                if j <= 5:
                                    if self.boardstate[i-1][j+1].lower() == "b":
                                        if self.boardstate[i-2][j+2] == "-":
                                            newpos = self.replicateBoardState()
                                            newpos[i-2][j+2] = newpos[i][j]
                                            newpos[i-1][j+1] = "-"
                                            newpos[i][j] = "-"
                                            possibleJumps.append(Board(self.turn, newpos))
                        if self.boardstate[i][j] == "R":
                            if i <= 5:
                                if j >= 2:
                                    if self.boardstate[i+1][j-1].lower() == "b":
                                        if self.boardstate[i+2][j-2] == "-":
                                            newpos = self.replicateBoardState()
                                            newpos[i+2][j-2] = newpos[i][j]
                                            newpos[i+1][j-1] = "-"
                                            newpos[i][j] = "-"
                                            possibleJumps.append(Board(self.turn, newpos))
                                if j <= 5:
                                    if self.boardstate[i+1][j+1].lower() == "b":
                                        if self.boardstate[i+2][j+2] == "-":
                                            newpos = self.replicateBoardState()
                                            newpos[i+2][j+2] = newpos[i][j]
                                            newpos[i+1][j+1] = "-"
                                            newpos[i][j] = "-"
                                            possibleJumps.append(Board(self.turn, newpos))
                    else:
                        if self.boardstate[i][j] == "B":
                            if i >= 2:
                                if j >= 2:
                                    if self.boardstate[i-1][j-1].lower() == "r":
                                        if self.boardstate[i-2][j-2] == "-":
                                            newpos = self.replicateBoardState()
                                            newpos[i-2][j-2] = newpos[i][j]
                                            newpos[i-1][j-1] = "-"
                                            newpos[i][j] = "-"
                                            possibleJumps.append(Board(self.turn, newpos))
                                if j <= 5:
                                    if self.boardstate[i-1][j+1].lower() == "r":
                                        if self.boardstate[i-2][j+2] == "-":
                                            newpos = self.replicateBoardState()
                                            newpos[i-2][j+2] = newpos[i][j]
                                            newpos[i-1][j+1] = "-"
                                            newpos[i][j] = "-"
                                            possibleJumps.append(Board(self.turn, newpos))
                        if self.boardstate[i][j].lower() == "b":
                            if i <= 5:
                                if j <= 5:
                                    if self.boardstate[i+1][j+1].lower() == "r":
                                        if self.boardstate[i+2][j+2] == "-":
                                            newpos = self.replicateBoardState()
                                            newpos[i+2][j+2] = newpos[i][j]
                                            newpos[i+1][j+1] = "-"
                                            newpos[i][j] = "-"
                                            possibleJumps.append(Board(self.turn, newpos))
                                if j >= 2:
                                    if self.boardstate[i+1][j-1].lower() == "r":
                                        if self.boardstate[i+2][j-2] == "-":
                                            newpos = self.replicateBoardState()
                                            newpos[i+2][j-2] = newpos[i][j]
                                            newpos[i+1][j-1] = "-"
                                            newpos[i][j] = "-"
                                            possibleJumps.append(Board(self.turn, newpos))
        else:
            i = xy[0]
            j = xy[1]
            if self.turn == "red":
                if self.boardstate[i][j].lower() == "r":
                    if i >= 2:
                        if j >= 2:
                            if self.boardstate[i-1][j-1].lower() == "b":
                                if self.boardstate[i-2][j-2] == "-":
                                    newpos = self.replicateBoardState()
                                    newpos[i-2][j-2] = newpos[i][j]
                                    newpos[i-1][j-1] = "-"
                                    newpos[i][j] = "-"
                                    possibleJumps.append(Board(self.turn, newpos))
                        if j <= 5:
                            if self.boardstate[i-1][j+1].lower() == "b":
                                if self.boardstate[i-2][j+2] == "-":
                                    newpos = self.replicateBoardState()
                                    newpos[i-2][j+2] = newpos[i][j]
                                    newpos[i-1][j+1] = "-"
                                    newpos[i][j] = "-"
                                    possibleJumps.append(Board(self.turn, newpos))
                if self.boardstate[i][j] == "R":
                    if i <= 5:
                        if j >= 2:
                            if self.boardstate[i+1][j-1].lower() == "b":
                                if self.boardstate[i+2][j-2] == "-":
                                    newpos = self.replicateBoardState()
                                    newpos[i+2][j-2] = newpos[i][j]
                                    newpos[i+1][j-1] = "-"
                                    newpos[i][j] = "-"
                                    possibleJumps.append(Board(self.turn, newpos))
                        if j <= 5:
                            if self.boardstate[i+1][j+1].lower() == "b":
                                if self.boardstate[i+2][j+2] == "-":
                                    newpos = self.replicateBoardState()
                                    newpos[i+2][j+2] = newpos[i][j]
                                    newpos[i+1][j+1] = "-"
                                    newpos[i][j] = "-"
                                    possibleJumps.append(Board(self.turn, newpos))
            else:
                if self.boardstate[i][j] == "B":
                    if i >= 2:
                        if j >= 2:
                            if self.boardstate[i-1][j-1].lower() == "r":
                                if self.boardstate[i-2][j-2] == "-":
                                    newpos = self.replicateBoardState()
                                    newpos[i-2][j-2] = newpos[i][j]
                                    newpos[i-1][j-1] = "-"
                                    newpos[i][j] = "-"
                                    possibleJumps.append(Board(self.turn, newpos))
                        if j <= 5:
                            if self.boardstate[i-1][j+1].lower() == "r":
                                if self.boardstate[i-2][j+2] == "-":
                                    newpos = self.replicateBoardState()
                                    newpos[i-2][j+2] = newpos[i][j]
                                    newpos[i-1][j+1] = "-"
                                    newpos[i][j] = "-"
                                    possibleJumps.append(Board(self.turn, newpos))
                if self.boardstate[i][j].lower() == "b":
                    if i <= 5:
                        if j <= 5:
                            if self.boardstate[i+1][j+1].lower() == "r":
                                if self.boardstate[i+2][j+2] == "-":
                                    newpos = self.replicateBoardState()
                                    newpos[i+2][j+2] = newpos[i][j]
                                    newpos[i+1][j+1] = "-"
                                    newpos[i][j] = "-"
                                    possibleJumps.append(Board(self.turn, newpos))
                        if j >= 2:
                            if self.boardstate[i+1][j-1].lower() == "r":
                                if self.boardstate[i+2][j-2] == "-":
                                    newpos = self.replicateBoardState()
                                    newpos[i+2][j-2] = newpos[i][j]
                                    newpos[i+1][j-1] = "-"
                                    newpos[i][j] = "-"
                                    possibleJumps.append(Board(self.turn, newpos))
        if len(possibleJumps) != 0:
            for boards in possibleJumps:
                if self.turn == "black":
                    nextturn = "red"
                if self.turn == "red":
                    nextturn = "black"
                boards.countRedPieces()
                boards.countBlackPieces()
                kingsbefore = boards.redkings + boards.blackkings
                boards.makeKings()
                boards.countRedPieces()
                boards.countBlackPieces()
                kingsafter = boards.redkings + boards.blackkings
                if kingsafter - kingsbefore > 0:
                    boards.turn = nextturn
                else:
                    if len(boards.availableJumps()) == 0:
                        if boards.originalturn == boards.turn:
                            boards.turn = nextturn
                    else:
                        for boards2 in boards.availableJumps(self.getJumpPos(boards)):
                            possibleJumps.append(boards2)
                        possibleJumps.remove(boards)
        else:
            return []
        dupelist = copy.deepcopy(possibleJumps)
        for i in possibleJumps:
            if len(dupelist) > 0:
                dupelist.pop(0)
            else:
                break
            for j in dupelist:
                if i.isEqual(i.boardstate, j.boardstate):
                    possibleJumps.reverse()
                    possibleJumps.remove(i)
                    possibleJumps.reverse()
                    break
        return possibleJumps

    #this function is here to make sure a jump continues and a new jumo doesn't start
    def getJumpPos(self, board1):
        for i in range(8):
            for j in range(8):
                if board1.boardstate[i][j].lower() == "b" or board1.boardstate[i][j].lower() == "r":
                    if self.boardstate[i][j] == "-":
                        return i, j

    #makes any pieces that land on the correct squares in to kings
    def makeKings(self):
        for i in range(8):
            if self.boardstate[0][i] == "r":
                self.boardstate[0][i] = "R"
            if self.boardstate[7][i] == "b":
                self.boardstate[7][i] = "B"

    #a method to copy the list so that it looks prettier
    def replicateBoardState(self):
        templist = copy.deepcopy(self.boardstate)
        return templist

    #checks if 2 board states are equal
    def isEqual(self, boardstate1, boardstate2):
        for i in range(8):
            for j in range(8):
                if boardstate1[i][j] != boardstate2[i][j]:
                    return False
        return True

class MCNode:

    parent = None
    boardrep = None
    children = []
    redwins = 0
    blackwins = 0
    explorationValue = math.sqrt(2)
    depth = 0
    maxdepth = 15
    visits = 0
    repeatedPos = False

    def __init__(self, board, parent=None):
        if parent != None:
            self.parent = parent
            self.depth = parent.depth + 1
        self.boardrep = board
        self.children = []
        self.redwins = 0
        self.blackwins = 0
        self.visits = 0
        self.maxdepth = 15

    #gets the child to node to go to
    def getChild(self):
        nodevisits = []
        for child in self.children:
            nodevisits.append(child.visits)
        return self.children[nodevisits.index(max(nodevisits))]

    #selects a child node based on value
    def selection(self):
        self.fixTurns()
        if len(self.children) == len(self.boardrep.availableMoves()) and len(self.children) != 0:
            vals = []
            for node in self.children:
                vals.append(node.evalNode())
            maxvalpos = vals.index(max(vals))
            self.children[maxvalpos].selection()
        else:
            avail = self.boardrep.availableMoves()
            for board in self.children:
                if board in avail:
                    avail.remove(board)
            if len(avail) == 1:
                self.children.append(MCNode(avail[0], self))
                self.children[len(self.children) - 1].rollout()
            elif len(avail) > 1:
                self.children.append(MCNode(avail[random.randint(0,len(avail)-1)], self))
                self.children[len(self.children) - 1].rollout()
            else:
                self.backprop(self.evalWinner())

    #rolls out from the newest child node
    def rollout(self):
        self.fixTurns()
        if(self.depth - self.getRootDepth() < self.maxdepth):
            moves = self.boardrep.availableMoves()
            if len(moves) == 0:
                if self.boardrep.countBlackPieces() == 0:
                    self.backprop("red")
                elif self.boardrep.countRedPieces() == 0:
                    self.backprop("black")
                elif self.boardrep.turn == "red":
                    self.backprop("black")
                else:
                    self.backprop("red")
            elif len(moves) == 1:
                if len(self.children) == 1:
                    children[0].rollout()
            elif len(self.children) > 1:
                chosen = random.randint(0, len(moves)-1)
                rolledout = 0
                for child in self.children:
                    if child.boardrep.isEqual(moves[chosen]):
                        child.rollout()
                        rolledout = 1
                        break
                if rolledout == 0:
                    self.children.append(MCNode(moves[chosen], self))
                    children[len(children) - 1].rollout()
        else:
            self.backprop(self.evalWinner)

    #gets the amount of visits below the current node
    def getVisitsBelow(self):
        vbelow = 0
        for child in self.children:
            vbelow = vbelow + child.visits
        if vbelow == 0:
            return 1
        return vbelow

    def fixTurns(self):
        if self.parent != None:
            if self.boardrep.turn == self.parent.boardrep.turn:
                if self.boardrep.turn == "red":
                    self.boardrep.turn = "black"
                else:
                    self.boardrep.turn = "red"

    #backpropagation algorithm
    def backprop(self, color):
        if color == "red":
            self.redwins = self.redwins + 1
        elif color == "black":
            self.blackwins = self.blackwins + 1
        else:
            self.blackwins = self.blackwins + .5
            self.redwins = self.redwins + .5
        self.visits = self.visits + 1
        if self.parent != None:
            self.parent.backprop(color)

    #evaluates who is winning in the node
    def evalWinner(self):
        self.boardrep.countBlackPieces
        self.boardrep.countRedPieces
        redval = self.boardrep.redmen + self.boardrep.redkings * 1.1
        blackval = self.boardrep.blackmen + self.boardrep.blackkings * 1.1
        if redval > blackval:
            return "red"
        elif blackval > redval:
            return "black"
        else:
            return "none"

    #evaluates the value of nodes
    def evalNode(self):
        self.fixTurns()
        if self.boardrep.turn == "black":
            firstval = self.redwins/self.getVisitsBelow()
        else:
            firstval = self.blackwins/self.getVisitsBelow()
        if self.parent == None:
            Ni = 0
        else:
            Ni = self.parent.getVisitsBelow()
        secondval = self.explorationValue * math.sqrt(np.log(Ni)/self.getVisitsBelow())
        return firstval + secondval

    #returns the depth of the current root node
    def getRootDepth(self):
        if(self.parent != None):
            return self.parent.getRootDepth()
        else:
            return self.depth
main()