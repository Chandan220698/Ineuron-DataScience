class customList:

    def __init__(self, l):
        if type(l) != list:
            raise Exception("Not a list")
        else:
            self.l = l

    def display(self):
        return self.l

    def appendList(self, data):
        self.l += [data]
        return data
