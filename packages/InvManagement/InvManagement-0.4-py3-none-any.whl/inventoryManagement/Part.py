class Part:
    def __init__(self, partNumber, partDescription, price):
        self.partNumber = partNumber
        self.partDescription = partDescription
        self.price = price

    def getPartNumber(self):
        return self.partNumber

    def getPartDescription(self):
        return self.partDescription

    def getPrice(self):
        return self.price

    def setPartNumber(self, partNumber):
        self.partNumber = partNumber

    def setPartDescription(self, partDescription):
        self.partDescription = partDescription

    def setPrice(self, price):
        self.price = price

    def __str__(self):
        return f"Part Number: {self.partNumber}\nDescription: {self.partDescription}\nPrice: {self.price}"
