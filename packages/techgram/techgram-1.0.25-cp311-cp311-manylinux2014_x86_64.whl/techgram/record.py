class Record:
    def __init__(self):
            self.recorder = {}

    def addFirst(self, key, value):
        if key in self.recorder:
            del self.recorder[key]
        self.recorder[key] = value
        return self.recorder[key]

    def findFirst(self, key):
        try:
            data = self.recorder[key]
            return data
        except KeyError:
            return None

    def delFirst(self, key):
        del self.recorder[key]