class Ball():
    def __init__(self, posX, posY, radius):
        self.posX = posX
        self.posY = posY
        self.radius = radius

    def center(self):
        return self.posX, self.posY