Notclothesminded
=========================

Overview
-----------

Notclothesminded is a web application that facilitates a more tailored purchasing experience for avid vintage clothing
consumers who seek one-of-a-kind items on Etsy’s e-commerce marketplace.The application augments existing Etsy search
capabilities with a measurement specific search facet by parsing freeform seller entered listing descriptions for each
buyer’s unique measurements in over 200,000 active listings.  This enables buyers to locate items specific to their 
search criteria quickly and without the hassle of manually scanning numerous beautiful but ill-fitting matches. 
Users waste less time, and are connected to more meaningful results. 

How it works
------------
Presentation Layer:  HTML, CSS, JS, JQuery, AJAX, JSON and Bootstrap<br/>
Application Layer: Python, Flask<br/>
Data Layer: Postgres, SQLAlchemy<br/>
APIs: Etsy<br/>

Notclothesminded's crawler makes HTTP requests to Etsy's API to retrieve active listings in Vintage/Clothing/Dresses, parses the listing descriptions for measurements using Regular Expressions, and commits them to a Postgres database. For database maintenance, every time the crawler is executed, it first deletes all expired listings before making batch requests to the Etsy API. It should crawl every couple of hours to ensure an updated database of active etsy listings.

###Crawler Components:

1. __crawler.py__: Main entry point, primary logic file.
2. __etsy.py__: Abstracts the Etsy API.
2. __parser.py__: Utility class, used for parsing listing descriptions.
3. __model.py__: Abstracts the local database model.

__Project Organization Diagram__:
![Alt text](/static/img/project_diagram.png)

###Database Tables:
See model.py for full schema details, the purpose of each table is:

1. __listings__: Stores matches listings and respective measurements.
2. __images__: Stores image URLs for listings.
2. __crawlhistory__: Stores crawl metadata for maintaining an audit trail.

###User Interface:


From the browser, the user can input a description of what they’re looking(case insensitive search) and measurements. Using AJAX and JQuery, the results are dynamically retrieved and rendered with new HTML in the same browser. I chose to do this to ensure an uninterrupted user experience. The results are presented in pages to reduce loading time, and each page link is an event handler, which when clicked, makes an AJAX request for the next set of listings. 

Set up
------------
### Get the code

Clone this repo (or fork, which you'll want to do eventually).

Open a terminal in the repo root directory and run:

```
pip install -r requirements.txt
```
### Etsy API

You will need to get your own Etsy API_KEY. Once you obtain one, put it in a file named "etsy_api_key"

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

The controller file, crawler.py, takes argv parameters from the command line that represent the min and max price range of your HTTP request to the Etsy API. Execute crawler.py file with price parameters in the command line to populate the database:


```
python -B crawler.py 50 100
```


Tips for Contributing
------
__Let's get more dresses!__ There is currently no standard format for sellers to list measurements in their descriptions. As such, the application is only able to capture measurements from about 50% of the total number of active listings. While it accounts for many variants, it is difficult to account for all the possible variations of listings from different sellers. Here are some examples:

1. Listings that do not list measurements, or are missing a necessary measurement (i.e. bust or waist). 
2. Listings that have two items, and thus two sets of measurements.
  1. Best fits a modern xsmall - small. Please see measurements to ensure a great fit!
     <br>Dress- 
     <br>Bust: 35"
     <br>Waist: 25"
     <br>Length: 15" shoulder to waist, 29" waist to hem
    
     Bolero- 
     <br>Shoulder: approx 15"
     <br>Bust: 38"
     <br>Length: 13"
     <br>Sleeve length: 18"
3. Listings that also include the model's measurement, along with the item.
4. Typos!!

These unmatched listings may possibly be captured with NLP, or statistical probability. 
