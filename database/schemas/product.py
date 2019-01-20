import sys
from database.schemas.base_response import BaseResponseSchema
from marshmallow import Schema, fields, post_load, validate, ValidationError
import constants


class ProductSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    price = fields.Float()
    inventory_count = fields.Integer()
    visits = fields.Integer()
    currency_unit = fields.String()


# Schema that represents Product HTTP response
class ProductResponseSchema(BaseResponseSchema):
    data = fields.Nested(ProductSchema, many=True)


# Schema that represents Product HTTP Request.
# The inner class is used to deserialize requests into application level object
class ProductRequestSchema(Schema):
    class ProductRequest:
        min_price = 0
        max_price = sys.maxsize
        available = False
        page = 0
        limit = 25

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    min_price = fields.Float(missing=0, default=0, validate=validate.Range(min=0, max=constants.MAX_INT))
    max_price = fields.Float(missing=constants.MAX_INT, default=constants.MAX_INT, validate=validate.Range(min=0, max=constants.MAX_INT))
    limit = fields.Integer(missing=25, validate=validate.Range(min=1, max=100000))
    page = fields.Integer(missing=0, validate=validate.Range(min=0, max=1000))
    available = fields.Boolean(missing=False, default=False)

    @post_load()
    def make_request(self, data):
        return self.ProductRequest(**data)
