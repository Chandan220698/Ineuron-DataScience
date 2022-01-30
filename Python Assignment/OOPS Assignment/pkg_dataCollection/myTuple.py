class customTuple:

    def __init__(self, tup):
        if type(tup) != tuple:
            raise Exception("Not a Tuple")
        else:
            self.tup = tup

    def display(self):
        return self.tup

    def countData(self, searchData):
        count = 0
        for i in self.tup:
            if i == searchData:
                count += 1

        return count
