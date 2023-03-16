
from flask import Flask, render_template, redirect
#render template helper function to render HTML template
#redirect users back to index page after adding documents to collection
from flask_pymongo import PyMongo
from pymongo import MongoClient #used to creat client object for MongoDB instance
import scrape_mars #import python script

# Create an instance of Flask
app = Flask(__name__)

#instantiate PyMongo and pass host of MongoDB server(local) and port
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
#Create MongoDB db called mars_db and save reference variable "db"
db = mongo.db.mars_db #Does this set up mongo database?
mars_data= db.mars_data #create collection called mars_data to store group of docs in MongoDB

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = db.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    run_scrape = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    db.update_one({}, {"$set": run_scrape}, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
