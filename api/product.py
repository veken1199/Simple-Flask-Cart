import sys
from flask import Blueprint, request
from flask_apispec import marshal_with
from flask_apispec.annotations import doc

from database.schemas.product import ProductSchema, ProductRequestSchema, ProductResponseSchema, validate
from database.models.product import Product, db
from util.response_builder import ApiResponse
from util.product_helper import product_id_validator


product_blueprint_name = 'product'
product_route = Blueprint(product_blueprint_name, __name__, url_prefix='/product')


@product_route.route('/all')
@marshal_with(ProductResponseSchema)
@doc(tags=['Product'], description='''Returns a list of products based on args passed in the request:
product/all?available=<bool>&min_price=<number>&max_price<number>&limit<int>&page<int>
the default values for the arguments above are:
    available = false
    min_price = 0
    max_price = inf
    page = 0  // min = 0 & max = 1000
    limit= 25 // min = 1 & max = 100000
From above, we can see that the page=0 will return 25 product, then page=1 will return the next 25 products''')
def get_products():

    # Check and validate client req, deserialize it to ProductRequest
    # It also sets the default values for missing args in the request
    product_request, err = ProductRequestSchema().load(request.args.to_dict())
    if err:
        return ApiResponse(message=err, has_error=True).respond()

    # Assigning query function reference so that we can use it with different filters
    product_query = Product.query

    # Apply the filter to return only products with inventory_count > 0 if `available is found in the request
    if product_request.available:
        product_query = product_query.filter((Product.inventory_count > 0))

    # Apply filters
    products = product_query.filter(Product.price >= product_request.min_price) \
        .filter(Product.price <= product_request.max_price)\
        .offset(product_request.page * product_request.limit)\
        .limit(product_request.limit).all()

    return ApiResponse(data=ProductSchema(many=True).dump(products, many=True).data)


@product_route.route('/<int:product_id>')
@marshal_with(ProductResponseSchema)
@doc(tags=['Product'], description='Returns a single product for the database based on the id passed')
@product_id_validator('product_id')
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return ApiResponse(message='Product not found', has_error=False)

    # Additional Feature: After every time we visit a product, its `visits`
    # count increments. A way of showing which product is the most popular
    product.increment_visit()
    db.session.add(product)
    db.session.commit()

    return ApiResponse(data=ProductSchema(many=True).dump([product]).data)



