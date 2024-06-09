from .part import Part

class Inventory:
    def __init__(self):
        self.inventory = {}

    def add_part(self, part_number, description, price):
        if part_number in self.inventory:
            print(f"Part with part number {part_number} already exists in the inventory.")
        else:
            self.inventory[part_number] = Part(part_number, description, price)

    def search_part(self, part_number):
        return part_number in self.inventory

    def change_part_description(self, part_number, new_description, new_price):
        part = self.inventory.get(part_number)
        if part:
            part.set_part_description(new_description)
            part.set_price(new_price)

    def delete_part(self, part_number):
        if part_number in self.inventory:
            del self.inventory[part_number]
            print("Part has been deleted from inventory!")
        else:
            print(f"Part with part number {part_number} does not exist in the inventory.")

    def print_inventory(self):
        if not self.inventory:
            print("Inventory is empty")
        else:
            for part in self.inventory.values():
                print(part)

