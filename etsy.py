
import json, httplib2
import urllib

mykey = 'vgmfi5108akc4ot4rthtrw08'

def get_listings(ListingHandler):
    """This only gets me the count for each 'price bucket', only gives me 100 items per query.
    Still need to query for items for 100-150, 150-200, and >200, and tab through paginations"""
    def get_page(offset, price):
        parameters = urllib.urlencode({'api_key': mykey, 'limit': 100, 
        'offset': offset, 'category': 'Vintage/Clothing/Dress', 
        'min_price': price, 'max_price': price+1})
        url = '?'.join(['https://openapi.etsy.com/v2/listings/active', parameters])
        resp, content = httplib2.Http().request(url)
        # print p, json.loads(content)['count']
        result = json.loads(content)
        for etsy_listing in result['results']:
            #initially, ListingHandler is passed through w/o parameters, so must provide one here: etsy_listing
            ListingHandler(etsy_listing)
        return result['count']

    for price in range(200, 201):
        #only returning the count
        count = get_page(0, price)
        print "*******Price: %s, Count: %s" % (price, count)
        for offset in range(100, count, 100):
            get_page(offset, price)
    
def get_images(listing_id):
    parameters = urllib.urlencode({'api_key': 'vgmfi5108akc4ot4rthtrw08',
                'listing_id': listing_id, 'includes': 'MainImage(url_fullxfull)'})
    url = '?'.join(['https://openapi.etsy.com/v2/listings/%d' % listing_id, parameters])
    resp, content = httplib2.Http().request(url)
    images = json.loads(content)
    print images

# def get_images(listing_id):
#     parameters = urllib.urlencode({'api_key': 'vgmfi5108akc4ot4rthtrw08',
#             'limit': 100, 'offset': 0, 'listing_id': listing_id})
#     url = '?'.join(['https://openapi.etsy.com/v2/listings/%d/images' % listing_id, parameters])
#     resp, content = httplib2.Http().request(url)
#     images = json.loads(content)
    # return images