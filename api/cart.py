from flask import Blueprint, session, request, jsonify
from database.schemas.product import *
from database.models.product import *
from database.schemas.purchase import *
from database.models.cart import *

from util.response_builder import ApiResponse
from util.cart_session import *
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.annotations import doc

cart_blueprint_name = 'cart'
cart_route = Blueprint(cart_blueprint_name, __name__, url_prefix='/cart')

@cart_route.route("", methods=['GET'])
@doc(tags=['Cart'], description='''Endpoint to fetch the current cart content.
The cart is session based and valid until the session's expiry. The session in persistent
in SQLAlchemy. The default expiry day is 31 day. The content of the session is a dictionary of
purchase requests that would be eventually completed once the user checks out''')
def cart(**kwargs):
    # Check if there is a cart, if not means there is no session either
    cart = get_cart(session)

    return ApiResponse(data=cart).respond()


@cart_route.route("", methods=['POST'])
@marshal_with(PurchaseResponseSchema)
@use_kwargs(PurchaseRequestSchema)
@doc(tags=['Cart'], description='''Endpoint to fetch the current cart content.
The cart is session based and valid until the session's expiry. The session in persistent
in SQLAlchemy. The default expiry day is 31 day. The content of the session is a list of
purchase requests that would be eventually completed once the user checks out''')
def post_cart(**kwargs):
    purchase_request, err = purchase_request_schema.load(request.get_json(force=True))

    # Check if there is a cart, if not means there is no session either
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

    ''' If we get here means the request is valid, the purchase will be done
        ideally the user would be logged in to record the request, but now we assume
        only process the purchase request
    '''
    product.inventory_count -= purchase_request['quantity']

    # Add it to the cart
    cart_item = CartItem(product.id, purchase_request['quantity'])
    cart[str(product.id)] = cart_item.__dict__
    session['cart'] = cart

    return ApiResponse(message='Item has been added to the cart', has_error=False).respond()

