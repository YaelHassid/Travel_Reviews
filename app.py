from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

#db init:
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(20), unique=False, nullable=False)
    country = db.Column(db.String(20), unique=False, nullable=False)
    photo = db.Column(db.String(100), unique=False, nullable=False)
    introduction = db.Column(db.String(800), unique=False, nullable=False)
    landmarks = db.Column(db.String(800), unique=False, nullable=False)
    cultural = db.Column(db.String(800), unique=False, nullable=False)
    activities = db.Column(db.String(800), unique=False, nullable=False)
    culinary = db.Column(db.String(800), unique=False, nullable=False)

class User(db.Model):
    username = db.Column(db.String(50), unique=True, primary_key=True)
    password = db.Column(db.String(20), unique=False, nullable=False)
    f_name = db.Column(db.String(20), unique=False, nullable=False)
    l_name = db.Column(db.String(20), unique=False, nullable=False)
    is_admin = db.Column(db.Integer, unique=False, nullable=False, default=0)

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.Integer, unique=False)
    by = db.Column(db.String(50), unique=False, nullable=False)
    review = db.Column(db.String(800), unique=False, nullable=False)

@app.route("/")
def homePage():
    username = request.args.get('username', 'Anonymous')
    is_admin = int(request.args.get('is_admin', 0))
    locations = Location.query.all()
    print(username, is_admin)
    return render_template("homepage.html", locations=locations, username=username, is_admin=is_admin)

@app.route("/add_location/<is_admin>/<username>", methods=["POST", "GET"])
def add_location(is_admin, username):
    if request.method == "POST":
        city = request.form.get("city")
        country = request.form.get("country")
        photo = request.form.get("photo")
        introduction = request.form.get("introduction")
        landmarks = request.form.get("landmarks")
        cultural = request.form.get("cultural")
        activities = request.form.get("activities")
        culinary = request.form.get("culinary")
        location_obj = Location(city=city, country=country, photo=photo, introduction=introduction, landmarks=landmarks, cultural=cultural, activities=activities, culinary=culinary)
        db.session.add(location_obj)
        db.session.commit()
        return redirect(url_for("homePage", username=username, is_admin=int(is_admin)))

    else:   
        return render_template("add_location.html")

@app.route("/add_review/<int:location_id>/<username>/<is_admin>", methods=["POST", "GET"])
def add_review(location_id, username, is_admin):
    if request.method == "POST":
        review = request.form.get("review")
        review_obj = Review(location_id=location_id, by=username, review=review)
        db.session.add(review_obj)
        db.session.commit()
        return redirect(url_for("homePage", username=username, is_admin=is_admin))
    else:
        return render_template("add_review.html")



@app.route("/location/<int:location_id>/<username>/<is_admin>")
def view_location(location_id, username, is_admin):
    location = Location.query.get(location_id)
    reviews = Review.query.filter_by(location_id=location_id).all()
    if location:
        return render_template("location.html", location=location, username=username, is_admin=is_admin, reviews=reviews)
    else:
        return "Location not found", 404




@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        user_obj = User(username=username, password=password, f_name=f_name, l_name=l_name)
        user = User.query.filter_by(username=username).first()
        if not user:
            db.session.add(user_obj)
            db.session.commit()
            if user_obj:
                return redirect(url_for("homePage", username=username, is_admin=int(user_obj.is_admin)))
            else:
                return render_template("sign_up.html")
        else :
            flash('username already exist!')
            return render_template("sign_up.html")    
    else:
        return render_template("sign_up.html")

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        if user:
            # Check if the password is correct
            if user.password == password:
                return redirect(url_for("homePage", username=username, is_admin=int(user.is_admin)))
            else:
                flash('Incorrect password!')
                return render_template("sign_in.html")
        else:
            flash('Username not found!')
            return render_template("sign_in.html")
    else:
        return render_template("sign_in.html")

if __name__ == "__main__":
    app.run(debug=True)