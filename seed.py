# import model
import json, httplib2
import pprint
import urllib
from model import db_session
import model

mykey = 'vgmfi5108akc4ot4rthtrw08'


# pass 'offset' variable to this from main function, figure out where it's left off every time you run function.
def get_listings(mykey):
	#HTTP GET request for active listings, filter by category string path "Vintage/Clothing"
	#Need to loop through paginations.
	#everything after '?'' is a parameter
	#urllib creates the url with parameters for me

	"""Need a new url for each time through this loop, so need to do the urlencode inside the loop (and the join)"""
	"""This only gets me the count for each 'price bucket', only gives me 100 items per query.
	Still need to query for items for 100-150, 150-200, and >200, and tab through paginations"""
	# need to put this is another for loop, to set offset to i+100
	p = 0

	for p in range(100, 101):
		parameters = urllib.urlencode({'api_key': mykey, 'limit': 100, 'offset': 0, 'category': 'Vintage/Clothing', 'min_price': p, 'max_price': p+1})
		url = '?'.join(['https://openapi.etsy.com/v2/listings/active', parameters])
		resp, content = httplib2.Http().request(url)
		# print p, json.loads(content)['count']
		result = json.loads(content)
	return result # dict of all objects

def get_images(result):
	"""There wasn't a need for creating a listing_id_list to loop through first,
	already has access to the listing_id's through results"""
	results = result['results'] # list of objects
	length = len(results)

	for i in range(length):
		listing_id = results[i]['listing_id']
		parameters = urllib.urlencode({'api_key': 'vgmfi5108akc4ot4rthtrw08', 'limit': 100, 'offset': 0, 'listing_id': i})
		url = '?'.join(['https://openapi.etsy.com/v2/listings/%d/images' % listing_id, parameters])
		resp, content = httplib2.Http().request(url)
		images = json.loads(content)
	return images # dict

def get_bust(result): 
	"""parse description for measurements"""
	#.*Bust\s*[ :-]?\D*([0-9]+)
	pass

def get_waist(result):
	pass

def get_hip(result):
	pass

def get_natural_waist(result):
	pass

def get_dress_length(result):
	pass

"""How will I know if it's a skirt, I think I need to build out my
data model and possibly split listings into diff types of clothing"""
def get_skirt_length(result):
	pass

def get_shirt_length(result):
	pass

def get_arm_length(result):
	pass

 
def main(db_session):
	"""Map objects to database from here so can move functions around"""
	result = get_listings(mykey)
	results = result['results'] # this is a list

#for every listing in results is an object with attributes
	for i in results:
		# pprint.pprint(listing)

		listing = model.Listing(title = i['title'], description = i['description'],
			listing_url = i['url'], price = str(i['price']),
			materials = ",".join(i['materials']), currency = i['currency_code'], creation_date = i['creation_tsz'], state = i['state'],
			last_modified = i['last_modified_tsz'])
		db_session.add(listing)


	images = get_images(result) #dict??
	images_list = images['results'] # list

	for i in images_list:
		# pprint.pprint(image)
		image = model.ListingImage(listing_image_id = i['listing_image_id'], listing_id = i['listing_id'],
			url_170x135 = i['url_170x135'], url_570xN = i['url_570xN'], url_75x75 = i['url_75x75'],
			url_fullxfull = i['url_fullxfull'])
		db_session.add(image)

	db_session.commit()

if __name__ == "__main__":
    s= model.db_session()
    main(s)