import model
import json, httplib2
import pprint

key = 'vgmfi5108akc4ot4rthtrw08'

# o this is *basically* allowing me to do a remote table query on the etsy database
# so I'm basically interacting with the etsy database through their api, which is a http request?
# Now how do I do it in webapp.py???

def connect():
	#HTTP GET request for active listings, filter by category string path "Vintage/Clothing"
	#Need to figure out how to paginate through count
	resp, content = httplib2.Http().request("https://openapi.etsy.com/v2/listings/active?api_key=vgmfi5108akc4ot4rthtrw08&limit=5&offset=0&category=Vintage/Clothing")
	result = json.loads(content)
	pprint.pprint(result['results'])
	length = len((result['results']))

	print "_______________length:%r" % length


def search_results():
	pass

def main():
	connect()

if __name__ == "__main__":
    main()