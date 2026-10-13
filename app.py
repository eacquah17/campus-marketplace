from flask import Flask, render_template, request, redirect, url_for
from extensions import db 
import models 

app = Flask(__name__)

# Local database for Sprint 1
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marketplace.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def index():
    listings = models.Listing.query.order_by(models.Listing.id.desc()).all()
    return render_template("index.html", listings=listings)


@app.route("/create_listing", methods=["GET", "POST"])
def create_listing():
    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        price = request.form["price"].strip()

        if not title or not description or not price:
            return render_template(
                "create_listing.html",
                error="All fields are required."
            )

        try:
            price_value = float(price)

            if price_value < 0:
                raise ValueError

        except ValueError:
            return render_template(
                "create_listing.html",
                error="Please enter a valid price."
            )

        listing = models.Listing(
            title=title,
            description=description,
            price=price_value
        )

        db.session.add(listing)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("create_listing.html")

@app.route("/register_user", methods = ["GET", "POST"])
def create_user():
    if request.method == "POST":
            email = request.form["email"].strip()
            username = request.form["username"].strip()
            password = request.form["password"].strip()
    
            if not email or not username or not password:
                return render_template(
                    "create_listing.html",
                    error="All fields are required."
                )
            user = models.User(
                email = email, 
                username=username
            )

            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for("index"))
    return render_template("register_user.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)