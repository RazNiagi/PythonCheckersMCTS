from graphics import *

def drawBoard(s_point, size, g):
    sizeSq = size / 8
    for i in range(8):
        for j in range(8):
            if i % 2 == 0 and j % 2 == 0 or i % 2 != 0 and j % 2 != 0:
                rect = Rectangle(
                    Point(s_point.getX() + sizeSq * i,
                          s_point.getY() + sizeSq * j),
                    Point(
                        s_point.getX() + sizeSq * (i + 1),
                        s_point.getY() + sizeSq * (j + 1),
                    ),
                )
                rect.setFill(color_rgb(230, 20, 20))
                rect.draw(g)
            else:
                rect = Rectangle(
                    Point(s_point.getX() + sizeSq * i,
                          s_point.getY() + sizeSq * j),
                    Point(
                        s_point.getX() + sizeSq * (i + 1),
                        s_point.getY() + sizeSq * (j + 1),
                    ),
                )

                rect.setFill(color_rgb(20, 20, 20))
                rect.draw(g)


def main():

    # Create a window in which an example of each piece is demonstrated
    # CheckerPiecesDemo = GraphWin(
    #     "Checker Pieces", 200, 100)  # title, width, height
    # CheckerPiecesDemo.setBackground("Black")

    # african-american piece
    # CheckerPieceBlack = Circle(Point(50, 50), 24)
    # CheckerPieceBlack.setFill(color_rgb(20, 20, 20))
    # CheckerPieceBlack.setOutline(color_rgb(250, 250, 250))
    # CheckerPieceBlack.draw(CheckerPiecesDemo)

    class CheckerPieceBlack:
        def __init__(self):
            self.body = Circle(Point(150, 50), 24)
            self.body.setFill(color_rgb(20, 20, 20))
            self.body.setOutline(color_rgb(250, 250, 250))

    class CheckerPieceRed:
        def __init__(self):
            self.body = Circle(Point(150, 50), 24)
            self.body.setFill(color_rgb(230, 20, 20))
            self.body.setOutline(color_rgb(250, 250, 250))

    # red pieces
    # CheckerPieceRed = Circle(Point(150, 50), 24)
    # CheckerPieceRed.setFill(color_rgb(230, 20, 20))
    # CheckerPieceRed.setOutline(color_rgb(250, 250, 250))
    # CheckerPieceRed.draw(CheckerPiecesDemo)

    # define mainWindow where the board and elements will be drawn
    mainWindow = GraphWin("Checkers", 1024, 768)
    mainWindow.setBackground(color_rgb(50, 50, 50))

    # checker pieces

    blackPiece1 = CheckerPieceBlack()
    blackPiece2 = CheckerPieceBlack()
    blackPiece3 = CheckerPieceBlack()
    blackPiece4 = CheckerPieceBlack()
    blackPiece5 = CheckerPieceBlack()
    blackPiece6 = CheckerPieceBlack()
    blackPiece7 = CheckerPieceBlack()
    blackPiece8 = CheckerPieceBlack()
    blackPiece9 = CheckerPieceBlack()
    blackPiece10 = CheckerPieceBlack()
    blackPiece11 = CheckerPieceBlack()
    blackPiece12 = CheckerPieceBlack()

    blackPieces = [
        blackPiece1,
        blackPiece2,
        blackPiece3,
        blackPiece4,
        blackPiece5,
        blackPiece6,
        blackPiece7,
        blackPiece8,
        blackPiece9,
        blackPiece10,
        blackPiece11,
        blackPiece12
    ]

    for i in blackPieces:
        i.body.draw(mainWindow)

    redPiece1 = CheckerPieceRed()
    redPiece2 = CheckerPieceRed()
    redPiece3 = CheckerPieceRed()
    redPiece4 = CheckerPieceRed()
    redPiece5 = CheckerPieceRed()
    redPiece6 = CheckerPieceRed()
    redPiece7 = CheckerPieceRed()
    redPiece8 = CheckerPieceRed()
    redPiece9 = CheckerPieceRed()
    redPiece10 = CheckerPieceRed()
    redPiece11 = CheckerPieceRed()
    redPiece12 = CheckerPieceRed()

    redPieces = [
        redPiece1,
        redPiece2,
        redPiece3,
        redPiece4,
        redPiece5,
        redPiece6,
        redPiece7,
        redPiece8,
        redPiece9,
        redPiece10,
        redPiece11,
        redPiece12
    ]

    for i in redPieces:
        i.body.draw(mainWindow)

    # MAIN WINDOW CONTENTS

    # create rectangle that represents the outer constraints of board
    boardBorder = Rectangle(Point(192, 64), Point(812, 704))
    boardBorder.draw(mainWindow)
    # draw board itself
    drawBoard(Point(192, 64), 640, mainWindow)

    # draw checker piece demo to view pieces
    # CheckerPiecesDemo.getMouse()
    # CheckerPiecesDemo.close()

    # draw main window
    mainWindow.getMouse()
    mainWindow.close()


main()
