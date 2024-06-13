class Cycle:
    def __init__(self, iterable):
        self.data = [i for i in iterable]
        self.idx = 0

    def __next__(self):
        out = self.data[self.idx]
        self.idx += 1
        if self.idx >= len(self.data):
            self.idx = 0
        return out