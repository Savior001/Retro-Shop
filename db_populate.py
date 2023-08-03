from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base, Item

# Example connection URL for MySQL: 'mysql+mysqlconnector://username:password@host/database'
engine = create_engine('mysql+mysqlconnector://root:password@host/retro_shop')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_items():
    item1 = Item(name='Super Mario Bros', price=29.99, quantity_available=10, image_url='https://coverproject.sfo2.cdn.digitaloceanspaces.com/nes/nes_supermariobros_thumb.jpg')
    item2 = Item(name='The Legend of Zelda', price=39.99, quantity_available=5, image_url='https://coverproject.sfo2.cdn.digitaloceanspaces.com/nes/nes_legendofzelda_thumb.jpg')
    item3 = Item(name='Mega Man 2', price=24.99, quantity_available=3, image_url='https://coverproject.sfo2.cdn.digitaloceanspaces.com/nes/nes_megaman2_thumb.jpg')

    session.add_all([item1, item2, item3])
    session.commit()

def initialize_database():
    create_items()

if __name__ == '__main__':
    initialize_database()
