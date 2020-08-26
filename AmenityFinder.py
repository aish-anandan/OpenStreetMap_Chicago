# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pymongo import MongoClient
from pymongo import GEO2D
client = MongoClient('localhost:27017')

# Get a list of db names 
dbs = MongoClient().list_database_names()

# Create a database
db = client["OpenStreetMapData"]

# Create a collection
Chicago_OSM = db['Chicago']

# Once the collection is created, insert the json data
data = "<path>/Chicago_output.json"
db.Chicago_OSM.insert(data)

# Verify
print (db.Chicago_OSM.find_one())

# Publish Indexes to make the search easier
db.Chicago_OSM.ensureIndex({"amenity":1})
db.Chicago_OSM.ensureIndex({"name":1})
db.Chicago_OSM.ensureIndex([("pos",GEO2D)])


search_tag = ["restaurant","Restaurant"]
name_match = "/*estauarnt*/" # This can be improved using regex (WIP)
current_location = [41.7153107, -87.9964622]

matches = db.Chicago_OSM.find({"$or": [{ "amenity" : {"$in": search_tag}, "name": name_match}],"pos":{"$near":current_location}})

# Add code for error handling - missing address components, if phone number is present display phone number
for match in matches:
    if "name" in match.keys():
        print("Name : " + match["name"])
    if "amenity" in match.keys():
        print("Amenity : " + match["amenity"])
    if "address" in match.keys():
        print("Address : " + match["address"]["housenumber"] +"," + match["address"]["street"])

