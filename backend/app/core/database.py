from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.mongodb_url)
db = client['studentdb']

users_collection = db['users']
metrics_collection = db['metrics']
predictions_collection = db['predictions']
