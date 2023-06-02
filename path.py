import os


class path:
    def __init__(self):
        self.ROOTPATH = os.path.dirname(os.path.abspath(__file__))

    def start(self):
        return self.ROOTPATH
