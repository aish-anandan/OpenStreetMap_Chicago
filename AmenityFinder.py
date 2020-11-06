# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 22:09:20 2020

@author: Aishwarya
"""

from pymongo import MongoClient,GEO2D
import json
import nltk
from nltk.corpus import wordnet 

#nltk.download('wordnet')
#mongodb+srv://aish_anandan:08011995@cluster-1-twvy8.mongodb.net/<dbname>?retryWrites=true&w=majority
client = MongoClient('localhost',27017)
db = client.ChicagoOSM
collection = db.Amenities

file = open('./OpenStreetMap_Chicago/chicago_output_coord_fixed.json','r')
data = json.load(file)
      
collection.insert_many(data)

print(collection.count_documents({}))

collection.create_index([("geoloc","2dsphere")])   

# Geometry
input_point = [-87.65338,41.7379093] #[long, lat]
dist_within_miles = 0.5 
search_q = {
 'geoloc':
    {'$near':
        {'$geometry': 
            {'type': "Point",
             'coordinates': input_point
             },
            '$maxDistance': dist_within_miles*1609.34
        }
    }
}

# Include amenities
amenity = ["Hospital","Restaurant", "Pharmacy", "Church", "Public Transport", "School"]
if amenity[3] == "Church":
    list = [
    {'amenity':'place_of_worship'},
    {'name':{'$regex':'*[Cc]hurch*'}},
    {'religion':{'$exists':True}}
    ]
    
    search_q['$or'] = list
    
collection.find(search_q)

res = collection.find(search_q)
for i in res:
    print(i)
    
'''
synonyms = []
for syn in wordnet.synsets("food"): 
    for i in syn.hypernyms():
        synonyms.append(i.name())

first_word = wordnet.synset("worship.n.01")
second_word = wordnet.synset("church.n.01")
print('Similarity: ' + str(first_word.wup_similarity(second_word)))
'''
