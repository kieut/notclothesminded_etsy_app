from flask import Flask, request, session, render_template, redirect, flash
import model
import jinja2

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
    email = request.form["email"]
    password = request.form["password"]
    # print "_____________%r" % d
    # 1) create a User object with form data
    new_user = model.User(email=email, password=password)
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
    #create a User object with form.data
    query = model.db_session.query(model.User)
    user = query.filter_by(email=email)

    if user == None:
        flash("You are not in the database. Please sign up.")
    elif user.password != password:
        flash("Password incorrect. Unable to log in.")
        return render_template("login.html")
    else:
        #add customer to cookie session, which is a dictionary
        session["customer"] = [email, password]
        flash("You've successfully logged in.")

        #figure out redirect page, homepage? 
        return redirect("/")

    # user = model.db_session.query(model.User).filter_by(email=request.form['email']).filter_by(password=request.form['password']).one()
    # print user

    return render_template("login.html")


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

    """Need to check for exceptions, empty input fields """

    query = model.db_session.query(model.Listing).filter(model.Listing.min_bust <= max_bust).filter(model.Listing.max_bust >= min_bust)
    query = query.filter(model.Listing.min_waist <= max_waist).filter(model.Listing.max_waist >= min_waist)
    query = query.filter(model.Listing.min_hip <= max_hip).filter(model.Listing.max_hip >= min_hip)

    for word in title:
        print word
        query = query.filter(model.Listing.title.like('%' + word + '%'))
    # print query

    results = query.all()
    # returns listing objects, can call diff columns on it.
    # print results

    # for listing in results:
    #     print listing.title, listing.price, listing.listing_url

    # return ""
    return render_template("_search_results.html", listings = results )


@app.route("/listing_details")
def get_listing_detail():
    return render_template("listing_details.html")

@app.route("/test", methods = ["POST", "GET"])
def test():
    return "ajax return"
    # return render_template("_search_results.html", listings =)



if __name__ == '__main__':
    app.run(debug=True)