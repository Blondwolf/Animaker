class Rotate(object):
    def __init__(self, alpha):
        self.alpha = alpha
        self.finish = False

    def rotate(self):
        pass

    def __str__(self):
        return "Rotate({})".format(self.alpha)