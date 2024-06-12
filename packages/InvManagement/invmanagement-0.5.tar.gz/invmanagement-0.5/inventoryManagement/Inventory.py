from .Part import Part

class Inventory:
    def __init__(self):
        self.inventory = {}

    def addPart(self, partNumber, description, price):
        if partNumber in self.inventory:
            print(f"Part with part number {partNumber} already exists in the inventory.")
        else:
            self.inventory[partNumber] = Part(partNumber, description, price)

    def searchPart(self, partNumber):
        return partNumber in self.inventory

    def changePart(self, partNumber, newDescription, price):
        part = self.inventory.get(partNumber)
        if part:
            part.setPartNumber(partNumber)
            part.setPartDescription(newDescription)
            part.setPrice(price)

    def changePartDescription(self, partNumber, newDescription, newPrice):
        part = self.inventory.get(partNumber)
        if part:
            part.setPartDescription(newDescription)
            part.setPrice(newPrice)

    def deletePart(self, partNumber):
        if partNumber in self.inventory:
            del self.inventory[partNumber]

    def printInventory(self):
        if not self.inventory:
            print("Inventory is empty")
        else:
            for part in self.inventory.values():
                print(part)

    def getInventoryList(self):
        return [{"part_number": part.partNumber, "description": part.partDescription, "price": part.price} for part in self.inventory.values()]

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
