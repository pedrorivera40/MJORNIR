from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import datetime
from handler.user import UserHandler
from handler.athlete import AthleteHandler
from auth import verifyHash, generateToken, verifyToken
from functools import wraps
from dotenv import load_dotenv
import os
from handler.position import PositionHandler

## Load environment variables
load_dotenv()




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def token_check(func):
    """
    Midleware to verify the request is authorized.

    Midleware function used to protect routes from unauthorized request
    by verifying each request provides a valid token.
    """
    @wraps(func)
    def decorated():

        token = request.headers.get('Authorization')
        print(token)
        print(request.headers)
        print(request.get_json())

        if not token:
            return jsonify(Error='Token is missing'), 403

        response = verifyToken(token, os.getenv('SECRET_KEY'))
        print(response, os.getenv('SECRET_KEY'))

        if response == False:
            return jsonify(Error="Token is invalid"), 403
        else:
            pass
        return func()
    return decorated


@app.route("/")
def hello():
    return jsonify("Hi, this is a route that will be eliminated xD")

#--------- Athlete Routes ---------#
@app.route("/athletes/",methods = ['GET','POST'])
def athletes():
    handler = AthleteHandler()
    if request.method == 'POST':
        json = request.json
        return handler.addAthlete(json['sID'],json['attributes'])
    elif request.method == 'GET':
        json = request.json
        return handler.getAtheletesBySport(json['sID'],json['branch'])

@app.route("/athletes/<int:aid>/", methods = ['GET','POST','PUT','DELETE'])
def athleteByID(aid):
    handler = AthleteHandler()
    if request.method == 'GET':
        return handler.getAthleteByID(aid)   
    elif request.method == 'PUT':
        json = request.json
        return handler.editAthlete(aid,json['attributes'])
    elif request.method == 'DELETE':
        json = request.json
        return handler.removeAthlete(aid)

#--------- Position Routes ---------# 
@app.route("/positions/", methods = ['GET','DELETE'])
def position():
    handler = PositionHandler()
    if request.method == 'GET':
        return handler.getPositionByName(request.json['psName'])
    elif request.method == 'DELETE':
        return handler.removeAthletePosition(request.json['apID'])
    

@app.route("/positions/<int:sid>", methods = ['GET'])
def sportPositions(sid):
    handler = PositionHandler()
    if request.method == 'GET':
        return handler.getPositions(sid)

@app.route("/positions/<int:sid>/<int:aid>", methods = ['GET','POST','PUT'])
def athletePositions(sid,aid):
    handler = PositionHandler()
    if request.method == 'GET':
        return handler.getAthletePositionInSport(sid,aid)
    if request.method == 'POST':
        return handler.addAthletePosition(request.json['psID'],aid)
    if request.method == 'PUT':
        return handler.editAthletePosition(request.json['apID'],request.json['psID'],aid)

###########################################
#--------- Dashboard User Routes ---------#
###########################################
@app.route("/users/", methods = ['GET','POST'])
def allUsers():
    handler = UserHandler()
    req = request.json
    if request.method == 'GET':
        ## For user list display
        return handler.getAllDashUsers()
    if request.method == 'POST':
        ## For account creation
        return handler.addDashUser(req['username'],req['full_name'], req['email'], req['password'])

@app.route("/users/<int:duid>", methods = ['GET','PATCH'])
def userByID(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'GET':
        ## For managing specific users
        return handler.getDashUserByID(duid)
    if request.method == 'PATCH':
        ## For username change
        return handler.updateDashUserUsername(duid,req['username'])

@app.route("/users/username/", methods = ['POST'])
def getUserByUsername():
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        return handler.getDashUserByUsername(req['username'])

@app.route("/users/email/", methods = ['POST'])
def getUserByEmail():
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        return handler.getDashUserByEmail(req['email'])

@app.route("/users/<int:duid>/reset", methods = ['PATCH'])
def passwordReset(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'PATCH':
        ## For password reset
        password = createHash(req['password'])
        return handler.updateDashUserPassword(duid,password)

@app.route("/users/<string:duid>/toggleActive", methods = ['PATCH']) ## TODO: id's that are sanwdiwch must be converted to string
def toggleActive(duid):
    handler = UserHandler()
    if request.method == 'PATCH':
        return handler.toggleDashUserActive(duid)

@app.route("/users/<string:duid>/remove", methods = ['PATCH']) ## TODO: id's that are sanwdiwch must be converted to string
def removeUser(duid):
    handler = UserHandler()
    if request.method == 'PATCH':
        return handler.removeDashUser(duid)

@app.route("/users/<string:duid>/permissions",  methods = [ 'GET','PATCH'])
def userPermissions(duid):
    handler = UserHandler()
    if request.method == 'GET':
        return  handler.getUserPermissions(duid)
    if request.method == 'PATCH':
        req = request.json
        handler = UserHandler()
        return  handler.setUserPermissions(duid, req['permissions'])

#Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    