from main import create_app
from database.seed import *

# reset the db
def reset_db():

    # Creating app context
    print("Creating flask app context...")
    app, db = create_app()

    # Deleting up the databasae
    print("Deleting the database...")
    db.reflect()
    db.drop_all()

    # Creating all tables for the models
    print("Creating database models...")
    db.create_all()

    # Starting seed
    print("Seeding table with data started...")

    user.seed_users()
    product.seed_products()

if __name__ == '__main__':
    reset_db()
