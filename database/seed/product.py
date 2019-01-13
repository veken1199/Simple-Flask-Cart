from ..models.product import Product
from database import db

def seed_products():
    product_1 = Product("Hamer Studio Sunburst 1995", 2322.26, 2)
    product_2 = Product("Gibson Les Paul Standard 2018", 3123.15, 3)
    product_3 = Product("Gibson Les Paul Standard 2018 Electric Guitar Mojave Burst", 4058.18, 0)

    db.session.add(product_1)
    db.session.add(product_2)
    db.session.add(product_3)

    db.session.commit()