import sys
import constants
from database.schemas.base_response import BaseResponseSchema
from marshmallow import fields, validate, post_load, Schema, pre_load


# Schema used to represent user purchase requests
# It is also used to deserialize requests to application object
class PurchaseRequestSchema(Schema):
    class PurchaseRequest:
        product_id = 0
        quantity = 0

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    product_id = fields.Integer(strict=True, required=True, validate=validate.Range(min=1, max=constants.MAX_INT))
    quantity = fields.Integer(strict=True, required=True, validate=validate.Range(min=1, max=constants.MAX_INT))

    @post_load()
    def create_purchase_request(self, data):
        # currently there is a bug in @use_kwargs and object deserialization using Schema.load()
        # See https://github.com/jmcarp/flask-apispec/issues/73
        # return self.PurchaseRequest(**data)
        return data


class DeletePurchaseRequestSchema(Schema):
    class DeletePurchaseRequest:
        product_id = 0
    product_id = fields.Integer(strict=True, required=True, validate=validate.Range(min=1, max=constants.MAX_INT))


class PurchaseResponseSchema(BaseResponseSchema):
    data = []

