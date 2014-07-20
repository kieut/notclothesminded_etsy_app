import re

BUST_PATTERNS = [
    re.compile('bust[- \t:~]+\D*(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile('pit[- \t:~]+\D*(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile('chest[- \t:~]+\D*(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile('armpit[- \t:~]+\D*(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
    #when size is listed first
    re.compile('(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*bust', re.IGNORECASE),
    re.compile('(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*pit', re.IGNORECASE),
    re.compile('(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*chest', re.IGNORECASE),
    re.compile('(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*armpit', re.IGNORECASE)
]

WAIST_PATTERNS = [
    re.compile('waist[- \t:~]+\D*(?P<waist>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile('(?P<waist>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*waist', re.IGNORECASE)

]

HIP_PATTERNS = [
    re.compile('hips?[- \t:~]+\D*(?P<hips>free|full|sweep|open)', re.IGNORECASE),
    re.compile('hips?[- \t:~]+\D*(?P<hips>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
    # when size is listed first
    re.compile('(?P<hips>free|full|sweep|open)[ \t\D]*hips?', re.IGNORECASE),
    re.compile('(?P<hips>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*hips?', re.IGNORECASE)
]

HIP_OPEN_VARIATIONS = ['full', 'Full', 'free', 'Free', 'FREE' 'Open', 'open', 'sweep', 'Sweep']

class ListingParser(object):
    def __init__(self, result):
        self.result = result

    def GetBust(self): 
        """parse description for measurements"""
        # print "\n*****listing description:"
        # print result
        # print "*******end of description*******"

        for pattern in BUST_PATTERNS:
            matches = [m.group('bust') for m in pattern.finditer(self.result)]
        # empty collections evaluate to false
            if not matches:
                continue
            if len(matches) > 1:
                print "*****Multiple bust matches*****: ", matches
                continue
            print "******Got match! Bust:******", matches[0]
            return str(matches[0])

    def GetWaist(self):
        # print "\n*****listing description:"
        # print result
        # print "*******end of description*******"

        for pattern in WAIST_PATTERNS:
            matches = [m.group('waist') for m in pattern.finditer(self.result)]
        # empty collections evaluate to false
            if not matches:
                continue
            if len(matches) > 1:
                print "*****Multiple waist matches*****: ", matches
                continue
            print "******Got match! Waist:******", matches[0]
            return str(matches[0])

    def GetHip(self):
        """This is the next pattern, need to save all free/full/sweep as the same thing
        in database, like free. Need to only allow user to input one type, 'free'."""

        # print "\n*****listing description:"
        # print result
        # print "*******end of description*******"

        for pattern in HIP_PATTERNS:
            matches = [m.group('hips') for m in pattern.finditer(self.result)]
        # empty collections evaluate to false
            if not matches:
                continue
            if len(matches) > 1:
                print "*****Multiple hip matches*****: ", matches
                continue
            print "******Got match! Hips:******", matches[0]
            for i in HIP_OPEN_VARIATIONS:
                if matches[0] == i: 
                    matches[0] = 100
                    print "******OPEN MATCH*******:%s" % matches[0]
            return str(matches[0])
