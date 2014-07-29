import HTMLParser
import model
from etsy import get_listings
from parser import ListingParser
import time
import sys
import traceback

MIN_PRICE = 95
MAX_PRICE = 96

def convert_listing(etsy_listing, start_time):
    description = etsy_listing['description']
    item = HTMLParser.HTMLParser().unescape(description)
    print "\n*****listing description:"
    print item.encode('ascii', errors='ignore')
    parser = ListingParser(item)
    bust = parser.GetBust()
    waist = parser.GetWaist()
    hip = parser.GetHip()
    print "*******end of description*******"

    if etsy_listing['currency_code'] == 'USD' and bust is not None and waist is not None:
        listing = model.Listing(
            etsy_listing_id=etsy_listing['listing_id'],
            title=etsy_listing['title'],
            description=etsy_listing['description'],
            listing_url=etsy_listing['url'],
            price=float(etsy_listing['price']),
            # materials=",".join(etsy_listing['materials']),
            currency=etsy_listing['currency_code'],
            min_bust=bust[0], max_bust=bust[1],
            min_waist=waist[0], max_waist=waist[0],
            min_hip=hip[0] if hip else 0,
            max_hip=hip[1] if hip else 100,
            creation_date=etsy_listing['creation_tsz'],
            state=etsy_listing['state'],
            last_modified=etsy_listing['last_modified_tsz'],
            ending_tsz=etsy_listing['ending_tsz'],
            timestamp=start_time)

        images = []
        for image in etsy_listing['Images']:
            images.append(model.ListingImage(
                etsy_listing_id=etsy_listing['listing_id'],
                url_75x75=image['url_75x75'],
                url_fullxfull=image['url_fullxfull']))

        return etsy_listing['listing_id'], listing, images

# def convert_images(image):
#   # print "*******image results list*****%s" % images_list
#       return model.ListingImage(
#       etsy_image_id=image['listing_image_id'],
#       etsy_listing_id=image['listing_id'],
#         # url_170x135=image['url_170x135'],
#         # url_570xN=image['url_570xN'],
#         url_75x75=image['url_75x75'],
#         url_fullxfull=image['url_fullxfull'])

def main(db_session):
    total_results = [0]
    matched_results = [0]

# get crawlhistory by descending timestamp, latest time
    result = model.db_session.query(model.CrawlHistory).order_by(
        model.CrawlHistory.timestamp.desc()).first()

    if not result:
        prev_timestamp = 0
    else: 
        prev_timestamp = result.timestamp

    seen_ids = set()
    def HandleListing(etsy_listing, start_time):
        total_results[0] += 1
#        if total_results[0] % 1000 == 0:
#            print >>sys.stderr, '***%s total listings processed' % total_results

        try:
            result = convert_listing(etsy_listing, start_time)
        except Exception:
            print >>sys.stderr, 'Invalid listing: ', etsy_listing
            traceback.print_exc()
            return

        if result is not None:
            matched_results[0] += 1
            listing_id, listing, images = result
            if listing_id in seen_ids:
                print >>sys.stderr, 'Warning, duplicate listing id:', listing_id
            seen_ids.add(listing_id)
            db_session.merge(listing)


            for image in images:
                db_session.add(image)

# 1. remove expired listings
    # expired = model.db_session.query(model.Listing).order_by(
    #     model.Listing.ending_tsz)
# 


    print >>sys.stderr, 'Getting listings: ', time.time()

    start_time = time.time()

    num_queries_made = get_listings(HandleListing, MIN_PRICE, MAX_PRICE, start_time)
    total_time = time.time() - start_time

    crawlhistory = model.CrawlHistory(
        timestamp=start_time,
        total_results=total_results[0],
        matched_results=matched_results[0],
        prev_timestamp=prev_timestamp,
        total_time=total_time,
        num_queries_made=num_queries_made,
        min_price=MIN_PRICE,
        max_price=MAX_PRICE,
        )

    db_session.add(crawlhistory)

    print >>sys.stderr, 'Comitting to DB: ', time.time()
    db_session.commit()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        MIN_PRICE = int(sys.argv[1])
        MAX_PRICE = int(sys.argv[2])
        
    s = model.db_session()
    main(s)
