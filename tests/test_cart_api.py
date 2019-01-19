from .base import BaseTestCase
from database.models.product import Product
from decimal import Decimal
import sys


class CartApiTest(BaseTestCase):
    def test_get_cart_content(self):
        response = self.client.get('/cart')
        self.assert_status(response, 200)

    def test_add_to_cart_content(self):
        product_to_add = Product.query.get(1)
        quantity_to_add = 2
        response = self.post('/cart', dict(product_id=product_to_add.id, quantity=quantity_to_add))

        self.assert_status(response, 200)
        self.assertEqual('Item has been added to the cart', response.json['message'])
        self.assertEqual(False, response.json['has_error'])

        response = self.client.get('/cart')
        actual_cart_data = response.json['data']

        self.assert_status(response, 200)
        self.assertAlmostEqual(Decimal(product_to_add.price * 2), Decimal(actual_cart_data['cart_total']), 2)
        self.assertEqual(quantity_to_add, actual_cart_data['cart'][str(product_to_add.id)]['quantity'])

    def test_remove_cart_content(self):
        product_to_add = Product.query.get(1)
        quantity_to_add = 2

        # add the product to the cart
        self.post('/cart', dict(product_id=product_to_add.id, quantity=quantity_to_add))

        # remove the product from the cart
        response = self.client.delete('/cart', data=dict(product_id=product_to_add.id, quantity=quantity_to_add))
        self.assertEqual('Successfully deleted from the cart', response.json['message'])
        self.assertEqual({}, response.json['data']['cart'])

    def test_cart_checkout(self):
        product_to_add = Product.query.get(1)
        quantity_to_add = 2

        # add the product to the cart
        self.post('/cart', dict(product_id=product_to_add.id, quantity=quantity_to_add))

        # purchase the entire cart
        response = self.post('/cart/checkout', dict(data=''))
        self.assertEqual('Successfully purchased the products with the following ids :{}'.format([product_to_add.id]),
                         response.json['message'])

    def test_invalid_requests(self):
        # posting invalid ids and quantities
        response = self.post('/cart', dict(product_id=-1, quantity=sys.maxsize + 1))
        self.assertEqual({'product_id': ['Must be between 1 and 2147483647.'],
                          'quantity': ['Must be between 1 and 2147483647.']}, response.json['message'])
        self.assertEqual(True, response.json['has_error'])

        response = self.client.delete('/cart', data=dict(product_id=-1, quantity=sys.maxsize))
        self.assertEqual({'product_id': ['Must be between 1 and 2147483647.']}, response.json['message'])
        self.assertEqual(True, response.json['has_error'])


    def test_incomplete_cart_purchase(self):
        product_to_add = Product.query.get(1)
        quantity_to_add = 2

        product_to_add_2 = Product.query.get(2)
        quantity_to_add_2 = 1

        # add the products to the cart
        self.post('/cart', dict(product_id=product_to_add.id, quantity=quantity_to_add))
        self.post('/cart', dict(product_id=product_to_add_2.id, quantity=quantity_to_add_2))

        # someone else will purchase all products with id = 1
        self.post('/purchase', dict(product_id=product_to_add.id, quantity=quantity_to_add))

        # purchase the entire cart
        # validate that we purchased product_to_add_2
        response = self.post('/cart/checkout', dict(data=''))
        self.assertEqual('Successfully purchased the products with the following ids :{}'.format([product_to_add_2.id]),
                         response.json['message'])

        # validate that only product_to_add is kept in the cart
        response = self.client.get('/cart')
        self.assertEqual(1, len(response.json['data']['cart']))
        self.assertTrue(str(product_to_add.id) in response.json['data']['cart'].keys())




