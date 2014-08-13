
import json, httplib2
import urllib
import sys
import time

with open("etsy_api_key") as f:
    mykey = f.read().strip()

def get_listings(ListingHandler, min_price, max_price, prev_crawl_time):

    def get_page(offset, price):
        parameters = urllib.urlencode({'api_key': mykey, 'limit': 100, 
        'offset': offset, 'category': 'Vintage/Clothing/Dress',
        'includes': 'Images(url_fullxfull,url_75x75)', 
        'min_price': price, 'max_price': price+.99, 'sorted_on': 'created'})
        url = '?'.join(['https://openapi.etsy.com/v2/listings/active', parameters])
        resp, content = httplib2.Http().request(url)
        # print p, json.loads(content)['count']
        result = json.loads(content)
        latest_created = time.time()
        for etsy_listing in result['results']:
            #initially, ListingHandler is passed through w/o parameters, so must provide one here: etsy_listing
            if etsy_listing['state'] == 'active':
                latest_created = int(etsy_listing['creation_tsz'])
                ListingHandler(etsy_listing)

        return result['count'], latest_created

    num_queries_made = 0
    total_results = 0
    for price in range(min_price, max_price):
        count, _ = get_page(0, price)
        total_results += count
        num_queries_made += 1
        print >>sys.stderr, "***** Price: %s, Count: %s" % (price, count)
        for offset in range(100, count, 100):
            num_queries_made += 1
            _, latest_created = get_page(offset, price)
            if latest_created < prev_crawl_time:
                print >>sys.stderr, "  *** Breaking price bucket early %s < %s" % (latest_created, prev_crawl_time)
                break

        # Call our handler with a sentinal value of None to indicate that we've
        # finished processing a price bucket.  See the comment in crawler.py
        # for more details on what this does.
        ListingHandler(None)
    return num_queries_made, total_results