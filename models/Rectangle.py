class Rectangle():
    def __init__(self, posX, posY, width, height):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height

    def center(self):
        return (self.posX+self.width)/2, (self.posY+self.height)/2