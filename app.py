from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
import extensions 
import models 
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)
# app.secret_key = os.urandom(24)  # Use a secure random key in production
# oauth = OAuth(app)

# oauth.register(
#   name='oidc',
#   authority='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_vTJE9GcZG',
#   client_id='3pldmehhl5l8ljuo28ab5lfstg',
#   client_secret='<client secret>',
#   server_metadata_url='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_vTJE9GcZG/.well-known/openid-configuration',
#   client_kwargs={'scope': 'phone openid email'}
# )

# Local database for Sprint 1
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marketplace.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = extensions.db

db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main_page")
def listings():
    listings = models.Listing.query.order_by(models.Listing.id.desc()).all()
    # user = session.get('user')

    # if user:
    #      return  f'Hello, {user["email"]}. <a href="/logout">Logout</a>'
    # else:
    #      return f'Welcome! Please <a href="/login">Login</a>.'

    return render_template("main_page.html", listings=listings)

# @app.route('/login')
# def login():
#     # Alternate option to redirect to /authorize
#     # redirect_uri = url_for('authorize', _external=True)
#     # return oauth.oidc.authorize_redirect(redirect_uri)
#     return oauth.oidc.authorize_redirect('https://d84l1y8p4kdic.cloudfront.net')

# @app.route('/authorize')
# def authorize():
#     token = oauth.oidc.authorize_access_token()
#     user = token['userinfo']
#     session['user'] = user
#     return redirect(url_for('index'))

# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect(url_for('index'))

# @app.route('/callback')
# def callback():
#     token = cognito.authorize_access_token()
#     user = token['userinfo']
#     session['user'] = user  # store in session
#     return redirect('/dashboard')

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/')



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

        return redirect(url_for("listings"))

    return render_template("create_listing.html")

@app.route("/register_user", methods = ["GET", "POST"])
def create_user():
    if request.method == "POST":
            email = request.form["email"].strip()
            username = request.form["username"].strip()
            password = request.form["password"].strip()
    
            if not email or not username or not password:
                return render_template(
                    "register_user.html",
                    error="All fields are required."
                )
            user = models.User(
                email = email, 
                username=username
            )

            user.set_password(password)

            #extensions.verifyEmail(email)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for("listings"))
    return render_template("register_user.html")


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True)