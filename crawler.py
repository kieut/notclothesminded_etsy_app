from model import db_session
import HTMLParser
import model
from etsy import get_listings, get_images
from parser import ListingParser

def convert_listings(etsy_listing):
	description = etsy_listing['description']
	item = HTMLParser.HTMLParser().unescape(description)
	print "\n*****listing description:"
	print item
	parser = ListingParser(item)
	bust = parser.GetBust()
	waist = parser.GetWaist()
	hip = parser.GetHip()
	print "*******end of description*******"

	if (bust is not None and waist is not None and hip is not None):# or (bust is not None and waist is not None) or (bust is not None):

	    return etsy_listing['listing_id'], model.Listing(
	    	title=etsy_listing['title'],
	    	description=etsy_listing['description'],
	    	listing_url=etsy_listing['url'],
	    	price=float(etsy_listing['price']),
	    	materials=",".join(etsy_listing['materials']),
	    	currency=etsy_listing['currency_code'],
	    	bust=bust, waist=waist, hip=hip,
	    	creation_date=etsy_listing['creation_tsz'],
	    	state=etsy_listing['state'],
	    	last_modified=etsy_listing['last_modified_tsz'])

def convert_images(image):
	# print "*******image results list*****%s" % images_list
		return model.ListingImage(
    	listing_image_id=image['listing_image_id'],
    	listing_id=image['listing_id'],
        url_170x135=image['url_170x135'],
        url_570xN=image['url_570xN'],
        url_75x75=image['url_75x75'],
        url_fullxfull=image['url_fullxfull'])

def main(db_session):
    """Map objects to database from here so can move functions around"""
    listing_id_list = []
    listings_dict = get_listings()
    listings = listings_dict['results'] # this is a list of listing objects

#for every listing in results is an object with attributes
    for etsy_listing in listings:
    	result = convert_listings(etsy_listing)
    	if result is not None:
			listing_id, listing = result
			listing_id_list.append(listing_id)
			db_session.add(listing)


    images = get_images(listing_id_list)
    images_list = images['results']
    for image in images_list:
		db_session.add(convert_images(image))

    db_session.commit()

if __name__ == "__main__":
    s= model.db_session()
    main(s)