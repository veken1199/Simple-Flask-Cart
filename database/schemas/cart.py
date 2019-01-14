import sys
from datetime import date
from marshmallow import Schema, fields, pre_load, validate


class CartItemSchema(Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    current_inventory =fields.Integer(required=False)
    added_on = fields.Date(default=date.today())


class CartInfoSchema(Schema):
    cart = fields.Dict(keys=fields.Integer(), values=fields.Nested(CartItemSchema()))
    cart_total = fields.Float()
    cart_total_currency = fields.String()


# Schema that represents Cart HTTP response
class CartResponseSchema(Schema):
    message = fields.String()
    has_error = fields.Boolean()
    data = fields.Nested(CartInfoSchema)

cart_Item_Schema = CartItemSchema()
cart_response_Schema = CartResponseSchema()



