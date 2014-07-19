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

@app.route("/search_results")
def get_results():
    #make queries here. 
	return render_template("search_results.html")



if __name__ == '__main__':
    app.run(debug=True)