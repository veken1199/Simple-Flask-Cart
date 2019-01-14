from flask import Blueprint, session, request, jsonify
from database.schemas.product import *
from database.models.product import *
from database.schemas.purchase import *
from database.schemas.cart import *

from util.response_builder import ApiResponse
from util.cart_helpers import *
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.annotations import doc

cart_blueprint_name = 'cart'
cart_route = Blueprint(cart_blueprint_name, __name__, url_prefix='/cart')

@cart_route.route("", methods=['GET'])
@marshal_with(CartResponseSchema)
@doc(tags=['Cart'], description='''Endpoint to fetch the current cart content.
The cart is session based and valid until the session's expiry. The session in persistent
using SQLAlchemy. The default expiry is 31 days, the session will be deleted then.
The content of the session is a dictionary of purchase requests that would be eventually completed once
the user checks out: Due to limitations with swagger and marshal. The type of the cart is not shown:
cart: {
    "key" {
        added_on : Date
        current_inventory : int
        quantity: int // quantity requested to purchase
        product_id: int
    }
''')
def cart(**kwargs):
    cart = get_cart(session)

    # Calculate the total of the cart, currency, and inventory counts
    cart_total, currency = calculate_cart_total(cart, Product)
    cart_with_inventory = update_cart_inventory_counts(cart, Product)
    data = dict(cart=cart_with_inventory, cart_total=cart_total, cart_total_currency=currency)
    return ApiResponse(data=data, message='Successful operation', has_error=False).respond()


@cart_route.route("", methods=['POST'])
@marshal_with(CartResponseSchema)
@use_kwargs(PurchaseRequestSchema)
@doc(tags=['Cart'], description='''Endpoint to add or update if already exists a product
in the cart. This endpoint does the same validation as purchase endpoint in order to
avoid adding invalid purchase requests in the cart, such as inventory count and quantity
Due to limitations with swagger and marshal. The type of the cart is not shown:
cart: {
    "key": {
        added_on : Date
        current_inventory : int
        quantity: int // quantity requested to purchase
        product_id: int
    }
        ''')
def add_to_cart(**kwargs):
    purchase_request, err = purchase_request_schema.load(request.get_json(force=True))
    cart = get_cart(session)

    if err:
        return ApiResponse(message=err, has_error=True).respond()

    # Find if a such product exists
    product = Product.query.get(purchase_request['product_id'])

    if not product:
        return ApiResponse(message='No such product exists', has_error=False).respond()

    # Check if there is enough quantity
    if product.inventory_count < purchase_request['quantity']:
        return ApiResponse(message='There not enough for the requested quantity, current inventory: {}'.format(
            product.inventory_count), has_error=False).respond()

    # If we get here means the request is valid
    product.inventory_count -= purchase_request['quantity']

    # Add it to the cart, using schema allows us do validation and date initialization
    cart_item = CartItemSchema().dump(dict(product_id=product.id, quantity=purchase_request['quantity'])).data
    cart[str(product.id)] = CartItemSchema().dump(cart_item).data
    session['cart'] = cart

    # Calculate the total of the cart, currency, and inventory counts
    data = generate_cart_response(cart, Product)
    return ApiResponse(data=data, message='Item has been added to the cart', has_error=False).respond()


@cart_route.route("", methods=['DELETE'])
@marshal_with(CartResponseSchema)
@use_kwargs({'product_id':fields.Integer()})
@doc(tags=['Cart'], description='''Endpoint to delete a product from the cart. The 'product_id' should
exist in the cart already otherwise a message indicating that product was not found will be returned''')
def delete_from_cart(product_id = None, **kwargs):
    cart = get_cart(session)

    if not product_id:
        return ApiResponse(message='Missing product_id', has_error=True).respond()

    if not str(product_id) in cart:
        # Calculate the total of the cart, currency, and inventory counts
        return ApiResponse(message='No such product in the cart', has_error=True).respond()

    # Delete the product from the cart
    del cart[str(product_id)]
    session['cart'] = cart

    # Calculate the total of the cart, currency, and inventory counts
    data = generate_cart_response(cart, Product)
    return ApiResponse(data=data, message='Successfully deleted from the cart', has_error=False).respond()


@cart_route.route("/checkout", methods=['POST'])
@marshal_with(CartResponseSchema)
@doc(tags=['Cart'], description='''Endpoint to checkout and purchase all the items in the cart. The endpoint
will still check if the products in the cart are still available in our inventory. It will process the products
that are available in the inventory, the rest will be kept in the inventory.
message will be shown indicating which products have be purchased successfully
The elements that have not been purchased will be returned in the cart field''')
def cart_checkout():
    cart = get_cart(session)
    if len(cart) == 0:
        return ApiResponse(data=cart,
                           message='Your cart is empty',
                           has_error=False).respond()

    # Get the inventory counts for all products in the cart
    cart_with_inventories = update_cart_inventory_counts(cart, Product)

    # Store which products have been purchased
    purchased_ids = []

    for cart_item in cart_with_inventories.values():
        cart_item = CardItem(**cart_item)
        print(cart_item)
        if cart_item.current_inventory >= cart_item.quantity:
            product = Product.query.get(cart_item.product_id)
            product.inventory_count -= cart_item.quantity
            db.session.add(product)
            del cart[str(cart_item.product_id)]
            db.session.commit()
            purchased_ids.append(cart_item.product_id)

    session['cart'] = cart
    data = generate_cart_response(cart, Product)
    return ApiResponse(data=data, message='Successfully purchased the products with the following ids :{}'.format(purchased_ids),
                       has_error=False).respond()
