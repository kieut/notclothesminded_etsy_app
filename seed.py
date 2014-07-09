import model
import json, httplib2
import pprint
import urllib

mykey = 'vgmfi5108akc4ot4rthtrw08'


# o this is *basically* allowing me to do a remote table query on the etsy database
# so I'm basically interacting with the etsy database through their api, which is a http request?
# Now how do I do it in webapp.py???

def connect(mykey):
	#HTTP GET request for active listings, filter by category string path "Vintage/Clothing"
	#Need to figure out how to paginate through count?
	#everything after ? is a parameter
	#urllib creates the url with parameters for me


	"""Need to convert this to urlli"""
	# for p in range(10, 100):
	# 	resp, content = httplib2.Http().request("https://openapi.etsy.com/v2/listings/active?api_key=vgmfi5108akc4ot4rthtrw08&limit=5&offset=0&category=Vintage%%2FClothing&min_price=%d&max_price=%d" % (p, p+1))
	# 	print p, json.loads(content)['count']

	p = 0
	"""Need a new url for each time through this loop, so need to do the urlencode inside the loop (and the join)"""
	"""This only gets me the count for each 'price bucket', only gives me 100 items per query.
	Still need to query for items for 100-150, 150-200, and >200, and tab through paginations"""
	for p in range(10, 100):
		parameters = urllib.urlencode({'api_key': mykey, 'limit': 100, 'offset': 0, 'category': 'Vintage/Clothing', 'min_price': p, 'max_price': p+1})
		url = '?'.join(['https://openapi.etsy.com/v2/listings/active', parameters])
		# print "url__________________%s" % url
		resp, content = httplib2.Http().request(url)
		print p, json.loads(content)['count']





	# resp, content = httplib2.Http().request("https://openapi.etsy.com/v2/listings/active?api_key=vgmfi5108akc4ot4rthtrw08&limit=5&offset=0&category=Vintage/Clothing")
	# result = json.loads(content)
	# pprint.pprint(result['results'])
	# length = len((result['results']))

	# print "_______________length:%r" % length


def search_results():
	pass

def main():
	connect(mykey)

if __name__ == "__main__":
    main()