from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base, Item, User

# Example connection URL for MySQL: 'mysql+mysqlconnector://username:Thelegendofzelda1!@127.0.0.1/database'
engine = create_engine('mysql+mysqlconnector://root:Thelegendofzelda1!@127.0.0.1/retro_shop')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_items():
    item1 = Item(name='Super Mario Bros', price=29.99, quantity_available=10, image_url='https://coverproject.sfo2.cdn.digitaloceanspaces.com/nes/nes_supermariobros_thumb.jpg')
    item2 = Item(name='The Legend of Zelda', price=39.99, quantity_available=5, image_url='https://coverproject.sfo2.cdn.digitaloceanspaces.com/nes/nes_legendofzelda_thumb.jpg')
    item3 = Item(name='Mega Man 2', price=24.99, quantity_available=3, image_url='https://coverproject.sfo2.cdn.digitaloceanspaces.com/nes/nes_megaman2_thumb.jpg')

    session.add_all([item1, item2, item3])
    session.commit()

    user1 = User(id=1, username="ptg426", password="password")
    user2 = User(id=2, username="admin", password="password")
    
    session.add_all([user1, user2])
    session.commit()

def initialize_database():
    create_items()

if __name__ == '__main__':
    initialize_database()
