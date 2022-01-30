class customSet:

    def __init__(self, s):
        if type(s) != set:
            raise Exception("Not a Set")
        else:
            self.s = s

    def display(self):
        return self.s

    def popSet(self):
        temp = list(self.s)
        temp = temp[0: len(temp)-1]

        self.s = set(temp)

        return self.s
