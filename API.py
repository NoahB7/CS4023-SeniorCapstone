import requests
import json

#post
def login(username, password):
    headers = { 'content-type' : 'application/json' }
    data = {'username':username,'password':password}
    response = requests.post( url = 'http://localhost:8081/login', headers=headers , json=data )
    return response


#post
def register(username, password):
    headers = { 'content-type' : 'application/json' }
    data = {'username':username,'password':password}
    response = requests.post( url = 'http://localhost:8081/register', headers=headers , json=data )
    return response

#post
def getAllWorkoutsForUserId(userId):
    headers = { 'content-type' : 'application/json' }
    data = {'userId':userId}
    response = requests.post( url = 'http://localhost:8081/getAllWorkoutsForUserId', headers=headers , json=data )
    return response


#post
#                ( int , int , python timestamp(in string form) , <- , int , int , int )
#example data input (1,1,'2022-04-04T12:11:54','2022-04-04T14:43:34',20,30,30)
#workout id isnt actually important input but the API call requires it, in database its auto generated
def createWorkout(workoutId, userId, workoutStartTime, workoutEndTime, pushups, situps, squats):
    headers = { 'content-type' : 'application/json' }
    workout = {'workoutId':workoutId,'userId':userId,'workoutStartTime':workoutStartTime,'workoutEndTime':workoutEndTime,'pushups':pushups,'situps':situps,'squats':squats}
    data = json.dumps({'workout':workout})
    response = requests.post( url = 'http://localhost:8081/createWorkout', headers=headers , data=data )
    return response


#get
def getUser():
    headers = { 'content-type' : 'application/json' }
    response = requests.get( url = 'http://localhost:8081/getUser', headers=headers )
    return response

