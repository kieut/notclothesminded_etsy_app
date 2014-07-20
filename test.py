
import json, httplib2
import urllib
import pprint
import re
import HTMLParser

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


def get_listings():
    #test listing https://openapi.etsy.com/v2/listings/195051502?api_key=vgmfi5108akc4ot4rthtrw08
    resp, content =httplib2.Http().request("https://openapi.etsy.com/v2/listings/active?api_key=vgmfi5108akc4ot4rthtrw08&limit=50&offset=25&category=Vintage/Clothing/Dress")
    result=json.loads(content)
    return result

listing = """Measurements taken while dress laid flat (please double bust, waist, and hips)
    Bust 16 inches
    Waist just under 12 inches
    Hips full
    Length 44 inches"""

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

def load_images(result):
    """Can I just track the listing_id from load_listings() and pass it as a list to load_images?"""
    #to get listingimage objects
    # listing_id_list = []
    results = result['results']
    length = len(result['results'])

    for i in range(length):
        listing_id = results[i]['listing_id']
        parameters = urllib.urlencode({'api_key': 'vgmfi5108akc4ot4rthtrw08', 'limit': 100, 'offset': 0, 'listing_id': i})
        url = '?'.join(['https://openapi.etsy.com/v2/listings/%d/images' % listing_id, parameters])
        resp, content = httplib2.Http().request(url)
        result = json.loads(content)
    return result

def main():
    """Map objects to database from here so can move functions around"""
    result = get_listings()
    results = result['results']

    for i in results:
        description = i['description']
        # print description
        item = HTMLParser.HTMLParser().unescape(description)
        # print "ITEM_____________________!!!!!!%s" % item
        print "\n*****listing description:"
        print item
        bust = get_bust(item)
        waist = get_waist(item)
        hips = get_hips(item)
        print "*******end of description*******"
        print bust, waist, hips 

    # description = results[0]['description']
    # item = HTMLParser.HTMLParser().unescape(description)
    # print item

    # get_bust(item)


if __name__ == "__main__":
    main()