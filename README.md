Notclothesminded
=========================

Overview
-----------

Notclothesminded is a web application that facilitates a more tailored purchasing experience for avid vintage clothing
consumers who seek one-of-a-kind items on Etsy’s e-commerce marketplace.The application augments existing Etsy search
capabilities with a measurement specific search facet by parsing freeform seller entered listing descriptions for each
buyer’s unique measurements in over 1 million active listings.  This enables buyers to locate items specific to their 
search criteria quickly and without the hassle of manually scanning numerous beautiful but ill-fitting matches. 
Users waste less time, and are connected to more meaningful results. 

How it works
------------
On the backend, it uses Python, Flask as a MVC framework, SQLAlchemy as an ORM, and Postgres as the database. It
makes calls to Etsy's API to retrieve active listings in Vintage/Clothing/Dresses, parses the listing descriptions for
measurements using Regular Expressions, and commits them to a Postgres database. 

For database maintenance, every time the crawler is executed, it first deletes all expired listings before making batch requests to the Etsy API. The crawler crawls every couple of hours to ensure an updated database of active etsy listings. 


On the frontend, Notclothesminded uses Bootstrap, and JQuery to ensure an uninterrupted user experience by dynamically
loading results in the browser per user query.


The following diagram maps out the code structure:


Set up
------------
### Get the code

Clone this repo (or fork, which you'll want to do eventually).

Open a terminal in the repo root directory and run:

```
pip install -r requirements.txt
```
### Etsy API

You will need to get your own Etsy API_KEY. Once you obtain one, it needs to be accessible by etsy.py.

[Etsy API Documentation](https://www.etsy.com/developers/documentation/getting_started/api_basics)



### Create Database

My application used a Postgres database, but if you'd like to use a different one, please feel free to configure engine.

Install [Postgres](http://postgresapp.com/documentation/).


To create the database and the tables, type the following into command line:


```
python -i model.py
create_tables()
```

### Populate the Database

The controller file, crawler.py, takes argv parameters from the command line that represent the min and max range of your
HTTP request to the Etsy API. Run the crawler.py file price parameters in the command line to populate the database.


```
python -B crawler.py 50 100
```
