import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database import db

Base = db.Model

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    quantity_available = Column(Integer, nullable=False)
    image_url = Column(String(255), nullable=False)

    # one-to-many relationship with SalesItem
    # an Item can have multiple SalesItems associated with it
    sales_items = relationship('SalesItem', back_populates='item')

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', price={self.price}, quantity_available={self.quantity_available})>"

class SalesItem(Base):
    __tablename__ = 'sales_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    sale_percentage = Column(Float, nullable=False)

    item = relationship('Item', back_populates='sales_items')

    def __repr__(self):
        return f"<SalesItem(id={self.id}, item_id={self.item_id}, sale_percentage={self.sale_percentage})>"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # one-to-many relationship between User and Order models
    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.utcnow)

    # one-to-many relationship between Order and User models
    user = relationship('User', back_populates='orders')

    # one-to-many relationship between Order and OrderItem models
    items = relationship('OrderItem', back_populates='order')

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total_amount={self.total_amount}, order_date={self.order_date})>"

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship('Order', back_populates='items')
    item = relationship('Item')

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, item_id={self.item_id}, quantity={self.quantity})>"

class DiscountCode(Base):
    __tablename__ = 'discount_codes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False)
    percentage = Column(Float, nullable=False)

    def __repr__(self):
        return f"<DiscountCode(id={self.id}, code='{self.code}', percentage={self.percentage})>"
    
engine = create_engine('mysql+mysqlconnector://root:password@host/retro_shop')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Database Queries
def get_all_items():
    return session.query(Item).all()

def get_all_discount_codes():
    return session.query(DiscountCode).all()

def get_all_sales_items():
    return session.query(SalesItem).all()

def get_all_users():
    return session.query(User).all()

def get_all_orders():
    return session.query(Order).all()

def get_order_history(sort_by='order_date'):
    # for retrieving order history from the database with sorting options
    if sort_by == 'order_date':
        return session.query(Order).order_by(Order.order_date).all()
    elif sort_by == 'total_amount':
        return session.query(Order).order_by(Order.total_amount).all()
    else:
        return session.query(Order).all()