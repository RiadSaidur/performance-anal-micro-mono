import numpy
import pymongo
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure

CLIENT_URL ='mongodb://localhost:27017/'
# CLIENT_URL = 'mongodb+srv://syds:ariana@netjobs.jglqn.mongodb.net/?retryWrites=true&w=majority&appName=netjobs'

client = pymongo.MongoClient(CLIENT_URL, server_api=ServerApi('1'))
db = client.faceRecognition

# Check MongoDB connection
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Connected to MongoDB")
except ConnectionFailure:
    print("MongoDB server not available")

def saveMissingPersonEncodings(encodeList, faceList):
  try:
    db.encodeList.insert_one({ "faceEncoding": list(encodeList[0]), "face": faceList })
    return True
  except Exception as e:
    print(e)
    return False

def getMissingPersonEncodings():
  try:
    faceCursor = db.encodeList.aggregate([{
      "$group": {
        "_id": 'encodings',
        "knownEncodings": {
          "$push": "$faceEncoding"
        },
        "faceList": {
          "$push": "$face"
        }
      }
    }])
    if not faceCursor:
      return None
    for faceEncodings in faceCursor:
      knownEncodings = faceEncodings['knownEncodings']
      encoding = [ numpy.array(faceEncoding) for faceEncoding in knownEncodings]
      return {"encoding": encoding, "faces": faceEncodings['faceList']}
  except Exception as e:
    print(e)
    return []

def getExistingMissingPersonEncoding(missingPersonId):
  isEncoded = db.encodeList.find_one({ 'face': missingPersonId })
  return isEncoded