from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/db"
mongo = PyMongo(app)

# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)

# Define the 'classDB' database in Mongo
# db = client.mars

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    # mars_data = scrape_mars.scrape_all()
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)