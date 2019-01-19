from sqlalchemy import Column, Integer, String, Enum
from .currency import CurrencyEnum
from database import db


class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True) # for simplicity we will keep simple int instead of UUID
    title = Column(String(50), unique=False, nullable=False)  # Assumption: Different products can have same title
    price = Column(db.Float(10,2), unique=False, nullable=False)
    currency_unit = Column(Enum(CurrencyEnum.USD.value, CurrencyEnum.CAD.value), name='currency_types')
    inventory_count = Column(Integer, default=0,  nullable=False)
    visits = Column(Integer, default=0,  nullable=False)

    def __init__(self, title=None, price=None, inventory_count=None, visits=None, currency_unit=CurrencyEnum.CAD.value):
        self.title = title
        self.price = price
        self.inventory_count = inventory_count
        self.visits = visits
        self.currency_unit = currency_unit

    def increment_visit(self):
        self.visits += 1


