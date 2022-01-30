class customDict:

    def __init__(self, d):
        if type(d) != dict:
            raise Exception("Not a Dict")
        else:
            self.d = d

    def display(self):
        return self.d

    def getItems(self):
        temp = str(self.d)

        temp = temp.removeprefix('{')
        temp = temp.removesuffix('}')

        temp = temp.replace(' ', '')
        temp = temp.split(',')

        return temp
