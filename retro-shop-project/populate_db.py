from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base, Item, DiscountCode, SalesItem, User, Order

# Example connection URL for MySQL: 'mysql+mysqlconnector://username:password@host/database'
engine = create_engine('mysql+mysqlconnector://root:pass@host/retro_shop')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_items():
    item1 = Item(name='Super Mario Bros', price=29.99, quantity_available=10)
    item2 = Item(name='The Legend of Zelda', price=39.99, quantity_available=5)
    item3 = Item(name='Mega Man 2', price=24.99, quantity_available=3)

    session.add_all([item1, item2, item3])
    session.commit()

def create_discount_codes():
    discount_code1 = DiscountCode(code='SUMMER2023', percentage=15)
    discount_code2 = DiscountCode(code='RETROGAMER', percentage=10)

    session.add_all([discount_code1, discount_code2])
    session.commit()

def create_sales_items():
    sales_item1 = SalesItem(item_id=1, sale_percentage=20)
    sales_item2 = SalesItem(item_id=3, sale_percentage=30)

    session.add_all([sales_item1, sales_item2])
    session.commit()

if __name__ == '__main__':
    create_items()
    create_discount_codes()
    create_sales_items()
