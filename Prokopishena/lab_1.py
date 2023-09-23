class Bill:
    def __init__(self, limitingAmount: float) :
        self.limitingAmount = limitingAmount
        self.currentDebt = 0.0

    def check(self, amount: float) -> float:
        return self.currentDebt + amount <= self.limitingAmount

    def add(self, amount: float) ->None:
        if self.check(amount):
            self.currentDebt += amount
        else:
            print("Bill limit exceeded!")

    def pay(self, amount:float) ->None:
        if self.check(amount):
            self.currentDebt -= amount
        else:
            print("Bill limit exceeded!")

    def changeTheLimit(self, amount: float)->None:
        self.limitingAmount = amount

    def getLimitingAmount(self):
        return self.limitingAmount

    def getCurrentDebt(self):
        return self.currentDebt


class Operator:
    def __init__(self, ID:int, talkingCharge:float, messageCost:float, networkCharge:float, discountRate:int):
        self.ID = ID
        self.talkingCharge = talkingCharge
        self.messageCost = messageCost
        self.networkCharge = networkCharge
        self.discountRate = discountRate

    def calculateTalkingCost(self, minute:int, customer) -> float:
        if customer.getAge() < 18 or customer.getAge() > 65:
            return minute * self.talkingCharge * (1 - self.discountRate / 100)
        else:
            return minute * self.talkingCharge

    def calculateMessageCost(self, quantity:int, customer, other) -> float:
        if customer.getOperator() == other.getOperator():
            return quantity * self.messageCost * (1 - self.discountRate / 100)
        else:
            return quantity * self.messageCost

    def calculateNetworkCost(self, amount:float) -> float:
        return amount * self.networkCharge


    def setTalkingCharge(self, talkingCharge):
        self._talkingCharge = talkingCharge

    def setMessageCost(self, messageCost):
        self._messageCost = messageCost

    def setNetworkCharge(self, networkCharge):
        self._networkCharge = networkCharge

    def setDiscountRate(self, discountRate):
        self._discountRate = discountRate

    def getTalkingCharge(self):
        return self.talkingCharge

    def getMessageCost(self):
        return self.messageCost

    def getNetworkCharge(self):
        return self.networkCharge

    def getDiscountRate(self):
        return self.discountRate

class Customer:
    def __init__(self, ID:int, name:str, age:int, operator, bill, limitingAmount):
        self.ID = ID
        self.name = name
        self.age = age
        self.operator = operator
        self.bill = bill
        self.limitingAmount = limitingAmount

    def talk(self, minute:int, other) -> None:
        if self.operator and other.operator:
            cost = self.operator.calculateTalkingCost(minute, self)
            if self.bill.check(cost):
                self.bill.add(cost)
                print(f"{self.name} talked to {other.name} for {minute} minutes. Cost: {cost}")
            else:
                print(f"{self.name} cannot talk, bill limit exceeded.")
        else:
            print("Both customers must have operators to talk.")

    def message(self, quantity:int, other) -> None:
        if self.operator and other.operator:
            cost = self.operator.calculateMessageCost(quantity, self, other)
            if self.bill.check(cost):
                self.bill.add(cost)
                print(f"{self.name} sent {quantity} messages to {other.name}. Cost: {cost}")
            else:
                print(f"{self.name} cannot send messages, bill limit exceeded.")
        else:
            print("Both customers must have operators to send messages.")

    def connection(self, amount:float) -> None:
        if self.operator:
            cost = self.operator.calculateNetworkCost(amount)
            if self.bill.check(cost):
                self.bill.add(cost)
                print(f"{self.name} used {amount} MB of data. Cost: {cost}")
            else:
                print(f"{self.name} cannot use the internet, bill limit exceeded.")
        else:
            print("Customer must have an operator to use the internet.")

    def payBill(self, amount:float) -> None:
        self.bill.pay(amount)
        print(f"{self.name} paid {amount} for the bill.")

    def changeOperator(self, new_operator):
        self.operator = new_operator
        print(f"{self.name} changed the operator to Operator {new_operator.ID}.")

    def changeBillLimit(self, amount:float):
        self.bill.changeTheLimit(amount)
        print(f"{self.name}'s bill limit changed to {amount}.")

    def getAge(self):
        return self.age

    def getOperator(self):
        return self.operator

    def getBill(self):
        return self.bill


# Initialize operators
operators = [
    Operator(0, 0.1, 0.05, 0.01, 10),
    Operator(1, 0.1, 0.08, 0.02, 15),

]

# Initialize bills
bills = [
    Bill(50.0),
    Bill(100.0),
]

# Initialize customers
customers = [
    Customer(0, "Alice", 15, operators[0], bills[0], 50.0),
    Customer(1, "Bob", 30, operators[1], bills[1], 100.0),
]

# Perform actions

customers[0].talk(15, customers[1])
customers[0].message(20, customers[1])
customers[1].connection(500)
customers[0].payBill(20)
customers[1].changeOperator(operators[0])
customers[1].changeBillLimit(150)
