# path:
"""first work on making the init so that it draws the game window and board

 make a while loop that alternates between true and false for who the current player is, draw in accordance
        # to the location of a click when user clicks

need to create a method that checks the board to determine the winner
    - I did this with a list for top bottom and middle rows
    - I need to figure out how to check these lists

**************** SOLVED *******************
Current Issue:
    although I am appending the correct gameType (x or o) to the proper column list, I am not keeping track of where in
    the row the gameType is ending up.  I need to do this in order to determine the winner of the game
Solution:
    To solve this issue I will create 3 dictionaries (top, middle, bottom) with empty keys for left, middle, and
    right instead of the lists I made.  use this link for information on how to create an empty dictionary with keys:
    https://pythonguides.com/how-to-create-an-empty-python-dictionary/

    After I do this, I will be able to use a method similar to what I did in code wars to determine a winner. This
    gets rid of my issue of not having a long enough list due to sections not yet being clicked and allows me to insert
    values exactly where I want them to go in accordance to the location of the click
**************** SOLVED *******************

**************** WORK ON NOW ***************
    - Now that I have the dictionaries set up, I will have to figure out how to fetch their values and compare them
    to determine who the winner of the game is (checkWinner)  FINISHED
    - Need to figure out why my clear method is not always undrawing all of the gameTypes FINISHED
        - Solved this by making lists of all the Text objects drawn when clicking for an X or an O.  This list has the
        points of where the X or O is drawn, so I will be able to use that for drawing the winner line later on
        - Will probably have to iterate through these lists, find the highest x and y coordinate and the lowest x and y
        coordinate and use them to draw the line showing who won. use the .getAnchor() method to get back the
        coordinates.
        - Need to change how I did this, going for max and min does not work for a horizontal win.
        - Solution was to alter the checkwin method and derive the points based on where the win occured
    - Need to figure out how to get the window to not close when three in a row is achieved FINISED
        - Have this done, now I need to pause the game after the win line is drawn and wait for the reset click, can
        probably do this easier by putting the if self.reset button in the game while loop
        - ALso, currently you can continue clicking and placing gameTypes after the game is won, need to change this
            - FINISHED
    - Got win counter to work properly
    - Need to figure out how to make sure that I cannot place a gameType in a square that already exists FINISHED
        - This can probably be done by making use of the gameType list and extracting their points and making an if
        statement that cancels out clicks in an area that a gameType exists
    - Now I need to make it so that the gameType turn does not update unless a gameType is first placed
        - Did this by moving the update player method to the drawXO method after it recieves a condition that allows
        it to draw the gameType

    - Need to figure out how to make it so that I can press the quit button when a win occurs, only clicking the reset
    button works at the moment when there is a win SOLVED (had to add elif end clicked to check winner)
        - I also get an error if I press end when the board is not cleared (easiest solution is including a try except
        but I am not sure why it is even sending a point to the checkBox method when I click end in the first place)
        - SOLUTION: called for checkbox method after the condition for a valid gameType click is done

    - increased the bottom horizontal line by 10 pixels so that the diagonal win line matches up better, REMEMBER
    TO GO BACK AND ADJUST OTHER COORDS FOR RELATED OPERATIONS
    - If i do not hit reset before ending the program, the win counter does not increase the most recent win (i.e.
    clicking end will not increase the most recent win) SOLVED this by making adjustment to the check win method

**************** WORK ON LATER ***************
future issues to fix:
    - I will run into glitches when the user clicks on a line, this may mess up the sorting into the dictionaries.
    I will work around this by taking a click and then centering the X or O in the middle of the box it was in and use
    those centered coordinates as values instead.

future features:
    - I want to be able to have a reset button, it will clear the game board and will also have to empty out
    the dictionaries FINISHED
    - clean up the UI as much as possible
    - Make the gameTypes auto center themselves to the box they are clicked in FINISHED
    - determine winner FINISHED
**************** WORK ON LATER ***************

"""

from graphics import *
from Button import Button


# --------------------------------------------------------

