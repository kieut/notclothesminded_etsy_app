import re

#pattern for all numbers, including decimals and fractions(ex. 17.5 or 17 1/2)
NUMBER_PAT = '[0-9]+\.?[0-9]*([ \t]*[0-9]+\/[0-9]+)?'
#Concatenates NUMBER_PAT with - and whitespaces to find any range numbers
RANGE_PAT = NUMBER_PAT + '(\s*-\s*' + NUMBER_PAT + ')?'

#Separates a fractional measurement into capture groups: dec, num, den
NUMBER_RE = re.compile('(?P<dec>[0-9]+\.?[0-9]*)(\s*(?P<num>[0-9]+)\/(?P<den>[0-9]+))?')

RANGE_RE = re.compile('(?P<min>' + NUMBER_PAT + ')(\s*-\s*(?P<max>' + NUMBER_PAT + '))?')

BUST_PATTERNS = [
    re.compile(
        '(bust|pit|chest)[- \t:~]+[^0-9\n]*'
        '(?P<bust>' + RANGE_PAT + ')[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile('(?P<bust>' + RANGE_PAT + ')[ \t]*(in|inches|")'
        '[^0-9\n]*(bust|pit|chest|armpit)', re.IGNORECASE),
]

WAIST_PATTERNS = [
    re.compile(
        'waist[- \t:~]+[^0-9\n]*(?P<waist>' + RANGE_PAT +
        ')[ \t]*(in|inches|")', re.IGNORECASE),
    re.compile(
        '(?P<waist>' + RANGE_PAT + 
        ')[ \t]*(in|inches|")[^0-9\n]*waist', re.IGNORECASE)

]

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
        self.output = []

    def GetBust(self):
        for pattern in BUST_PATTERNS:
            matches = [m.group('bust') for m in pattern.finditer(self.result)]
        # empty collections evaluate to false
            if not matches:
                continue
            if len(matches) > 1:
                self.output.append(
                    "  Single regex got multiple bust matches: %s" % matches)
                continue
            min_val, max_val = ParseRange(str(matches[0]))
            self.output.append(
                "  Got bust match: %s, Range: %s - %s" % (
                matches[0], min_val, max_val))
            #if max_val is 0 or None, it evaluates to False
            if not max_val:
                return min_val, min_val
            return min_val, max_val

    def GetWaist(self):
        for pattern in WAIST_PATTERNS:
            matches = [m.group('waist') for m in pattern.finditer(self.result)]
        # empty collections evaluate to false
            if not matches:
                continue
            if len(matches) > 1:
                self.output.append(
                    "  Single regex got multiple waist matches: %s" % matches)
                continue
            min_val, max_val = ParseRange(str(matches[0]))
            self.output.append(
                "  Got waist match: %s, Range: %s - %s" % (
                matches[0], min_val, max_val))
            #if max_val is 0 or None, it evaluates to False
            if not max_val:
                #if false, set max_val to min_val
                return min_val, min_val
            return min_val, max_val

    def GetHip(self):
        """Saving all open hip variations as min_val:0, and max_val: 100"""
        for pattern in HIP_PATTERNS:
            matches = [m.group('hips') for m in pattern.finditer(self.result)]
        # empty collections evaluate to false
            if not matches:
                continue
            if len(matches) > 1:
                self.output.append(
                    "  Single regex got multiple hip matches: %s" % matches)
                continue
            self.output.append(
                "  Got hips match: %s" % matches[0])
            if OPEN_RE.match(matches[0]):
                self.output.append("    OPEN HIP MATCH")
                return 0, 100
            else:
                min_val, max_val = ParseRange(str(matches[0]))
                self.output.append(
                    "    Range hip match: %s - %s" % (min_val, max_val))
            if not max_val:
                #if false, set max_val to min_val
                return min_val, min_val
            return min_val, max_val
