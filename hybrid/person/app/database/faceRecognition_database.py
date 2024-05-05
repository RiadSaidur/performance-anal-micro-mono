import numpy

from db import db

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