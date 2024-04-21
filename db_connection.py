import pymongo
from pymongo import MongoClient

url= 'mongodb://localhost:27017'
client= pymongo.MongoClient(url)

db = client['campus_market']