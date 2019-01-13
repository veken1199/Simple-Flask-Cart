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
    hasError = fields.Boolean()
    data = fields.Nested(ProductSchema, many=True)


class ProductRequestSchema(Schema):
    min_price = fields.Float(default=0)
    max_price = fields.Float(default=sys.maxsize)
    available = fields.Boolean(default=False)


products_schema = ProductSchema(many=True)
product_response_schema = ProductResponseSchema()
product_request_schema = ProductRequestSchema()