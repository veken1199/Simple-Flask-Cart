from .base import BaseTestCase
from database.models.product import Product
from database.schemas.product import ProductSchema


class ProductApiTest(BaseTestCase):
    def test_get_specific_product(self):
        response = self.client.get('/product/1')

        expected_products = Product.query.get(1)
        expected_products = ProductSchema().dump(expected_products).data
        self.assert_status(response, 200)
        self.assertEqual(expected_products, response.json['data'][0])

    def test_404_product_not_found(self):
        response = self.client.get('/product/10000')

        self.assert_status(response, 200)
        self.assertEqual(response.json['data'], [])
        self.assertEqual("Product not found", response.json['message'])
        self.assertEqual(False, response.json['has_error'])

    def test_404_invalid_product_id(self):
        response = self.client.get('/product/-1')
        self.assert_status(response, 404)

    def test_get_all_products(self):
        response = self.client.get('/product/all')

        expected_products = Product.query.all()
        expected_products, er = ProductSchema(many=True).dump(expected_products)
        self.assert_status(response, 200)

        self.assertEqual(expected_products, response.json['data'])
        self.assertEqual("Successful request", response.json['message'])
        self.assertEqual(False, response.json['has_error'])

    def test_get_all_products_with_available_filter(self):
        response = self.client.get('/product/all?available=true')

        expected_products = Product.query.filter(Product.inventory_count > 0).all()
        expected_products = ProductSchema(many=True).dump(expected_products).data

        self.assert_status(response, 200)
        self.assertEqual(expected_products, response.json['data'])
        self.assertEqual("Successful request", response.json['message'])
        self.assertEqual(False, response.json['has_error'])

    def test_get_all_products_with_limit_filter(self):
        response = self.client.get('/product/all?available=true&limit=1')

        self.assert_status(response, 200)
        self.assertEqual(1, len(response.json['data']))
        self.assertEqual("Successful request", response.json['message'])
        self.assertEqual(False, response.json['has_error'])

    def test_get_all_products_with_min_max_price_filter(self):
        response = self.client.get('/product/all?available=true&limit=2&min_price=2000&max_price=3000')

        expected_products = Product.query.filter(Product.price >= 2000)\
            .filter(Product.price <= 3000)\
            .filter(Product.inventory_count > 0)\
            .all()

        expected_products = ProductSchema(many=True).dump(expected_products).data

        self.assert_status(response, 200)
        self.assertEqual(expected_products, response.json['data'])
        self.assertEqual("Successful request", response.json['message'])
        self.assertEqual(False, response.json['has_error'])

    def test_get_all_products_with_invalid_args(self):
        response = self.client.get('/product/all?available=nottrue')
        self.assert_status(response, 422)
        self.assertEqual({'available': ['Not a valid boolean.']}, response.json['message'])
        self.assertEqual(True, response.json['has_error'])

        response = self.client.get('/product/all?available=loll')
        self.assert_status(response, 422)
        self.assertEqual({'available': ['Not a valid boolean.']}, response.json['message'])

        response = self.client.get('/product/all?available=true&limit=-1')
        self.assert_status(response, 422)
        self.assertEqual({'limit': ['Must be between 1 and 100000.']}, response.json['message'])

        response = self.client.get('/product/all?available=true&min_price=-23')
        self.assert_status(response, 422)
        self.assertEqual({'min_price': ['Must be between 0 and 2147483647.']}, response.json['message'])

    def test_visit_counts(self):
        num_visits = 4

        response = self.client.get('/product/1')
        initial_visits_count = response.json['data'][0]['visits']

        # Lets visit this products 3 times + 1 visit from initial request
        self.client.get('/product/1')
        self.client.get('/product/1')
        self.client.get('/product/1')

        response = self.client.get('/product/1')
        current_visits_count = response.json['data'][0]['visits']
        self.assertEqual(initial_visits_count + num_visits, current_visits_count)
