from datetime import date


class CartItem():
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quntity = quantity
        self.added_on = str(date.today())