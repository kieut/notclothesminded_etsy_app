from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///notclothesminded.db", echo=False)
db_session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))
ENGINE = None
Session = None

Base = declarative_base()
Base.query = db_session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    first_name = Column(String(64), nullable = True)
    surname = Column(String(64), nullable = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)


class Listing(Base):
    __tablename__= "listings"

    id = Column(Integer, primary_key = True)
    title = Column(String(140), nullable = True)
    description = Column(Text, nullable = True) # LOOK AT THIS, string or text data type
    listing_url = Column(String(100), nullable = False)
    price = Column(String(64), nullable = False)
    materials = Column(String(100), nullable = True)
    # color is in the params key
    # color = Column(String(64), nullable = True)
    currency = Column(String(64), nullable = False)
    bust = Column(Integer, nullable = True)
    waist = Column(Integer, nullable = True)
    hip = Column(Integer, nullable = True)
    natural_waist = Column(Integer, nullable = True)
    dress_length = Column(Integer, nullable = True)
    skirt_length = Column(Integer, nullable = True)
    shirt_length = Column(Integer, nullable = True)
    arm_length = Column(Integer, nullable = True)
    creation_date = Column(Integer, nullable = True)
    state = Column(String(64), nullable = True)
    last_crawl = Column(Integer, nullable = True) # get epoch time from python, utc, save as int
    last_modified = Column(Integer, nullable = False) # already displayed in epoch time, just save as an int

class UserFavorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = True)
    #ForeignKey says it references another column in another table
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable = True)

    user = relationship("User", backref=backref("favorites", order_by=id))
    listing = relationship("Listing", backref=backref("favorites", order_by=id))

    
class ListingImage(Base):
    __tablename__= "images"

    id = Column(Integer, primary_key = True)
    listing_image_id = Column(Integer(64), nullable = False)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable = False)
    url_170x135 = Column(String(200), nullable = True)
    url_570xN = Column(String(200), nullable = True)
    url_75x75 = Column(String(200), nullable = True)
    url_fullxfull = Column(String(200), nullable = True)

    listing = relationship("Listing", backref=backref("listings", order_by=id))

# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///notclothesminded.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()

def main():
    """In case we need this for something"""

if __name__ == "__main__":
    main()