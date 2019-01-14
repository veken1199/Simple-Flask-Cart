from .product import *
from .user import *


def start_seed(db):
    # Deleting up the databasae
    print("Deleting the database...")
    db.reflect()
    db.drop_all()

    # Creating all tables for the models
    print("Creating database models...")
    db.create_all()

    # Starting seed
    print("Seeding table with data started...")
    seed_users()
    product.seed_products()