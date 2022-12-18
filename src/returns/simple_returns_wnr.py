class simpleReturnsWNR:

    value = 0

    def Trade(self, buy=0, sell=0):
        if buy>=0 and sell>=0:
            self.value = self.value + sell - buy

    def getProfit(self):
        return self.value

class simpleReturnsWFR:

    value = 1

    def Trade(self, buy=1, sell=1):
        if buy>=0 and sell>=0:
            self.value *= sell/buy