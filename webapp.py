from flask import Flask, request, session, render_template, redirect, flash
import model
import jinja2
from sqlalchemy.orm.exc import NoResultFound
import json
import md5

app = Flask(__name__)
app.secret_key = 'dress'

@app.route("/")
def index():
    """This is the 'cover' page of the notclothesminded site""" 
    return render_template("index.html")

@app.route("/signup", methods=["GET"])
def show_signup():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def process_sign_up():
    first_name = request.form['first_name']
    surname = request.form['surname']
    email = request.form["email"]
    password = request.form["password"]

    # print "_____________%r" % d
    # 1) create a User object with form data
    new_user = model.User(first_name=first_name, surname=surname, email=email, password=password)
    # 2) add object to db
    model.db_session.add(new_user)
    model.db_session.commit()
    return render_template("signup.html")

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    query = model.db_session.query(model.User)

    try:    # if username exists
        user = query.filter_by(email = email).one()

        if user.password != password:
            flash ("Password incorrect, unable to login.  Please try again.")
            return render_template("login.html")
        else:
            session['user'] = user.first_name
            session['email'] = user.email
            return redirect("/search")

    except NoResultFound:   # if username does not exist
        flash ("%s is not a registered email.  Please try again." % email)
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You've successfully logged out.")
    return render_template("logout.html")


@app.route("/user/<int:id>")
def show_favorites():
	"""This page will display the user's saved items, as well as the search facet
	panel on the left hand side"""
	pass

@app.route("/search")
def search():
    #make queries here. 
    return render_template("search.html")

@app.route("/search_results", methods=["POST"])
def get_results():
    # need to break up description and query for each one against title


    description = request.form['description']
    title = description.split(' ')
    min_bust = request.form['min-bust']
    max_bust = request.form['max-bust']
    min_waist = request.form['min-waist']
    max_waist = request.form['max-waist']
    min_hip = request.form['min-hip']
    max_hip = request.form['max-hip']

    result_key = md5.new(json.dumps([title, min_bust, max_bust, min_waist, max_waist, min_hip, max_hip])).digest().encode("hex")

    #session[result_key] = "lol"

    #print session.viewkeys(),result_key

    if 'results' in session.keys():
        #print "RESUTS IN SESSION"
        if result_key in session['results']:
            #print "I'M GETTING DATA FROM THE CACHE"
            results = session['results'][result_key]
    else:
        #print "I'M GETTING DATA FROM THE DATABASE"
        """Need to check for exceptions, empty input fields """

        query = model.db_session.query(model.Listing).filter(model.Listing.min_bust <= max_bust).filter(model.Listing.max_bust >= min_bust)
        query = query.filter(model.Listing.min_waist <= max_waist).filter(model.Listing.max_waist >= min_waist)
        query = query.filter(model.Listing.min_hip <= max_hip).filter(model.Listing.max_hip >= min_hip)

        for word in title:
            #print word
            query = query.filter(model.Listing.title.ilike('%' + word + '%'))
        # print query

        results = query.all()

        if 'results' not in session.keys():
            session['results'] =  {}

        session['results'][result_key] = results

        #print session['results'][result_key]


    count = len(results)
    #print count

    def format_price(amount):
        return u'{0:.2f}'.format(amount)

    return render_template("_search_results.html", listings = results, count = count, format_price = format_price)


@app.route("/listing_details")
def get_listing_detail():
    return render_template("listing_details.html")


if __name__ == '__main__':
    app.run(debug=True)