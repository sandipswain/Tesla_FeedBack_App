import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, app, render_template, request
from flask_sqlalchemy import SQLAlchemy

from send_mail import send_mail

dotenv_path = Path("./config/.env")
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)

ENV = "dev"

# ############## Connecting to the database ############## #
# if the environment == development
if ENV == "dev":
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQL_Local")


else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQL_Production")


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Creating an database object
db = SQLAlchemy(app)

# Creating a model
class Feedback(db.Model):
    __tablename__ = "feedback_data"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        # Fetching data from the form
        customer = request.form["customer"]
        dealer = request.form["dealer"]
        rating = request.form["rating"]
        comments = request.form["comments"]
        # print(customer, dealer, rating, comments)
        if customer == "" or dealer == "":
            return render_template(
                "index.html", message="* Please enter the required fields"
            )

        # Check whether the customer exists in the db. Like we are avoiding multiple feedbacks from a single customer
        ## If the count of the customer is 0 then add the data to the database

        if (
            db.session.query(Feedback).filter(Feedback.customer == customer).count()
            == 0
        ):
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()

            send_mail(customer, dealer, rating, comments)

            return render_template("success.html")
        return render_template(
            "index.html", message="You have already submitted your response"
        )


if __name__ == "__main__":
    app.run()
