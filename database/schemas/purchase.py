import sys
from marshmallow import fields, pre_load, validate, ValidationError, Schema


class PurchaseRequestSchema(Schema):
    def validate_quantity(n):
        if n <= 0:
            raise ValidationError('Quantity must be greater than 0.')
        if n > sys.maxsize:
            raise ValidationError('Quantity is too big')

    product_id = fields.Integer(required=True)
    quantity = fields.Integer(validate=validate_quantity, required=True)


class PurchaseResponseSchema(Schema):
    message = fields.String()
    hasError = fields.Boolean()
    data = []

purchase_request_schema = PurchaseRequestSchema()