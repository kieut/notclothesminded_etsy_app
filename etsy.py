
import json, httplib2
import urllib

mykey = 'vgmfi5108akc4ot4rthtrw08'

def get_listings():
    #HTTP GET request for active listings, filter by category string path "Vintage/Clothing"
    #Need to loop through paginations.
    #everything after '?'' is a parameter
    #urllib creates the url with parameters for me

    """Need a new url for each time through this loop, so need to do the urlencode inside the loop (and the join)"""
    """This only gets me the count for each 'price bucket', only gives me 100 items per query.
    Still need to query for items for 100-150, 150-200, and >200, and tab through paginations"""
    p = 0

    for p in range(100, 120):
        parameters = urllib.urlencode({'api_key': mykey, 'limit': 100, 'offset': 0, 'category': 'Vintage/Clothing', 'min_price': p, 'max_price': p+1})
        url = '?'.join(['https://openapi.etsy.com/v2/listings/active', parameters])
        resp, content = httplib2.Http().request(url)
        # print p, json.loads(content)['count']
        result = json.loads(content)
    return result

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