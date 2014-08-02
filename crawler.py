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
    parser = ListingParser(item)
    bust = parser.GetBust()
    waist = parser.GetWaist()
    hip = parser.GetHip()

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

    # If we weren't able to match the listing, print it out so we can see
    # descriptions that we failed to match.
    print "\n***** unmatched listing description:"
    print item.encode('ascii', errors='ignore')
    print "***** end of description"


def delete_expired():

    # How do you delete from a table using a join with SQLAlchemy?  This doesn't
    # work :(  You can't delete from a join, we can't figure out how to specify
    # to SQLAlchemy which table to delete from - we could do it with raw SQL,
    # but seems cleaner to do it the SQLAlchemy-friendly subquery way below.
    #model.db_session.query(model.ListingImage).join(
    #    model.ListingImage.listing).filter(
    #    model.Listing.ending_tsz < time.time()).delete(
    #    synchronize_session=False)
    #model.db_session.commit()

    listings_query = model.db_session.query(model.Listing.etsy_listing_id).filter(
        model.Listing.ending_tsz < time.time())
    images_query = model.db_session.query(model.ListingImage).filter(
        model.ListingImage.etsy_listing_id.in_(listings_query.subquery()))

    print >>sys.stderr, 'Deleting %d expired listings' % len(listings_query.all())
    images_query.delete(synchronize_session=False)
    listings_query.delete(synchronize_session=False)
    model.db_session.commit()


def get_last_crawl():
    # get crawlhistory by descending timestamp, latest time
    result = model.db_session.query(model.CrawlHistory).order_by(
        model.CrawlHistory.timestamp.desc()).first()
    return result.timestamp if result is not None else 0


def main(db_session):
    # Delete any expired listings right away before we do anything else.
    delete_expired()

    # Get the last crawl timestamp so we know how far back in time to check for
    # listings.
    prev_crawl_timestamp = get_last_crawl()

    # Set up some variables we need for doing the crawl.  We have to put our
    # counters in a list because it has to be a mutable type for the nested
    # function below to modify the value, and ints are not mutable.  List are
    # mutable, though, so we can use this trick to *change* the value of our
    # counters without having to *reassign* a new value to them.  In Python 3,
    # we could use the 'nonlocal' keyword to avoid having to do the list trick.
    total_results = [0]
    matched_results = [0]
    start_time = time.time()
    
    seen_ids = set()
    def HandleListing(etsy_listing):
        # Handle the end of a price bucket specially by identifying our bucket-
        # delimiter of None.  At the end of a price bucket, we commit the
        # listings that we found, and clear the seen_ids set so it doesn't get
        # too big - we don't have to check for duplicates across price buckets
        # because we're committing the session between buckets (the
        # session.merge() call handles the duplicates as long as they've been
        # committed).  This also makes the frontend show the most up-to-date
        # data while the crawler is running.
        if etsy_listing is None:
            print >>sys.stderr, 'Comitting Price bucket to DB: ', time.time()
            db_session.commit()
            seen_ids.clear()
            return

        # Otherwise we have a listing to handle, get to it!
        total_results[0] += 1

        try:
            result = convert_listing(etsy_listing, start_time)
        except Exception:
            # Augh random exceptions, eventually clean this up to catch explicit
            # errors we care about.
            print >>sys.stderr, 'Invalid listing: ', etsy_listing
            traceback.print_exc()
            return

        # If we were able to find the measurements we need, we'll get an
        # etsy_listing_id, a model.Listing, and a list of model.ImageListing's
        # associated with the listing.
        if result is not None:
            matched_results[0] += 1
            listing_id, listing, images = result
            if listing_id in seen_ids:
                print >>sys.stderr, 'Warning, duplicate listing id:', listing_id
            else:
                db_session.merge(listing)
                seen_ids.add(listing_id)

            for image in images:
                db_session.add(image)

    print >>sys.stderr, 'Getting listings: ', time.time()


    num_queries_made = get_listings(HandleListing, MIN_PRICE, MAX_PRICE)
    total_time = time.time() - start_time

    crawlhistory = model.CrawlHistory(
        timestamp=start_time,
        total_results=total_results[0],
        matched_results=matched_results[0],
        prev_timestamp=prev_crawl_timestamp,
        total_time=total_time,
        num_queries_made=num_queries_made,
        min_price=MIN_PRICE,
        max_price=MAX_PRICE,
        )

    db_session.add(crawlhistory)

    print >>sys.stderr, 'Comitting crawlhistory to DB: ', time.time()
    db_session.commit()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        MIN_PRICE = int(sys.argv[1])
        MAX_PRICE = int(sys.argv[2])
        
    s = model.db_session()
    main(s)
