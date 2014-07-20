import re

listing1 = """
    Bust (underarm to underarm measured flat, then doubled) to about 34" with the curve of the bust
    Waist 25", tight 26"
    Hips full/free
    Bodice, underarm to waist seam 8 1/2"
    Length of skirt, waist to hem 34" """

listing2 = """chest: 33 in
waist: 24 in
hip: free sweep
length: 38 in
"""

listing3 = """Pit to Pit:   17" 
Waist: 31
Hips: 36
Length: 42
Clipped on the model: No
Shown on a size 6 form"""


def get_bust(result): 
    """parse description for measurements"""
    # PATTERN = re.compile('.*bust\s*[ :-]?\D*([0-9]+)\s*(in|inches|")', re.IGNORECASE)
    # m = PATTERN.finditer(result)
    # if m:
    #     print('Match found: ', m)
    #     if len(m) > 1:
    #         print "More than 1 match"
    #         #maybe toss record from db, not in scope of project
    # else:
    #     print('No match')

    #re.compile turns a regular expression pattern into a regular expression object
    PATTERN = re.compile('.*bust\s*[ :-]?\D*(?P<bustsize>[0-9]+)\s*(in|inches|")', re.IGNORECASE)
    PATTERN2 = re.compile('.*pit\s*[ :-]?\D*(?P<pit>[0-9]+)\s*(in|inches|")', re.IGNORECASE)
    PATTERN3 = re.compile('.*chest\s*[ :-]?\D*(?P<chest>[0-9]+)\s*(in|inches|")', re.IGNORECASE)
    # matches = [m for m in PATTERN.finditer(result)] #for m in PATTERN..., matches.append(m)


#really inefficient and repetitive!!!!
    matches = [m.group('bustsize') for m in PATTERN.finditer(result)]
    # empty collections evaluate to false
    if not matches:
        print "No match found: ", result
        #PATTERN2
        matches2 = [m.group('pit') for m in PATTERN2.finditer(result)]
        if not matches2:
            print "No match found on PATTERN2: ", result
            #PATTERN3
            matches3 = [m.group('chest') for m in PATTERN3.finditer(result)]
            if not matches3:
                print "No match found on PATTERN3: ", result
            elif len(matches3) > 1:
                print "Multiple matches found on PATTERN3: ", result, matches
            else:
                print "Got match on PATTERN3! Bust: ", matches3[0]

        elif len(matches2) > 1:
            print "Multiple matches found on PATTERN2: ", result, matches
        else:
            print "Got match on PATTERN2! Bust: ", matches2[0]
    elif len(matches) > 1:
        print "Multiple matches found: ", result, matches
    else:
        print "Got match! Bust: ", matches[0]


def get_waist(result):
    PATTERN = re.compile('.*waist\s*[ :-]?\D*(?P<waistsize>[0-9]+)\s*(in|inches|")', re.IGNORECASE)
    matches = [m.group('waistsize') for m in PATTERN.finditer(result)]
    # empty collections evaluate to false
    if not matches:
        print "No match found: ", result
        #make another pattern for sweep, full, open
    elif len(matches) > 1:
        print "Multiple matches found: ", result, matches
    else:
        print "Got match! Waist: ", matches[0]

def get_hip(result):
    PATTERN = re.compile('.*hips\s*[ :-]?\D*(?P<hipsize>[0-9]+)\s*(in|inches|")', re.IGNORECASE)
    PATTERN2 = re.compile('.*hips\s*[ :-]?\D*(?P<hipsize2>free|full|sweep|open)', re.IGNORECASE)

    matches = [m.group('hipsize') for m in PATTERN.finditer(result)]

    if not matches:
        print "No match found, try next pattern ", result

        """This is the next pattern, need to save all free/full/sweep as the same thing
        in database, like free. Need to only allow user to input one type, 'free'."""

        matches2 = [m.group('hipsize2') for m in PATTERN2.finditer(result)]
        if not matches2:
            print "No match found on PATTERN2: ", result
        #make another pattern for sweep, full, open
        elif len(matches2) > 1:
            print "Multiple matches found on PATTERN2: ", result, matches
        else:
            print "Got match on PATTERN2! Waist: ", matches2[0]

    elif len(matches) > 1:
        print "Multiple matches found: ", result, matches
    else:
        print "Got match! Waist: ", matches[0]

def get_shoulder(result):
    pass

def main():
    get_bust(listing2)

if __name__ == '__main__':
    main()