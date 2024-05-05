import numpy

from app.database.db import db

def saveImage(filename):
  try:
    db.image.insert_one({ "filename": filename })
    return True
  except Exception as e:
    return False

def saveMissingPersonEncodings(encodeList, faceList):
  try:
    db.encodeList.insert_one({ "faceEncoding": list(encodeList[0]), "face": faceList })
    return True
  except Exception as e:
    return False
