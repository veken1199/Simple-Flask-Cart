from database.models.currency import CurrencyEnum
from copy import deepcopy
from database.models.cart import CardItem


def get_cart(session):
    if 'cart' not in session:
        session['cart'] = dict()
    return session['cart']


''' Helper function to calculate the total of products in the cart.
 It returns the total and the currency. The currency are not taken into
 consideration during the calculations '''
def calculate_cart_total(cart, model):
    sum = 0
    product_currency = CurrencyEnum.CAD.value
    product_dict = get_products_from_cart(cart, model)
    for cart_item in cart.values():
        sum += cart_item['quantity'] * product_dict[cart_item['product_id']].price
    return format(sum, '.2f'), product_currency


'''This function will fetch all product info from the the model provided.
The reason for this approach is that we don't want to store in the cart data
that could change over time such as price and inventory count'''
def get_products_from_cart(cart, model):
    # Get all the products that we will need
    query = model.query.filter(model.id.in_([id for id in cart.keys()]))
    products = query.all()
    query.session.close()

    # Convert the list to dictionary and the key is product id. Remember that product_id is string in the cart
    product_dict = {product.id: CardItem(price=product.price, inventory_count=product.inventory_count) for product in products}
    return product_dict


'''This function is used to traverse over the products in the cart
in order to display the most up to date values of products inventory count. '''
def update_cart_inventory_counts(cart, model):
    product_dict = get_products_from_cart(cart, model)
    copy_card = deepcopy(cart)
    for cart_item in copy_card.values():
        cart_item['current_inventory'] = product_dict[cart_item['product_id']].inventory_count
    return copy_card


def generate_cart_response(cart, model):
    if not cart:
        return dict(cart=cart, cart_total=0, cart_total_currency='')
    cart_total, currency = calculate_cart_total(cart, model)
    cart_with_inventory = update_cart_inventory_counts(cart, model)
    data = dict(cart=cart_with_inventory, cart_total=cart_total, cart_total_currency=currency)

    return data