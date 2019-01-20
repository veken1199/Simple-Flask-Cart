from ..models.product import Product
from database import db

def seed_products():
    product_1 = Product('Hamer Studio Sunburst 1995', 2322.26, 2)
    product_2 = Product('Gibson Les Paul Standard 2018', 3123.15, 3)
    product_3 = Product('Gibson Les Paul Standard 2018 Electric Guitar Mojave Burst', 4058.18, 0)
    product_4 = Product('Firebird V Tom Murphy', 2500.99)
    product_5 = Product('Godin Guitars 5th Avenue', 681.99)
    product_6 = Product('Gibson Les Paul Money Bass', 1049.99)
    product_7 = Product('Boulder Creek Left Handed EBR3-N4L 4 String', 999.99)

    db.session.add(product_1)
    db.session.add(product_2)
    db.session.add(product_3)
    db.session.add(product_4)
    db.session.add(product_5)
    db.session.add(product_6)
    db.session.add(product_7)

    db.session.commit()