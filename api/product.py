from flask import Blueprint, request
from database.schemas.product import *
from database.models.product import *
from util.response_builder import ApiResponse
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.annotations import doc


product_blueprint_name = 'product'
product_route = Blueprint(product_blueprint_name, __name__, url_prefix='/product')


@product_route.route("/all")
@marshal_with(ProductResponseSchema)
@doc(tags=['Product'], description="""Returns a list products based on parameters passed in the request
product/all?available=<bool>&min_price=<number>&max_price<number>""")
def get_products():

    # Check if the client  requested the only available products
    req, errors = product_request_schema.dump(request.args.to_dict())
    if errors:
        return ApiResponse(message=errors, has_error=True).respond()

    # Assigning query function reference so that we can use it with different filters
    product_query = Product.query

    # Apply the filter to return only products with count > 0 if `available is found in the request
    if req['available']:
        product_query = product_query.filter((Product.inventory_count == 0) == req['available'])
    # Apply filters
    products = product_query.filter(Product.price >= req['min_price']) \
        .filter(Product.price <= req['max_price']).all()
    return ApiResponse(data=products_schema.dump(products, many=True).data)


@product_route.route("/<id>")
@marshal_with(ProductResponseSchema)
@doc(tags=['Product'], description='Returns a single product for the database based on the id passed')
def get_product(id):
    product = Product.query.get(id)

    # Additional Feature: After every time we visit a product, it `visits`
    # count increments. A way of showing which product is the most popular
    product.increment_visit()
    db.session.add(product)
    db.session.commit()

    return ApiResponse(data=products_schema.dump([product]).data)


