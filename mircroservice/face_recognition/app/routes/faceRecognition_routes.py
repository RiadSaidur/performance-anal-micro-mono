from flask import request
from flask_restful import Resource

from app.database.faceRecognition_database import getMissingPersonEncodings, saveMissingPersonEncodings
from app.services.faceRecognition_services import doesPersonExists, findEncodings, findMissingPerson


class FaceRecognition(Resource):
  def get(self):
    try:
      reportedPersonURL = request.args.get('url')
      encodedList = getMissingPersonEncodings()
      isFound = findMissingPerson(encodedList, reportedPersonURL)
      if isFound == None:
        return { "found": isFound, "error": "Face did not match" }, 404
      else:
        return { "found": isFound }, 200
    except FileNotFoundError:
      return { "found": False, "error": "Image not found" }, 404
    except KeyError:
      return { "found": False, "error": "Invalid arguments" }, 400
    except TypeError:
      return { "found": False, "error": "url argument required" }, 400
    except Exception as e:
      return { "found": False, "error": type(e) }, 500
  
  def post(self):
    try:
      missingPersonURL = request.get_json()['url']
      missingPersonId = request.get_json()['face']
      doesExist = doesPersonExists(missingPersonId)
      if doesExist:
        return { "successful": False, "error": "Person with this ID already exists" }, 409
      images = [missingPersonURL]
      encodeList = findEncodings(images)
      if not encodeList:
        return { "successful": False, "error": "Image not found" }, 404
      isSaved = saveMissingPersonEncodings(encodeList, missingPersonId)
      if isSaved:
        return { "successful": True }, 201
      return { "successful": False, "error": "Unable to store on Database" }, 500
    except KeyError:
      return { "successful": False, "error": "Invalid arguments" }, 400
    except FileNotFoundError:
      return { "successful": False, "error": "Image not found" }, 404
