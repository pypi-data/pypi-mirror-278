class Transaction:
    def __init__(self, code, partNumber, description, price):
        self.code = code
        self.partNumber = partNumber
        self.description = description
        self.price = price

    def getCode(self):
        return self.code

    def getPartNumber(self):
        return self.partNumber

    def getDescription(self):
        return self.description

    def getPrice(self):
        return self.price
