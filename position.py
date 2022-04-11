#zhuojinjun

class position():

    def __init__(self):
        self.cc = "0"
        self.cop = 0.0
        self.ccp = 0.0
        self.cn = 0
        self.pc = "0"
        self.pop = 0.0
        self.pcp = 0.0
        self.pn = 0
        self.pf = 0.0
        self.log = []

    def initialCall(self):
        self.cc = "0"
        self.cop = 0.0
        self.ccp = 0.0
        self.cn = 0
    def initialput(self):
        self.pc = "0"
        self.pop = 0.0
        self.pcp = 0.0
        self.pn = 0
    
    def openCall(self,contract, price, num):
        self.cc = contract
        self.cop = price
        self.cn = num
        position.log(self,"openCall", contract, price)

    def closeCall(self,contract, price):
        if self.cc == contract:
            self.ccp = price
            profit = (self.cop - self.ccp) * 10000.0 * self.cn
            position.profit(self,profit)
            position.initialCall(self)
            position.log(self,"closeCall", contract, price)
        else:
            print("wrong close call")

    def openPut(self,contract, price, num):
        self.pc = contract
        self.pop = price
        self.pn = num
        position.log(self,"openPut", contract, price)

    def closePut(self,contract, price):
        if self.pc == contract:
            self.pcp = price
            profit = (self.pop - self.pcp) * 10000.0 * self.pn
            position.profit(self,profit)
            position.initialput(self)
            position.log(self,"closePut", contract, price)
        else:
            print("wrong close put")

    def profit(self,profit):
        self.pf += profit

    def log(self,symbol,contract,price):
        value = symbol + ", the contract is: " + contract + ", the price is: " +str(price)
        self.log.append(value)

    def getPosition(self):
        return self.cc, self.cn, self.pc, self.pn

    def getProfit(self):
        return self.pf

    def getLog(self):
        return self.log

# pos = position()
# pos.openCall("1",1.01,100)
# a,b,c,d = pos.getPosition()
# print(a,b,c,d)

# pos.openPut("2",2.01,50)
# a,b,c,d = pos.getPosition()
# print(a,b,c,d)

# pos.closeCall("1",0.95)
# a,b,c,d = pos.getPosition()
# print(a,b,c,d)

# pos.closePut("2",1.99)
# a,b,c,d = pos.getPosition()
# print(a,b,c,d)

# profit = pos.getProfit()
# print(profit)

# log = pos.getLog()
# print(log)