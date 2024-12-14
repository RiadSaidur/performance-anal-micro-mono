import pymongo
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure

# CLIENT_URL ='mongodb://localhost:27017/'
CLIENT_URL = 'mongodb+srv://mono:mono@netjobs.jglqn.mongodb.net/?retryWrites=true&w=majority&appName=netjobs'

client = pymongo.MongoClient(CLIENT_URL, server_api=ServerApi('1'))
db = client.faceRecognition

# Check MongoDB connection
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Connected to MongoDB")
except ConnectionFailure:
    print("MongoDB server not available")