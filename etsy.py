
import json, httplib2
import urllib

mykey = 'vgmfi5108akc4ot4rthtrw08'

def get_listings(ListingHandler, min_price, max_price, start_time):

    def get_page(offset, price):
        parameters = urllib.urlencode({'api_key': mykey, 'limit': 100, 
        'offset': offset, 'category': 'Vintage/Clothing/Dress',
        'includes': 'Images(url_fullxfull,url_75x75)', 
        'min_price': price, 'max_price': price+.99})
        url = '?'.join(['https://openapi.etsy.com/v2/listings/active', parameters])
        resp, content = httplib2.Http().request(url)
        # print p, json.loads(content)['count']
        result = json.loads(content)
        for etsy_listing in result['results']:
            #initially, ListingHandler is passed through w/o parameters, so must provide one here: etsy_listing
            if etsy_listing['state'] == 'active':
                ListingHandler(etsy_listing, start_time)
        return result['count']

    num_queries_made = 0
    for price in range(min_price, max_price):
        #only returning the count
        count = get_page(0, price)
        num_queries_made += 1
        print "*******Price: %s, Count: %s" % (price, count)
        for offset in range(100, count, 100):
            num_queries_made += 1
            get_page(offset, price)
    return num_queries_made


    
# def get_images(listing_id):
#     parameters = urllib.urlencode({'api_key': 'vgmfi5108akc4ot4rthtrw08',
#                 'listing_id': listing_id, 'includes': 'MainImage(url_fullxfull)'})
#     url = '?'.join(['https://openapi.etsy.com/v2/listings/%d' % listing_id, parameters])
#     resp, content = httplib2.Http().request(url)
#     images = json.loads(content)
#     print images

# def get_images(listing_id):
#     parameters = urllib.urlencode({'api_key': 'vgmfi5108akc4ot4rthtrw08',
#             'limit': 100, 'offset': 0, 'listing_id': listing_id})
#     url = '?'.join(['https://openapi.etsy.com/v2/listings/%d/images' % listing_id, parameters])
#     resp, content = httplib2.Http().request(url)
#     images = json.loads(content)
#     return images
