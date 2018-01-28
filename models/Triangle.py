class Triangle():
    def __init__(self, posX1, posY1, posX2, posY2, posX3, posY3):
        self.posX = posX1
        self.posY = posY1
        self.posX2 = posX2
        self.posY2 = posY2
        self.posX3 = posX3
        self.posY3 = posY3

    def center(self):
        return (self.posX1+self.posX2+self.posX3)/3, (self.posY+self.posY2+self.posY3)/3