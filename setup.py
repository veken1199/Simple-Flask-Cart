from main import create_app
from database.seed import *


# reset the db
def reset_db():
    # Creating app context
    print('Creating flask app context...')
    _, db = create_app()

    start_seed(db)

if __name__ == '__main__':
    reset_db()
