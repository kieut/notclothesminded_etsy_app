from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///notclothesminded.db", echo=False)
db_session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

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

    # ratings = relationship("Ratings")

class Listing(Base):
    __tablename__= "listings"

    id = Column(Integer, primary_key = True)
    title = Column(String(64), nullable = True)
    description = Column(Text(???), nullable = True) # LOOK AT THIS
    listing_url = Column(String(100), nullable = False)
    price = Column(Float, nullable = False)
    shop_section_id = Column(Integer, nullable = True) # shop id can return null?
    materials = Column(String(100), nullable = True)
    color = Column(String(64), nullable = True)
    currency = Column(String(64), nullable = False)
    bust = Column(Integer, nullable = True)
    waist = Column(Integer, nullable = True)
    hip = Column(Integer, nullable = True)
    natural_waist = Column(Integer, nullable = True)
    length = Column(Integer, nullable = True)
    arm_length = Column(Integer, nullable = True)

    """look up datetime and epoch time"""
    last_crawl = Column(DateTime, nullable = True)
    last_modified = Column(Epoch) # look up datatype for epoch



    # ratings = relationship("Ratings")

class UserFavorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = True)
    #ForeignKey says it references another column in another table
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable = True)

    #This establish relationship between Rating and User objects with 'backref'
    user = relationship("User", backref=backref("favorites", order_by=id))
    listing = relationship("Listing", backref=backref("favorites", order_by=id))

# ## End class declarations
# def connect():
#     global ENGINE 
#     global Session

#     ENGINE = create_engine("sqlite:///ratings.db", echo=False)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()

def main():
    """In case we need this for something"""

if __name__ == "__main__":
    main()