import sys
from marshmallow import Schema, fields, pre_load, validate


class ProductSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    price = fields.Float()
    inventory_count = fields.Integer()
    visits = fields.Integer()
    currency_unit = fields.String()


# Schema that represents Product HTTP response
class ProductResponseSchema(Schema):
    message = fields.String()
    has_error = fields.Boolean()
    data = fields.Nested(ProductSchema, many=True)


# Schema that represents Product HTTP response
class ProductRequestSchema(Schema):
    min_price = fields.Float(missing=0, default=0)
    max_price = fields.Float(missing=sys.maxsize, default=sys.maxsize)
    limit = fields.Integer(missing=25, validate=validate.Range(min=1, max=100000))
    page = fields.Integer(missing=0, validate=validate.Range(min=0, max=1000))
    available = fields.Boolean(missing=False, default=False)

products_schema = ProductSchema(many=True)
product_response_schema = ProductResponseSchema()
product_request_schema = ProductRequestSchema()