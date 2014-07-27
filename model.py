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

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    age = Column(Integer, nullable=False)
    zipcode = Column(String(15), nullable=False)


class Listing(Base):
    __tablename__= "listings"

    id = Column(Integer, primary_key=True)
    etsy_listing_id = Column(Integer(64), nullable=False)
    title = Column(String(140), nullable=False)
    description = Column(Text, nullable=False)
    listing_url = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    materials = Column(String(100), nullable=False)
    currency = Column(String(64), nullable=False)
    min_bust = Column(Float, nullable=False)
    max_bust = Column(Float, nullable=False)
    min_waist = Column(Float, nullable=False)
    max_waist = Column(Float, nullable=False)
    min_hip = Column(Float, nullable=False)
    max_hip = Column(Float, nullable=False)
    creation_date = Column(Integer, nullable=False)
    state = Column(String(64), nullable=False)
    # last_crawl = Column(Integer, nullable=False)
    last_modified = Column(Integer, nullable=False) 
    ending_tsz = Column(Integer, nullable=False)
 
class UserFavorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    #ForeignKey says it references another column in another table
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)

    user = relationship("User", backref=backref("favorites", order_by=id))
    listing = relationship("Listing", backref=backref("favorites", order_by=id))

    
class ListingImage(Base):
    __tablename__= "images"

    id = Column(Integer, primary_key=True)
#    etsy_image_id = Column(Integer, nullable=False)
    etsy_listing_id = Column(Integer, ForeignKey("listings.etsy_listing_id"), nullable=True)
    # url_170x135 = Column(String(200), nullable=True)
    # url_570xN = Column(String(200), nullable=True)
    url_75x75 = Column(String(200), nullable=True)
    url_fullxfull = Column(String(200), nullable=True)

    listing = relationship("Listing", backref=backref("images", order_by=id))

class CrawlHistory(Base):
    __tablename__="crawlhistory"

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer, ForeignKey("listings.id"), nullable=False)
    total_results = Column(Integer, nullable=False)
    matched_results = Column(Integer, nullable=False)
    prev_timestamp = Column(Integer, nullable=False)
    total_time = Column(Integer, nullable=False)
    num_queries_made = Column(Integer, nullable=False)
    min_price = Column(Integer, nullable=False)
    max_price = Column(Integer, nullable=False)

    listing = relationship("Listing", backref=backref("crawlhistory", order_by=id))

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