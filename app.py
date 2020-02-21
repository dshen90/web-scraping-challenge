from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_CXH

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")

@app.route("/")
def home():
	mars_data = mongo.db.collection.find_one()
	if mars_data is None:
		mars_data={}
		mars_data['latest_news']={'title': "NASA's Briefcase-Size MarCO Satellite Picks Up Honors",
  'paragraph': 'The twin spacecraft, the first of their kind to fly into deep space, earn a Laureate from Aviation Week & Space Technology.'}
		mars_data['featured_image_url'] = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19101_ip.jpg'
		mars_data['mars_weather'] = 'sol 366 (2019-12-07) low -98.9ºC (-146.1ºF) high -20.4ºC (-4.8ºF), winds from the SSE at 5.7 m/s (12.6 mph) gusting to 20.4 m/s (45.5 mph), pressure at 6.60 hPa'
		mars_data['mars_facts'] = html_mars
		mars_data['mars_hemisphere_images_url'] = [{'title': 'Cerberus Hemisphere Enhanced',
   'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
  {'title': 'Schiaparelli Hemisphere Enhanced',
   'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
  {'title': 'Syrtis Major Hemisphere Enhanced',
   'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},
  {'title': 'Valles Marineris Hemisphere Enhanced',
   'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}] 
		
	return render_template("index.html", mars_data=mars_data )

@app.route("/scrape")
def scrape():
	mars_data = scraper.scrape()
	print(mongo.db.collection.update({}, mars_data, upsert=True))

	return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)