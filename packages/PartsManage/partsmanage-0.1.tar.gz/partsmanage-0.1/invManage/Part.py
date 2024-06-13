class Part:
    def __init__(self, part_number, part_description, price):
        self.part_number = part_number
        self.part_description = part_description
        self.price = price

    def get_part_number(self):
        return self.part_number

    def get_part_description(self):
        return self.part_description

    def get_price(self):
        return self.price

    def set_part_number(self, part_number):
        self.part_number = part_number

    def set_part_description(self, part_description):
        self.part_description = part_description

    def set_price(self, price):
        self.price = price

    def __str__(self):
        return f"Part Number: {self.part_number}\nDescription: {self.part_description}\nPrice: {self.price}"
