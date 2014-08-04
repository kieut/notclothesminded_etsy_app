
import json, httplib2
import urllib
import sys

with open("etsy_api_key") as f:
    mykey = f.read().strip()

def get_listings(ListingHandler, min_price, max_price):

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
                ListingHandler(etsy_listing)

        return result['count']

    num_queries_made = 0
    for price in range(min_price, max_price):
        count = get_page(0, price)
        num_queries_made += 1
        print >>sys.stderr, "***** Price: %s, Count: %s" % (price, count)
        for offset in range(100, count, 100):
            num_queries_made += 1
            get_page(offset, price)
        # Call our handler with a sentinal value of None to indicate that we've
        # finished processing a price bucket.  See the comment in crawler.py
        # for more details on what this does.
        ListingHandler(None)
    return num_queries_made