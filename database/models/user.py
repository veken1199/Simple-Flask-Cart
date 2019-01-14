from sqlalchemy import Column, Integer, String
from marshmallow import Schema, fields, pre_load, validate
from database import db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()

users_schema = UserSchema(many=True)
user_schema = UserSchema()