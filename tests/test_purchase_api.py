import sys
from tests.base import BaseTestCase


class PurchaseApiTest(BaseTestCase):
    def test_purchase_api_validations(self):

        response = self.post('/purchase', dict())

        self.assert_status(response, 422)
        self.assertEqual({'product_id': ['Missing data for required field.'],
                        'quantity': ['Missing data for required field.']}, response.json['message'])

        response = self.post('/purchase', dict(product_id=1))
        self.assert_status(response, 422)
        self.assertEqual({'quantity': ['Missing data for required field.']}, response.json['message'])

        response = self.post('/purchase', dict(quantity=1))
        self.assert_status(response, 422)
        self.assertEqual({'product_id': ['Missing data for required field.']}, response.json['message'])

        # inserting invalid data:
        response = self.post('/purchase', dict(product_id=sys.maxsize+1, quantity=-1))
        self.assert_status(response, 422)
        self.assertEqual({'product_id': ["Must be between 1 and 2147483647."],
                        'quantity': ["Must be between 1 and 2147483647."]}, response.json['message'])

    def test_purchasing_product(self):
        # get the initial inventory count of product id =1
        product_id = 2
        requested_quantity = 2

        response = self.client.get('/product/2')
        initial_inventory_count = response.json['data'][0]['inventory_count']

        # purchase 2 products of id = 1
        response = self.post('/purchase', dict(product_id=product_id, quantity=requested_quantity))
        self.assert200(response)
        self.assertEqual('Purchase has been completed!', response.json['message'])

        # check the inventory count has been reduced
        response = self.client.get('/product/2')
        atfer_purchase_inventory_count = response.json['data'][0]['inventory_count']
        self.assertEqual(initial_inventory_count - requested_quantity, atfer_purchase_inventory_count)