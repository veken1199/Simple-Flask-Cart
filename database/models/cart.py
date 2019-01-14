class CardItem():
    added_on = ""
    product_id = ""
    current_inventory = ""
    quantity = ""

    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)