from flask import Blueprint, request
from database.schemas.product import *
from database.models.product import *
from database.schemas.purchase import *

from util.response_builder import ApiResponse
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.annotations import doc

purchase_blueprint_name = 'purchase'
purchase_route = Blueprint(purchase_blueprint_name, __name__, url_prefix='/purchase')


@purchase_route.route("", methods=['POST'])
@use_kwargs(PurchaseRequestSchema)
@marshal_with(PurchaseResponseSchema)
@doc(tags=['Purchase'], description=''' Endpoint to submit the purchase request
You need to POST valid product_id and a valid quantity.
The purchase request will only be completed in case there was at least
the exact quantity of the product to be purchased in our inventory''')
def purchase(**kwargs):
    purchase_request, err = purchase_request_schema.load(request.get_json(force=True))
    if err:
        return ApiResponse(message=err, has_error=True).respond()

    # Find if a such product exists
    product = Product.query.get(purchase_request['product_id'])

    if not product:
        return ApiResponse(message='No such product exists', has_error=False).respond()

    # Check if there is enough quantity
    if product.inventory_count < purchase_request['quantity']:
        return ApiResponse(message='There not enough for the requested quantity, current inventory: {}'.format(product.inventory_count), has_error=False).respond()

    ''' If we get here means the request is valid, the purchase will be done
        ideally the user would be logged in to record the request, but now we assume
        only process the purchase request
    '''
    product.inventory_count -= purchase_request['quantity']
    db.session.add(product)
    db.session.commit()

    return ApiResponse(message='Purchase has been completed!', has_error=False).respond()

