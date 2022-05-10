import requests
import json
import time
from datetime import datetime
import random

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


for i in range(20):
    register('user'+str((i+100)),'pass'+str((i+100)))

userId = 0
for i in range(100):
    if i %5==0:
        userId += 1

    workoutId = i+100

    seed = random.randrange(3000,4200,1)
    seed1 = random.randrange(86400,864000)

    workoutStartTime = datetime.fromtimestamp(int(time.time())-seed1)
    split = str(workoutStartTime).split(' ')
    workoutStartTime = split[0] + 'T' + split[1]

    workoutEndTime = datetime.fromtimestamp(int(time.time())-seed1+seed)
    split = str(workoutEndTime).split(' ')
    workoutEndTime = split[0] + 'T' + split[1]

    pushups = random.randrange(1,100, 1)
    situps = random.randrange(20,200,1)
    squats = random.randrange(10,150,1)

    createWorkout(workoutId,userId,workoutStartTime,workoutEndTime,pushups,situps,squats)


