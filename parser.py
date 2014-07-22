import re

#pattern for all numbers, including decimals and fractions(ex. 17.5 or 17 1/2)
NUMBER_PAT = '[0-9]+\.?[0-9]*([ \t]*[0-9]+\/[0-9]+)?'
#Concatenates NUMBER_PAT with - and whitespaces to find any range numbers, captures only 2nd num??
RANGE_PAT = NUMBER_PAT + '(\s*-\s*' + NUMBER_PAT + ')?'

#Separates a fractional measurement into capture groups: dec, num, den
NUMBER_RE = re.compile('(?P<dec>[0-9]+\.?[0-9]*)(\s*(?P<num>[0-9]+)\/(?P<den>[0-9]+))?')

RANGE_RE = re.compile('(?P<min>' + NUMBER_PAT + ')(\s*-\s*(?P<max>' + NUMBER_PAT + '))?')

# BUST_PATTERNS_OLD = [
#     re.compile('bust[- \t:~]+\D*(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
#     re.compile('pit[- \t:~]+\D*(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
#     re.compile('chest[- \t:~]+\D*(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
#     re.compile('armpit[- \t:~]+\D*(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
#     #when size is listed first
#     re.compile('(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*bust', re.IGNORECASE),
#     re.compile('(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*pit', re.IGNORECASE),
#     re.compile('(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*chest', re.IGNORECASE),
#     re.compile('(?P<bust>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*armpit', re.IGNORECASE)
# ]

BUST_PATTERNS = [
    re.compile(
        '(bust|pit|chest)[- \t:~]+[^0-9\n]*'
        '(?P<bust>' + RANGE_PAT + ')[ \t]*(in|inches|")', re.IGNORECASE),
    #when size is listed first
    re.compile('(?P<bust>' + RANGE_PAT + ')[ \t]*(in|inches|")'
        '[^0-9\n]*(bust|pit|chest|armpit)', re.IGNORECASE),
]

# WAIST_PATTERNS_OLD = [
#     re.compile('waist[- \t:~]+\D*(?P<waist>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
#     re.compile('(?P<waist>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*waist', re.IGNORECASE)

# ]

WAIST_PATTERNS = [
    re.compile(
        'waist[- \t:~]+[^0-9\n]*(?P<waist>' + RANGE_PAT +
        ')[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile(
        '(?P<waist>' + RANGE_PAT + 
        ')[ \t]*(in|inches|")[^0-9\n]*waist', re.IGNORECASE)

]

# HIP_PATTERNS_OLD = [
#     re.compile('hips?[- \t:~]+\D*(?P<hips>free|full|sweep|open)', re.IGNORECASE),
#     re.compile('hips?[- \t:~]+\D*(?P<hips>([0-9\.\/\s-])+)[ \t]*(in|inches|")', re.IGNORECASE),
#     # when size is listed first
#     re.compile('(?P<hips>free|full|sweep|open)[ \t\D]*hips?', re.IGNORECASE),
#     re.compile('(?P<hips>([0-9\.\/\s-])+)[ \t]*(in|inches|")\D*hips?', re.IGNORECASE)
# ]

OPEN_PAT = 'free|full|open|sweep'
OPEN_RE = re.compile(OPEN_PAT, re.IGNORECASE)

HIP_PATTERNS = [
    re.compile(
        'hips?[- \t:~]+[^0-9\n]*(?P<hips>' + OPEN_PAT + ')', re.IGNORECASE),
    re.compile(
        'hips?[- \t:~]+[^0-9\n]*(?P<hips>' + RANGE_PAT +
        ')[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile(
        '(?P<hips>' + OPEN_PAT + ')[^0-9\n]*hips?', re.IGNORECASE),
    re.compile(
        '(?P<hips>' + RANGE_PAT + 
        ')[ \t]*(in|inches|")[^0-9\n]*hips?', re.IGNORECASE)
]


def ParseNumber(number_string):
    #Given a string containing a number, parses out match groups: dec, num, den
    # Convert the fractions to floats for easier storage. 
    if not number_string:
        return None
    match = NUMBER_RE.match(number_string)
    if match:
        dec = float(match.group('dec'))
        num = int(match.group('num') or 0)
        den = int(match.group('den') or 1)
        return dec + (float(num) / float(den))

def ParseRange(range_string):
    """Given a string containing a range of numbers, parse out the numbers.

    Args:
        range_string: String containing one number or a range of numbers
            separated by a hyphen.

    Returns:
        min, max: Floating point numbers in the range.  Max may be None if only
            a single number was found, and both may be None if no numbers
            were found.
    """
    match = RANGE_RE.match(range_string)
    if match:
        min_val = ParseNumber(match.group('min'))
        max_val = ParseNumber(match.group('max'))
        return min_val, max_val
    else:
        return None, None

class ListingParser(object):
    def __init__(self, result):
        self.result = result

    def GetBust(self): 
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
            min_val, max_val = ParseRange(str(matches[0]))
            print "******Got match! Bust: %s, Range: %s - %s" % (
                matches[0], min_val, max_val)
            #if max_val is 0 or None, it evaluates to False
            if not max_val:
                return min_val, min_val
            return min_val, max_val

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
            min_val, max_val = ParseRange(str(matches[0]))
            print "******Got match! Waist: %s, Range: %s - %s" % (
                matches[0], min_val, max_val)
            #if max_val is 0 or None, it evaluates to False
            if not max_val:
                #if false, set max_val to min_val
                return min_val, min_val
            return min_val, max_val

    def GetHip(self):
        """Saving all open hip variations as min_val:0, and max_val: 100"""

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
            if OPEN_RE.match(matches[0]):
                print "******OPEN HIP MATCH*******:%s" % matches[0]
                return 0, 100
            else:
                min_val, max_val = ParseRange(str(matches[0]))
                print "******Got match! Hip: %s, Range: %s - %s" % (
                matches[0], min_val, max_val)
            if not max_val:
                #if false, set max_val to min_val
                return min_val, min_val
            return min_val, max_val
