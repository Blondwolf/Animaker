class Move(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.finish = False

    def move(self):
        translateX = 0
        translateY = 0
        if self.x > 0:
            self.x -= 1
            translateX = 1
        elif self.x < 0:
            self.x += 1
            translateX = -1
        if self.y > 0:
            self.y -= 1
            translateY = 1
        elif self.y < 0:
            self.y += 1
            translateY = -1
        if self.x == 0 and self.y == 0:
            self.finish = True
        return (translateX, translateY)

    def __str__(self):
        return "{}, {}".format(self.x, self.y)