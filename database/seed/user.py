from ..models.user import User
from database import db


def seed_users():
    user_1 = User("user@email.com", "user user")
    user_2 = User("user2@email.com", "user2 user2")

    db.session.add(user_1)
    db.session.add(user_2)

    db.session.commit()