class TicTacToe:

    # ---------------------------------------------------
    def __init__(self):
        self.oList = []
        self.xList = []
        self.clicks = 0
        self.X = None
        self.O = None
        self.winLine = None
        self.win = GraphWin("Tic Tac Toe", 400, 400)
        self.win.setCoords(0, 0, 400, 400)
        self.win.setBackground("dark gray")
        self.bottomLimit, self.topLimit = Point(75, 75), Point(325, 325)

        self.icon = Text(Point(25, 375), "X")
        self.icon.setSize(26)
        self.icon.draw(self.win)

        line1 = Line(Point(75, 147.5), Point(325, 147.5)).draw(self.win)
        line2 = Line(Point(75, 252.5), Point(325, 252.5)).draw(self.win)
        line3 = Line(Point(147.5, 75), Point(147.5, 325)).draw(self.win)
        line4 = Line(Point(252.5, 75), Point(252.5, 325)).draw(self.win)

        self.keyList = ["left", "middle", "right"]
        self.topDict = dict(zip(self.keyList, [None] * len(self.keyList)))
        self.middleDict = dict(zip(self.keyList, [None] * len(self.keyList)))
        self.bottomDict = dict(zip(self.keyList, [None] * len(self.keyList)))

        self.end = Button(self.win, Point(325, 45), 55, 30, "End")
        self.end.enable()

        self.reset = Button(self.win, Point(75, 45), 55, 30, "Reset")
        self.reset.enable()

        self.xWin, self.oWin = 0, 0
        self.playerX = True
        self.game = True
        while self.game:
            self.drawXO()
            self.checkWinner()

    @staticmethod
    def centerClick(click: Point):
        # top boxes
        if 75 < click.getX() < 147.5 and click.getY() > 252.5:
            return Point(75+36.25, 252.5+36.25)
        elif 147.5 < click.getX() < 252.5 and click.getY() > 252.5:
            return Point(147.5 + (252.5 - 147.5) / 2, 252.5+35.25)
        elif 252 < click.getX() < 325 and click.getY() > 252.5:
            return Point(252.5 + (325 - 252.5) / 2, 252.5 + 35.25)

        # middle boxes
        if 75 < click.getX() < 147.5 and click.getY() > 147.5: # might want to change this value in the future
            return Point(75+36.25, 137.5 + (252.5 - 137.5) / 2)
        elif 147.5 < click.getX() < 252.5 and click.getY() > 147.5:
            return Point(147.5 + (252.5 - 147.5) / 2, 137.5 + (252.5 - 137.5) / 2)
        elif 252 < click.getX() < 325 and click.getY() > 147.5:
            return Point(252.5 + (325 - 252.5) / 2, 137.5 + (252.5 - 137.5) / 2)

        # bottom boxes
        if 75 < click.getX() < 147.5 and click.getY() > 75:
            return Point(75 + 36.25, 75 + 35.25)
        elif 147.5 < click.getX() < 252.5 and click.getY() > 75:
            return Point(147.5 + (252.5 - 147.5) / 2, 75 + 36.25)
        elif 252 < click.getX() < 325 and click.getY() > 75:
            return Point(252.5 + (325 - 252.5) / 2, 75 + 36.25)


    @staticmethod
    def checkBox(click: Point, xList: list, oList: list, win: GraphWin):
        # make it so that the points of the text objects are auto centered first so that these are the only points
        # that are ever used for a gameType
        xPoints = []
        oPoints = []
        for item in xList:
            xPoints.append(item.getAnchor())
        for item in oList:
            oPoints.append(item.getAnchor())

        for point in xPoints:
            if click.getX() == point.getX() and click.getY() == point.getY():
                return True
        for point in oPoints:
            if click.getX() == point.getX() and click.getY() == point.getY():
                return True
        return False

    def drawXO(self):
        click = self.win.getMouse()
        p = self.centerClick(click)

        self.clicks += 1
        point = Point(click.getX(), click.getY())
        if self.bottomLimit.getX() <= point.getX() \
                <= self.topLimit.getX() and self.bottomLimit.getY() <= point.getY() <= self.topLimit.getY():
            exists = self.checkBox(p, self.xList, self.oList, self.win)
            # x is 1
            if self.playerX:
                if not exists:
                    self.drawX(p)
                    self.updatePlayer()
                    # self.drawX(centeredClick)
                    if point.getY() >= 252.5:
                        if point.getX() <= 147.5:
                            self.topDict.update(dict(left=1))
                        elif 147.5 <= point.getX() <= 252.5:
                            self.topDict.update(dict(middle=1))
                        elif point.getX() >= 252.5:
                            self.topDict.update(dict(right=1))
                    elif 147.5 <= point.getY() <= 252.5:
                        if point.getX() <= 147.5:
                            self.middleDict.update(dict(left=1))
                        elif 147.5 <= point.getX() <= 252.5:
                            self.middleDict.update(dict(middle=1))
                        elif point.getX() >= 252.5:
                            self.middleDict.update(dict(right=1))
                    elif point.getY() <= 137.5:
                        if point.getX() <= 147.5:
                            self.bottomDict.update(dict(left=1))
                        elif 147.5 <= point.getX() <= 252.5:
                            self.bottomDict.update(dict(middle=1))
                        elif point.getX() >= 252.5:
                            self.bottomDict.update(dict(right=1))
            # o is 2
            else:
                if not exists:
                    self.draw0(p)
                    self.updatePlayer()
                    if point.getY() >= 252.5:
                        if point.getX() <= 147.5:
                            self.topDict.update(dict(left=2))
                        elif 147.5 <= point.getX() <= 252.5:
                            self.topDict.update(dict(middle=2))
                        elif point.getX() >= 252.5:
                            self.topDict.update(dict(right=2))
                    elif 137.5 <= point.getY() <= 252.5:
                        if point.getX() <= 147.5:
                            self.middleDict.update(dict(left=2))
                        elif 147.5 <= point.getX() <= 252.5:
                            self.middleDict.update(dict(middle=2))
                        elif point.getX() >= 252.5:
                            self.middleDict.update(dict(right=2))
                    elif point.getY() <= 137.5:
                        if point.getX() <= 147.5:
                            self.bottomDict.update(dict(left=2))
                        elif 147.5 <= point.getX() <= 252.5:
                            self.bottomDict.update(dict(middle=2))
                        elif point.getX() >= 252.5:
                            self.bottomDict.update(dict(right=2))
        else:
            if self.end.clicked(click):
                self.game = False
            elif self.reset.clicked(click):
                self.clearBoard()
                self.topDict = dict(zip(self.keyList, [None] * len(self.keyList)))
                self.middleDict = dict(zip(self.keyList, [None] * len(self.keyList)))
                self.bottomDict = dict(zip(self.keyList, [None] * len(self.keyList)))

    def clearBoard(self):
        for drawing in self.xList:
            drawing.undraw()
        for drawing in self.oList:
            drawing.undraw()
        self.xList.clear()
        self.oList.clear()
        try:
            self.winLine.undraw()
        except:
            pass

    def drawX(self, point: Point):
        self.X = Text(point, "X")
        self.X.setSize(36)
        self.X.draw(self.win)
        self.xList.append(self.X)

    def draw0(self, point: Point):
        self.O = Text(point, "O")
        self.O.setSize(36)
        self.O.draw(self.win)
        self.oList.append(self.O)

    def drawWinLine(self, lP, rP):
        self.winLine = Line(lP, rP)
        self.winLine.setOutline("red")
        self.winLine.draw(self.win)

    def updatePlayer(self):
        if self.playerX:
            self.playerX = False
            self.icon.setText("O")
        else:
            self.playerX = True
            self.icon.setText("X")

    def checkWinner(self):
        # catches the winner who gets all of a row
        win = False
        if self.topDict['left'] == self.topDict['middle'] == self.topDict['right'] is not None:
            lP, rP = Point(75, 289), Point(325, 289)
            self.drawWinLine(lP, rP)
            win = True
        elif self.middleDict['left'] == self.middleDict['middle'] == self.middleDict['right'] is not None:
            lP, rP = Point(75, 195), Point(325, 195)
            self.drawWinLine(lP, rP)
            win = True
        elif self.bottomDict['left'] == self.bottomDict['middle'] == self.bottomDict['right'] is not None:
            lP, rP = Point(75, 106.25), Point(325, 106.25)
            self.drawWinLine(lP, rP)
            win = True

        # catches the winner who gets all of a column
        if self.topDict['left'] == self.middleDict['left'] == self.bottomDict['left'] is not None:
            lP, rP = Point(111.25, 75), Point(111.25, 325)
            self.drawWinLine(lP, rP)
            win = True
        elif self.topDict['middle'] == self.middleDict['middle'] == self.bottomDict['middle'] is not None:
            lP, rP = Point(200, 75), Point(200, 325)
            self.drawWinLine(lP, rP)
            win = True
        elif self.topDict['right'] == self.middleDict['right'] == self.bottomDict['right'] is not None:
            lP, rP = Point(288.75, 75), Point(288.75, 325)
            self.drawWinLine(lP, rP)
            win = True

        # diagonal winner
        if self.topDict['left'] == self.middleDict['middle'] == self.bottomDict['right'] is not None:
            lP, rP = Point(75, 325), Point(325, 75)
            self.drawWinLine(lP, rP)
            win = True
        elif self.topDict['right'] == self.middleDict['middle'] == self.bottomDict['left'] is not None:
            lP, rP = Point(325, 325), Point(75, 75)
            self.drawWinLine(lP, rP)
            win = True

        if win:
            while True:
                p = self.win.getMouse()
                if self.reset.clicked(p):
                    if not self.playerX:
                        self.xWin += 1
                    else:
                        self.oWin += 1
                    self.clearBoard()
                    self.topDict = dict(zip(self.keyList, [None] * len(self.keyList)))
                    self.middleDict = dict(zip(self.keyList, [None] * len(self.keyList)))
                    self.bottomDict = dict(zip(self.keyList, [None] * len(self.keyList)))
                    break
                elif self.end.clicked(p):
                    self.game = False
                    if not self.playerX:
                        self.xWin += 1
                    else:
                        self.oWin += 1
                    break

    def __str__(self) -> str:
        string = f"Top -> left: {self.topDict['left']}, middle: {self.topDict['middle']} right: {self.topDict['right']}" \
                 f"\nmiddle -> {self.middleDict['left']}, middle: {self.middleDict['middle']} right: {self.middleDict['right']}" \
                 f"\nbottom -> {self.bottomDict['left']}, middle: {self.bottomDict['middle']} right: {self.bottomDict['right']}" \
                 f"\n({self.xList}) ({self.oList})" \
                 f"\nX wins: {self.xWin}\nO wins: {self.oWin}"

        return string


# ------------------------------------------------------
def main():
    game = TicTacToe()
    print(game)


if __name__ == "__main__":
    main()
