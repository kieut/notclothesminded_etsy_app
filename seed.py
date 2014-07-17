# import model
import json, httplib2
import pprint
import urllib
from model import db_session
import model
import re
import HTMLParser

mykey = 'vgmfi5108akc4ot4rthtrw08'

listing_id_list = []

BUST_PATTERNS = [
    re.compile('.*bust[ \t:-]+\D*(?P<bust>[0-9]+)[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile('.*pit[ \t:-]+\D*(?P<bust>[0-9]+)[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile('.*chest[ \t:-]+\D*(?P<bust>[0-9]+)[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile('.*armpit[ \t:-]+\D*(?P<bust>[0-9]+)[ \t]*(in|inches|")', re.IGNORECASE)
]

WAIST_PATTERNS = [
    re.compile('.*waist[ \t:-]+\D*(?P<waist>[0-9]+)[ \t]*(in|inches|")', re.IGNORECASE)

]

HIP_PATTERNS = [
    re.compile('.*hips?[ \t:-]+\D*(?P<hips>free|full|sweep|open)', re.IGNORECASE),
    re.compile('.*hips?[ \t:-]+\D*(?P<hips>[0-9]+)[ \t]*(in|inches|")', re.IGNORECASE)
]

HIP_OPEN_VARIATIONS = ['full', 'Full', 'free', 'Free', 'Open', 'open', 'sweep', 'Sweep']


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

    for p in range(30, 130):
        parameters = urllib.urlencode({'api_key': mykey, 'limit': 100, 'offset': 0, 'category': 'Vintage/Clothing', 'min_price': p, 'max_price': p+1})
        url = '?'.join(['https://openapi.etsy.com/v2/listings/active', parameters])
        resp, content = httplib2.Http().request(url)
        # print p, json.loads(content)['count']
        result = json.loads(content)
    return result

# def get_images(result):
#     """There wasn't a need for creating a listing_id_list to loop through first,
#     already has access to the listing_id's through results"""
#     results = result['results'] # list of objects
#     length = len(results)

#     for i in range(length):
#         listing_id = results[i]['listing_id']
#         parameters = urllib.urlencode({'api_key': 'vgmfi5108akc4ot4rthtrw08', 'limit': 100, 'offset': 0, 'listing_id': i})
#         url = '?'.join(['https://openapi.etsy.com/v2/listings/%d/images' % listing_id, parameters])
#         resp, content = httplib2.Http().request(url)
#         images = json.loads(content)
#     return images # dict

def get_images(listing_id_list):
    """Need to only grab images for the items that have all measurements, pull from list"""
    # length = len(results)

    for listing_id in listing_id_list:
        parameters = urllib.urlencode({'api_key': 'vgmfi5108akc4ot4rthtrw08', 'limit': 100, 'offset': 0, 'listing_id': listing_id})
        url = '?'.join(['https://openapi.etsy.com/v2/listings/%d/images' % listing_id, parameters])
        resp, content = httplib2.Http().request(url)
        images = json.loads(content)
    # print images
    return images

def get_bust(result): 
    """parse description for measurements"""
    # PATTERN = re.compile('.*bust[ \t:-]+\D*(?P<bustsize>[0-9]+)\s*(in|inches|")', re.IGNORECASE)
    # PATTERN2 = re.compile('.*pit[ \t:-]+\D*(?P<pit>[0-9]+)\s*(in|inches|")', re.IGNORECASE)
    # PATTERN3 = re.compile('.*chest[ \t:-]+\D*(?P<chest>[0-9]+)\s*(in|inches|")', re.IGNORECASE)
    # matches = [m for m in PATTERN.finditer(result)] #for m in PATTERN..., matches.append(m)

    # print "\n*****listing description:"
    # print result
    # print "*******end of description*******"

    for pattern in BUST_PATTERNS:
        matches = [m.group('bust') for m in pattern.finditer(result)]
    # empty collections evaluate to false
        if not matches:
            continue
        if len(matches) > 1:
            print "*****Multiple matches found*****: ", matches
            continue
        print "******Got match! Bust:******", matches[0]
        return int(matches[0])

def get_waist(result):
    # print "\n*****listing description:"
    # print result
    # print "*******end of description*******"

    for pattern in WAIST_PATTERNS:
        matches = [m.group('waist') for m in pattern.finditer(result)]
    # empty collections evaluate to false
        if not matches:
            continue
        if len(matches) > 1:
            print "*****Multiple matches found*****: ", matches
            continue
        print "******Got match! Waist:******", matches[0]
        return int(matches[0])

def get_hips(result):
    """This is the next pattern, need to save all free/full/sweep as the same thing
    in database, like free. Need to only allow user to input one type, 'free'."""

    # print "\n*****listing description:"
    # print result
    # print "*******end of description*******"

    for pattern in HIP_PATTERNS:
        matches = [m.group('hips') for m in pattern.finditer(result)]
    # empty collections evaluate to false
        if not matches:
            continue
        if len(matches) > 1:
            print "*****Multiple matches found*****: ", matches
            continue
        print "******Got match! Hips:******", matches[0]
        for i in HIP_OPEN_VARIATIONS:
            if matches[0] == i: 
                matches[0] = 100
                print "******OPEN MATCH*******:%s" % matches[0]
        return matches[0]
 
def main(db_session):
    """Map objects to database from here so can move functions around"""
    listings_dict = get_listings(mykey)
    listings = listings_dict['results'] # this is a list of listing objects

#for every listing in results is an object with attributes
    for i in listings:
        description = i['description']
        item = HTMLParser.HTMLParser().unescape(description)
        # print "\n*****listing description:"
        # print item
        bust = get_bust(item)
        waist = get_waist(item)
        hips = get_hips(item)
        # print "*******end of description*******"

        if bust is not None and waist is not None and hips is not None:
            listing_id_list.append(i['listing_id'])
            print listing_id_list

            listing = model.Listing(title = i['title'], description = i['description'],
            listing_url = i['url'], price = float(i['price']),
            materials = ",".join(i['materials']), currency = i['currency_code'],
            bust = bust, waist = waist, hip = hips, creation_date = i['creation_tsz'],
            state = i['state'], last_modified = i['last_modified_tsz'])
            db_session.add(listing)


    images = get_images(listing_id_list) #dict
    # print "IMAGES*****%s" % images
    images_list = images['results'] # list
    print "*******image results list*****%s" % images_list

# will need to pass through list of listings that I'm keeping...
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