import HTMLParser
import model
from etsy import get_listings, get_images
from parser import ListingParser
import time
import sys
import traceback

def convert_listings(etsy_listing):
	description = etsy_listing['description']
	item = HTMLParser.HTMLParser().unescape(description)
	print "\n*****listing description:"
	print item.encode('ascii', errors='ignore')
	parser = ListingParser(item)
	bust = parser.GetBust()
	waist = parser.GetWaist()
	hip = parser.GetHip()
	print "*******end of description*******"

	if bust is not None and waist is not None:

	    return etsy_listing['listing_id'], model.Listing(
	    	listing_id=etsy_listing['listing_id'],
	    	title=etsy_listing['title'],
	    	description=etsy_listing['description'],
	    	listing_url=etsy_listing['url'],
	    	price=float(etsy_listing['price']),
	    	materials=",".join(etsy_listing['materials']),
	    	currency=etsy_listing['currency_code'],
	    	min_bust=bust[0], max_bust=bust[1],
	    	min_waist=waist[0], max_waist=waist[0],
	    	min_hip=hip[0] if hip else 0,
	    	max_hip=hip[1] if hip else 100,
	    	creation_date=etsy_listing['creation_tsz'],
	    	state=etsy_listing['state'],
	    	last_modified=etsy_listing['last_modified_tsz'],
	    	last_crawl=time.time())

def convert_images(image):
	# print "*******image results list*****%s" % images_list
		return model.ListingImage(
    	listing_image_id=image['listing_image_id'],
    	# listing_id=image['listing_id'],
        url_170x135=image['url_170x135'],
        url_570xN=image['url_570xN'],
        url_75x75=image['url_75x75'],
        url_fullxfull=image['url_fullxfull'])

def main(db_session):
    listing_id_list = []
    def HandleListing(etsy_listing):
    	try:
    		result = convert_listings(etsy_listing)
    	except Exception:
    		print >>sys.stderr, 'Invalid listing: ', etsy_listing
    		traceback.print_exc()
    		return

    	if result is not None:
    		listing_id, listing = result
    		listing_id_list.append(listing_id)
    		db_session.add(listing)

    print >>sys.stderr, 'Getting listings: ', time.time()
    get_listings(HandleListing)

#Not getting images right now until figure out how to retrieve a batch
    if True:
        print >>sys.stderr, 'Getting images: ', time.time()
        for listing_id in listing_id_list:
   		    images = get_images(listing_id)
   	 	    images_list = images['results']
   		    for image in images_list:
			    db_session.add(convert_images(image))

    print >>sys.stderr, 'Comitting to DB: ', time.time()
    db_session.commit()

if __name__ == "__main__":
    s = model.db_session()
    main(s)