
# A class that represents a product stored in the cart
# this is used to deserialize json objects stored into the cart session
# to application object
class CardItem():
    added_on = ''
    product_id = ''
    current_inventory = ''
    quantity = ''

    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
