from graphics import *

class Button:

    def __init__(self, win: GraphWin, center: Point, width: float, height: float, label: str):
        halfWidth, halfHeight = width / 2.0, height / 2.0
        x, y = center.getX(), center.getY()

        self.xMax, self.xMin = x + halfWidth, x - halfWidth
        self.yMax, self.yMin = y + halfHeight, y - halfHeight

        p1 = Point(self.xMin, self.yMin)
        p2 = Point(self.xMax, self.yMax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill("lightgray")
        self.rect.draw(win)

        self.label = Text(center, label)
        self.label.draw(win)

        self.disable()

    def disable(self):
        self.label.setFill("darkgray")
        self.rect.setWidth(1)
        self.enabled = False

    def clicked(self, p) -> bool:
        return (self.enabled and self.xMin <= p.getX() <= self.xMax and
                self.yMin <= p.getY() <= self.yMax)

    def getLabel(self) -> str:
        return self.label.getText()

    def setLabel(self, label: str):
        self.label.setText(label)

    def enable(self):
        self.label.setFill("black")
        self.rect.setWidth(2)
        self.enabled = True






