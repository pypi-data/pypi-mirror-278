from .Inventory import Inventory

def print_separator():
    print("=" * 30)

def print_menu():
    print_separator()
    print("         MAIN MENU        ")
    print_separator()
    print("1. Enter transaction")
    print("2. Check Inventory")
    print("3. Exit")
    print_separator()

def print_transaction_menu():
    print("\nTransaction Codes:")
    print("A - Add a new part")
    print("C - Change part description and price")
    print("D - Delete a part")
    print("X - Exit transaction")
    print_separator()

def print_inventory(inventory):
    inventory_list = inventory.getInventoryList()
    if not inventory_list:
        print("\n+++++++++++++++++++++++++")
        print("++++++++ EMPTY +++++++++")
        print("+++++++++++++++++++++++++")
    else:
        print("\n====== Inventory List ======")
        print(f"{'Part Number':<12} {'Description':<28} {'Price':>10}")
        print("-" * 50)
        for part in inventory_list:
            print(f"{part['part_number']:<12} {part['description']:<28} {part['price']:>10.2f}")
    print_separator()

def Menu():
    import sys

    inventory = Inventory()
    
    while True:
        print_menu()

        choice = input("Choose what to do (1, 2, or 3): ")

        if choice == '1':
            while True:
                print_transaction_menu()
                code = input("Enter transaction code (A, C, D, X): ").upper()

                if code == 'X':
                    break
                elif code == 'A':
                    part_number = input("Enter part number (10 characters max): ")
                    if len(part_number) > 10:
                        print("Part number must be 10 characters or less.")
                        continue

                    description = input("Enter description (26 characters max): ")
                    if len(description) > 26:
                        print("Description must be 26 characters or less.")
                        continue

                    try:
                        price = float(input("Enter price: "))
                    except ValueError:
                        print("Invalid price. Please enter a numeric value.")
                        continue

                    inventory.addPart(part_number, description, price)
                    print_inventory(inventory)

                elif code == 'C':
                    part_number = input("Enter part number: ")
                    if not inventory.searchPart(part_number):
                        print(f"Part with part number {part_number} does not exist in the inventory.")
                        continue

                    new_description = input("Enter new description: ")
                    try:
                        new_price = float(input("Enter new price: "))
                    except ValueError:
                        print("Invalid price. Please enter a numeric value.")
                        continue

                    inventory.changePartDescription(part_number, new_description, new_price)
                    print_inventory(inventory)

                elif code == 'D':
                    part_number = input("Enter part number: ")
                    if not inventory.searchPart(part_number):
                        print(f"Part with part number {part_number} does not exist in the inventory.")
                        continue

                    inventory.deletePart(part_number)
                    print("Part has been deleted from inventory!")
                    print_inventory(inventory)

                else:
                    print("Invalid transaction code.")

        elif choice == '2':
            print_inventory(inventory)

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

from .Inventory import Inventory

def print_separator():
    print("=" * 30)

def print_menu():
    print_separator()
    print("         MAIN MENU        ")
    print_separator()
    print("1. Enter transaction")
    print("2. Check Inventory")
    print("3. Exit")
    print_separator()

def print_transaction_menu():
    print("\nTransaction Codes:")
    print("A - Add a new part")
    print("C - Change part description and price")
    print("D - Delete a part")
    print("X - Exit transaction")
    print_separator()

def print_inventory(inventory):
    inventory_list = inventory.getInventoryList()
    if not inventory_list:
        print("\n+++++++++++++++++++++++++")
        print("++++++++ EMPTY +++++++++")
        print("+++++++++++++++++++++++++")
    else:
        print("\n====== Inventory List ======")
        print(f"{'Part Number':<12} {'Description':<28} {'Price':>10}")
        print("-" * 50)
        for part in inventory_list:
            print(f"{part['part_number']:<12} {part['description']:<28} {part['price']:>10.2f}")
    print_separator()

def Menu():
    import sys

    inventory = Inventory()
    
    while True:
        print_menu()

        choice = input("Choose what to do (1, 2, or 3): ")

        if choice == '1':
            while True:
                print_transaction_menu()
                code = input("Enter transaction code (A, C, D, X): ").upper()

                if code == 'X':
                    break
                elif code == 'A':
                    part_number = input("Enter part number (10 characters max): ")
                    if len(part_number) > 10:
                        print("Part number must be 10 characters or less.")
                        continue

                    description = input("Enter description (26 characters max): ")
                    if len(description) > 26:
                        print("Description must be 26 characters or less.")
                        continue

                    try:
                        price = float(input("Enter price: "))
                    except ValueError:
                        print("Invalid price. Please enter a numeric value.")
                        continue

                    inventory.addPart(part_number, description, price)
                    print_inventory(inventory)

                elif code == 'C':
                    part_number = input("Enter part number: ")
                    if not inventory.searchPart(part_number):
                        print(f"Part with part number {part_number} does not exist in the inventory.")
                        continue

                    new_description = input("Enter new description: ")
                    try:
                        new_price = float(input("Enter new price: "))
                    except ValueError:
                        print("Invalid price. Please enter a numeric value.")
                        continue

                    inventory.changePartDescription(part_number, new_description, new_price)
                    print_inventory(inventory)

                elif code == 'D':
                    part_number = input("Enter part number: ")
                    if not inventory.searchPart(part_number):
                        print(f"Part with part number {part_number} does not exist in the inventory.")
                        continue

                    inventory.deletePart(part_number)
                    print("Part has been deleted from inventory!")
                    print_inventory(inventory)

                else:
                    print("Invalid transaction code.")

        elif choice == '2':
            print_inventory(inventory)

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

