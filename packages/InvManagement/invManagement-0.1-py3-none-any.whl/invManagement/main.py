from .inventory import Inventory

def main():
    inventory = Inventory()
    
    while True:
        print("==========================")
        print("1. Enter transaction\n2. Check Inventory\n3. Exit")
        print("==========================")

        choice = input("Choose what to do (1, 2, or 3): ")

        if choice == '1':
            code = input("Enter transaction code (A, C, D, X): ").upper()

            while code != 'X':
                if code == 'A':
                    part_number = input("Enter part number (10 Characters max): ")

                    if len(part_number) > 10:
                        print("Part number must be 10 characters or less.")
                        continue

                    description = input("Enter description (26 Characters max): ")

                    if len(description) > 26:
                        print("Description must be 26 characters or less.")
                        continue

                    try:
                        price = float(input("Enter price: "))
                    except ValueError:
                        print("Invalid price. Please enter a numeric value.")
                        continue

                    inventory.add_part(part_number, description, price)
                    print("====== Inventory List: =======")
                    inventory.print_inventory()

                elif code == 'C':
                    part_number = input("Enter part number: ")
                    
                    if inventory.search_part(part_number):
                        new_description = input("Enter new description: ")
                        try:
                            new_price = float(input("Enter new price: "))
                        except ValueError:
                            print("Invalid price. Please enter a numeric value.")
                            continue

                        inventory.change_part_description(part_number, new_description, new_price)
                        print("====== Inventory List: =======")
                        inventory.print_inventory()
                    else:
                        print(f"Part with part number {part_number} does not exist in the inventory.")

                elif code == 'D':
                    part_number = input("Enter part number: ")

                    if inventory.search_part(part_number):
                        inventory.delete_part(part_number)
                        print("====== Inventory List: =======")
                        inventory.print_inventory()
                    else:
                        print(f"Part with part number {part_number} does not exist in the inventory.")

                else:
                    print("Invalid transaction code")

                code = input("Enter transaction code (A, C, D, X): ").upper()

        elif choice == '2':
            inventory.print_inventory()

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
