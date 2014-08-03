Notclothesminded
=========================

Overview
-----------

Notclothesminded is a web application that facilitates a more tailored purchasing experience for avid vintage clothing
consumers who seek one-of-a-kind items on Etsy’s e-commerce marketplace.The application augments existing Etsy search
capabilities with a measurement specific search facet by parsing freeform seller entered listing descriptions for each
buyer’s unique measurements in over 300,000 active listings.  This enables buyers to locate items specific to their 
search criteria quickly and without the hassle of manually scanning numerous beautiful but ill-fitting matches. 
Users waste less time, and are connected to more meaningful results. 

How it works
------------
Presentation Layer:  HTML, CSS, JS, JQuery, AJAX, JSON and Bootstrap
Application Layer: Python, Flask
Data Layer: Postgres, SQLAlchemy
APIs: Etsy

Notclothesminded's crawler makes HTTP requests to Etsy's API to retrieve active listings in Vintage/Clothing/Dresses, parses the listing descriptions for measurements using Regular Expressions, and commits them to a Postgres database. For database maintenance, every time the crawler is executed, it first deletes all expired listings before making batch requests to the Etsy API. It crawls every couple of hours to ensure an updated database of active etsy listings. 

The following diagram maps out the backend code structure:


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

My application used a Postgres database, but if you'd like to use a different one, please feel free to configure the engine.

Install [Postgres](http://postgresapp.com/documentation/).


To create the database and the tables, type the following into command line:


```
python -i model.py
create_tables()
```

### Populate the Database

The controller file, crawler.py, takes argv parameters from the command line that represent the min and max range of your
HTTP request to the Etsy API. Execute crawler.py file with price parameters in the command line to populate the database.


```
python -B crawler.py 50 100
```


Tips for Contributing
------
1. __Let's get more dresses!__ Currently, the application is only able to capture measurements from about 50% of the total number of active listings. This is due to the difficulty of accounting for all the possible variations of listings from different sellers. Some of the more obvious difficult to capture listings:

  1. Listings that do not list measurements, or are missing a necessary measurement (i.e. bust or waist). 
  2. Listings that have two items, and thus two sets of measurements.
    1. Best fits a modern xsmall - small. Please see measurements to ensure a great fit!
       Dress- 
       Bust: 35"
       Waist: 25"
       Length: 15" shoulder to waist, 29" waist to hem
      
       Bolero- 
       Shoulder: approx 15"
       Bust: 38"
       Length: 13"
       Sleeve length: 18"
  3. Listings that also include the model's measurement, along with the item.
  4. Typos!!
  5. 
