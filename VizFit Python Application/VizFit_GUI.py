from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import VizFit_API as api
import mediapipe as mp
import numpy as np
import webbrowser
import datetime
import math
import sys
import cv2



class CreateWireframeER():
    #Based on Source: https://www.youtube.com/watch?v=5kaX3ta398w&t=1127s
    #Edited by Alana Matheny and Sasha Lawson
    
    def __init__(self, mode=False, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
 
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
 
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList   


class ExercisesER():
    def drawSquatsPoints(self, pointsList, counters, durations, img):
        try:
            # Points #
            # Head 
            x0, y0 = pointsList[0][1:]

            # Left Side
            x11, y11 = pointsList[11][1:]
            x13, y13 = pointsList[13][1:]
            x15, y15 = pointsList[15][1:] 
            x23, y23 = pointsList[23][1:]
            x25, y25 = pointsList[25][1:]
            x27, y27 = pointsList[27][1:]
            x29, y29 = pointsList[29][1:]
            x31, y31 = pointsList[31][1:]
            
            # Right Side
            x12, y12 = pointsList[12][1:]
            x14, y14 = pointsList[14][1:]
            x16, y16 = pointsList[16][1:] 
            x24, y24 = pointsList[24][1:]
            x26, y26 = pointsList[26][1:]
            x28, y28 = pointsList[28][1:]
            x30, y30 = pointsList[30][1:]
            x32, y32 = pointsList[32][1:]
            
            
            # Standing and Arms Out Determination #
            isStandingCalculation = y27/y0
            leftArmOut = y23/y15
            rightArmOut = y24/y16

            if (isStandingCalculation > 2 and isStandingCalculation > 0) and (leftArmOut >= 1 and rightArmOut >= 1):
                # Angles #
                if x23-x11 == 0:
                    x11 = x11+.001
                if x24-x12 == 0:
                    x12 = x12+.001
                if x27-x25 == 0:
                    x25 = x25+.001
                if x28-x26 == 0:
                    x26 = x26+.001
                if x27-x11 == 0:
                    x11 = x11+.001
                if x28-x12 == 0:
                    x12 = x12+.001
                
                
                # Angles at the Knee
                leftKneeAngle = math.degrees(math.atan2(y23 - y25, x23 - x25) - math.atan2(y27 - y25, x27 - x25))
                if leftKneeAngle < 0:
                    leftKneeAngle += 360
                    
                rightKneeAngle = math.degrees(math.atan2(y24 - y26, x24 - x26) - math.atan2(y28 - y26, x28 - x26))
                if rightKneeAngle < 0:
                    rightKneeAngle += 360

                # Angles at the Shoulder
                leftShoulderAngle = math.degrees(math.atan2(y13 - y11, x13 - x11) - math.atan2(y23 - y11, x23 - x11))
                if leftShoulderAngle < 0:
                    leftShoulderAngle += 360
                    
                rightShoulderAngle = math.degrees(math.atan2(y14 - y12, x14 - x12) - math.atan2(y24 - y12, x24 - x12))
                if rightShoulderAngle < 0:
                    rightShoulderAngle += 360


                # Determining 0-100 Percentage Value #
                # Knee Percentage
                leftKneePercentLF = np.interp(leftKneeAngle, (170,250),(0,100))
                rightKneePercentLF = np.interp(rightKneeAngle, (170,250),(0,100))

                leftKneePercentRF = np.interp(leftKneeAngle, (80,160),(100,0))
                rightKneePercentRF = np.interp(rightKneeAngle, (80,160),(100,0))

                
                # Average Percentages
                averagePercentLF = (leftKneePercentLF+rightKneePercentLF)/2
                averagePercentRF = (leftKneePercentRF+rightKneePercentRF)/2
                
                #print(averagePercent)
                # Adding to Squats Counter #
                if averagePercentLF == 100:
                    if durations[0] == 0:
                        counters[0] += 0.5
                        durations[0] = 1
                        
                if averagePercentLF <= 50:
                    if durations[0] == 1:
                        counters[0] += 0.5
                        durations[0] = 0

                if averagePercentRF == 100:
                    if durations[1] == 0:
                        counters[0] += 0.5
                        durations[1] = 1
                            
                if averagePercentRF <= 50:
                    if durations[1] == 1:
                        counters[0] += 0.5
                        durations[1] = 0


            # Draw to Image #
            # Left Side
            cv2.circle(img, (x11, y11), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x13, y13), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x15, y15), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x23, y23), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x25, y25), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x27, y27), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x29, y29), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x31, y31), 10, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (x11, y11), (x13, y13), (255, 255, 255), 3)
            cv2.line(img, (x13, y13), (x15, y15), (255, 255, 255), 3) 
            cv2.line(img, (x11, y11), (x23, y23), (255, 255, 255), 3) 
            cv2.line(img, (x23, y23), (x25, y25), (255, 255, 255), 3)
            cv2.line(img, (x25, y25), (x27, y27), (255, 255, 255), 3)
            cv2.line(img, (x27, y27), (x29, y29), (255, 255, 255), 3)
            cv2.line(img, (x27, y27), (x31, y31), (255, 255, 255), 3)
            cv2.line(img, (x29, y29), (x31, y31), (255, 255, 255), 3)

            # Right Side
            cv2.circle(img, (x12, y12), 10, (0, 0, 255), cv2.FILLED)      
            cv2.circle(img, (x14, y14), 10, (0, 0, 255), cv2.FILLED)       
            cv2.circle(img, (x16, y16), 10, (0, 0, 255), cv2.FILLED)           
            cv2.circle(img, (x24, y24), 10, (0, 0, 255), cv2.FILLED)           
            cv2.circle(img, (x26, y26), 10, (0, 0, 255), cv2.FILLED) 
            cv2.circle(img, (x28, y28), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x30, y30), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x32, y32), 10, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (x12, y12), (x14, y14), (255, 255, 255), 3)
            cv2.line(img, (x14, y14), (x16, y16), (255, 255, 255), 3) 
            cv2.line(img, (x12, y12), (x24, y24), (255, 255, 255), 3) 
            cv2.line(img, (x24, y24), (x26, y26), (255, 255, 255), 3)
            cv2.line(img, (x26, y26), (x28, y28), (255, 255, 255), 3)
            cv2.line(img, (x28, y28), (x30, y30), (255, 255, 255), 3)
            cv2.line(img, (x28, y28), (x32, y32), (255, 255, 255), 3)
            cv2.line(img, (x30, y30), (x32, y32), (255, 255, 255), 3)


            return counters
        except:
            doNothing = 0

    def drawPushUpsPoints(self, pointsList, counters, durations, img):
        try:
            # Points #
            # Head 
            x0, y0 = pointsList[0][1:]

            # Left Side
            x11, y11 = pointsList[11][1:]
            x13, y13 = pointsList[13][1:]
            x15, y15 = pointsList[15][1:]
            x23, y23 = pointsList[23][1:]
            x25, y25 = pointsList[25][1:]
            x27, y27 = pointsList[27][1:]
            x29, y29 = pointsList[29][1:]
            x31, y31 = pointsList[31][1:]
            
            # Right Side
            x12, y12 = pointsList[12][1:]
            x14, y14 = pointsList[14][1:]
            x16, y16 = pointsList[16][1:]
            x24, y24 = pointsList[24][1:]
            x26, y26 = pointsList[26][1:]
            x28, y28 = pointsList[28][1:]
            x30, y30 = pointsList[30][1:]
            x32, y32 = pointsList[32][1:]


            # Standing Determination #
            isStandingCalculation = y27/y0

            if isStandingCalculation <= 2 and isStandingCalculation > 0:
                if y15 > y0 and y16 > y0:
                    # Angles #
                    if x27-x11 == 0:
                        x11 = x11+.001
                    if x28-x12 == 0:
                        x12 = x12+.001
                    if x13-x11 == 0:
                        x11 = x11+.001
                    if x14-x12 == 0:
                        x12 = x12+.001
                    
                    # Angles at the Elbow
                    leftElbowAngle = math.degrees(math.atan2(y15 - y13, x15 - x13) - math.atan2(y11 - y13, x11 - x13))
                    if leftElbowAngle < 0:
                        leftElbowAngle += 360

                    rightElbowAngle = math.degrees(math.atan2(y16 - y14, x16 - x14) - math.atan2(y12 - y14, x12 - x14))
                    if rightElbowAngle < 0:
                        rightElbowAngle += 360
                    
                    # Angles Produced by the Full Body
                    leftSideAngle = math.degrees(math.atan2(y11 - y25, x11 - x25) - math.atan2(y27 - y25, x27 - x25))
                    if leftSideAngle < 0:
                        leftSideAngle += 360

                    rightSideAngle = math.degrees(math.atan2(y12 - y26, x12 - x26) - math.atan2(y28 - y26, x28 - x26))
                    if rightSideAngle < 0:
                        rightSideAngle += 360
                        

                    # Determining 0-100 Percentage Value #
                    # Knee Percentage
                    leftElbowPercentLF = np.interp(leftElbowAngle, (200,270),(0,100))
                    rightElbowPercentLF = np.interp(rightElbowAngle, (200,270),(0,100))

                    leftElbowPercentRF = np.interp(leftElbowAngle, (60,130),(100,0))
                    rightElbowPercentRF = np.interp(rightElbowAngle, (60,130),(100,0))
                    
                    # Full Body Percentage 
                    leftSidePercentLF = np.interp(leftSideAngle, (60,180),(0,100))
                    rightSidePercentLF = np.interp(rightSideAngle, (60,180),(0,100))

                    leftSidePercentRF = np.interp(leftSideAngle, (80,160),(0,100))
                    rightSidePercentRF = np.interp(rightSideAngle, (80,160),(0,100))

                    # Average Percentages
                    averagePercentLF = (leftElbowPercentLF+rightElbowPercentLF+leftSidePercentLF+rightSidePercentLF)/4
                    averagePercentRF = (leftElbowPercentRF+rightElbowPercentRF+leftSidePercentRF+rightSidePercentRF)/4
                    

                    # Adding to Push-Up Counter #
                    if averagePercentLF == 100:
                        if durations[3] == 0:
                            counters[1] += 0.5
                            durations[3] = 1
                            counters[3] = 1
                                
                    if averagePercentLF <= 50:
                        if durations[3] == 1:
                            counters[1] += 0.5
                            durations[3] = 0
                            counters[3] = 1
                            
                    if averagePercentRF == 100:
                        if durations[2] == 0:
                            counters[1] += 0.5
                            durations[2] = 1
                            counters[3] = 1
                                
                    if averagePercentRF <= 50:
                        if durations[2] == 1:
                            counters[1] += 0.5
                            durations[2] = 0
                            counters[3] = 1
                    

            # Draw to Image #
            # Left Side 
            cv2.circle(img, (x11, y11), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x13, y13), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x15, y15), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x23, y23), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x25, y25), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x27, y27), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x29, y29), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x31, y31), 10, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (x11, y11), (x13, y13), (255, 255, 255), 3)
            cv2.line(img, (x13, y13), (x15, y15), (255, 255, 255), 3) 
            cv2.line(img, (x11, y11), (x23, y23), (255, 255, 255), 3) 
            cv2.line(img, (x23, y23), (x25, y25), (255, 255, 255), 3)
            cv2.line(img, (x25, y25), (x27, y27), (255, 255, 255), 3)
            cv2.line(img, (x27, y27), (x29, y29), (255, 255, 255), 3)
            cv2.line(img, (x27, y27), (x31, y31), (255, 255, 255), 3)
            cv2.line(img, (x29, y29), (x31, y31), (255, 255, 255), 3)
            
            # Right Side
            cv2.circle(img, (x12, y12), 10, (0, 0, 255), cv2.FILLED)      
            cv2.circle(img, (x14, y14), 10, (0, 0, 255), cv2.FILLED)       
            cv2.circle(img, (x16, y16), 10, (0, 0, 255), cv2.FILLED)           
            cv2.circle(img, (x24, y24), 10, (0, 0, 255), cv2.FILLED)           
            cv2.circle(img, (x26, y26), 10, (0, 0, 255), cv2.FILLED) 
            cv2.circle(img, (x28, y28), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x30, y30), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x32, y32), 10, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (x12, y12), (x14, y14), (255, 255, 255), 3)
            cv2.line(img, (x14, y14), (x16, y16), (255, 255, 255), 3) 
            cv2.line(img, (x12, y12), (x24, y24), (255, 255, 255), 3) 
            cv2.line(img, (x24, y24), (x26, y26), (255, 255, 255), 3)
            cv2.line(img, (x26, y26), (x28, y28), (255, 255, 255), 3)
            cv2.line(img, (x28, y28), (x30, y30), (255, 255, 255), 3)
            cv2.line(img, (x28, y28), (x32, y32), (255, 255, 255), 3)
            cv2.line(img, (x30, y30), (x32, y32), (255, 255, 255), 3)


            return counters
        except:
            doNothing = 0
             
    def drawSitUpsPoints(self, pointsList, counters, durations, img):
        try:
            goodSU = 1
            
            # Points #
            # Head 
            x0, y0 = pointsList[0][1:]

            # Left Side
            x11, y11 = pointsList[11][1:]
            x13, y13 = pointsList[13][1:]
            x15, y15 = pointsList[15][1:] 
            x23, y23 = pointsList[23][1:] 
            x25, y25 = pointsList[25][1:] 
            x27, y27 = pointsList[27][1:]
            x29, y29 = pointsList[29][1:]
            x31, y31 = pointsList[31][1:]
            
            # Right Side
            x12, y12 = pointsList[12][1:]
            x14, y14 = pointsList[14][1:]
            x16, y16 = pointsList[16][1:] 
            x24, y24 = pointsList[24][1:] 
            x26, y26 = pointsList[26][1:] 
            x28, y28 = pointsList[28][1:]
            x30, y30 = pointsList[30][1:]
            x32, y32 = pointsList[32][1:]
            

            # Standing Determination #
            isStandingCalculation = y27/y0

            if isStandingCalculation <= 2 and isStandingCalculation > 0:
                if y24 > y26 and y23 > y25:
                    # Angles #
                    if x23-x11 == 0:
                        x11 = x11+.001
                    if x24-x12 == 0:
                        x12 = x12+.001
                        
                    if x25-x23 == 0:
                        x23 = x23+.001
                    if x26-x24 == 0:
                        x24 = x24+.001
                    

                    pastL = (y23-y11)/(x23-x11) #Shoulder to hip slope L
                    backStrightL = abs(pastL)
                    pastR = (y24-y12)/(x24-x12) #Shoulder to hip slope R
                    backStrightR = abs(pastR)
                    
                    legsNotStrightL = abs((y25-y23)/(x25-x23)) #hip to knee slope L
                    legsNotStrightR = abs((y26-y24)/(x26-x24)) #hip to knee slope R
                    

                    # Angles Produced by the Full Body
                    leftSideAngle = math.degrees(math.atan2(y11 - y23, x11 - x23) - math.atan2(y25 - y23, x25 - x23))
                    if leftSideAngle < 0:
                        leftSideAngle += 360

                    rightSideAngle = math.degrees(math.atan2(y12 - y24, x12 - x24) - math.atan2(y26 - y24, x26 - x24))
                    if rightSideAngle < 0:
                        rightSideAngle += 360

                    
                    # Angles at the Knee
                    leftKneeAngle = math.degrees(math.atan2(y23 - y25, x23 - x25) - math.atan2(y27 - y25, x27 - x25))
                    if leftKneeAngle < 0:
                        leftKneeAngle += 360

                    rightKneeAngle = math.degrees(math.atan2(y24 - y26, x24 - x26) - math.atan2(y28 - y26, x28 - x26))
                    if rightKneeAngle < 0:
                        rightKneeAngle += 360
                
                    if backStrightL > 2 or backStrightR > 2:
                        goodSU = 0
                    
                    if legsNotStrightL < .05 or legsNotStrightR < .05:
                        goodSU = 0
                    
                    
                    # Determining 0-100 Percentage Value #
                    # Body Percentage
                    leftSidePercentLF = np.interp(leftSideAngle, (80,140),(100,0))
                    rightSidePercentLF = np.interp(rightSideAngle, (80,140),(100,0))

                    leftSidePercentRF = np.interp(leftSideAngle, (210,270),(0,100))
                    rightSidePercentRF = np.interp(rightSideAngle, (210,270),(0,100))

                    # Knee Percentage
                    leftKneePercentLF = np.interp(leftKneeAngle, (250,260),(0,100))
                    rightKneePercentLF = np.interp(rightKneeAngle, (250,260),(0,100))
                    
                    leftKneePercentRF = np.interp(leftKneeAngle, (80,90),(100,0))
                    rightKneePercentRF = np.interp(rightKneeAngle, (80,90),(100,0))
                    

                    # Average Percentages
                    averagePercentLF = (leftSidePercentLF+rightSidePercentLF+leftKneePercentLF+rightKneePercentLF)/4
                    averagePercentRF = (leftSidePercentRF+rightSidePercentRF+leftKneePercentRF+rightKneePercentRF)/4
                    

                    
                    # Adding to Sit-Up Counter #
                    if averagePercentLF == 100:
                        if durations[4] == 0:
                            if goodSU == 1: 
                                counters[2] += 0.5
                                durations[4] = 1
                            counters[3] = 2
                                
                    if averagePercentLF <= 65: #Increase to 65 to account for more sensitive angles 
                        if durations[4] == 1:
                            if goodSU == 1: 
                                counters[2] += 0.5
                                durations[4] = 0
                            counters[3] = 2

                    if averagePercentRF == 100:
                        if durations[5] == 0:
                            if goodSU == 1: 
                                counters[2] += 0.5
                                durations[5] = 1
                            counters[3] = 2
                                
                    if averagePercentRF <= 65: #Increase to 65 to account for more sensitive angles 
                        if durations[5] == 1:
                            if goodSU == 1: 
                                counters[2] += 0.5
                                durations[5] = 0
                            counters[3] = 2


            # Draw to Image #
            # Left Side
            cv2.circle(img, (x11, y11), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x13, y13), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x15, y15), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x23, y23), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x25, y25), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x27, y27), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x29, y29), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x31, y31), 10, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (x11, y11), (x13, y13), (255, 255, 255), 3)
            cv2.line(img, (x13, y13), (x15, y15), (255, 255, 255), 3) 
            cv2.line(img, (x11, y11), (x23, y23), (255, 255, 255), 3) 
            cv2.line(img, (x23, y23), (x25, y25), (255, 255, 255), 3)
            cv2.line(img, (x25, y25), (x27, y27), (255, 255, 255), 3)
            cv2.line(img, (x27, y27), (x29, y29), (255, 255, 255), 3)
            cv2.line(img, (x27, y27), (x31, y31), (255, 255, 255), 3)
            cv2.line(img, (x29, y29), (x31, y31), (255, 255, 255), 3)

            # Right Side
            cv2.circle(img, (x12, y12), 10, (0, 0, 255), cv2.FILLED)      
            cv2.circle(img, (x14, y14), 10, (0, 0, 255), cv2.FILLED)       
            cv2.circle(img, (x16, y16), 10, (0, 0, 255), cv2.FILLED)           
            cv2.circle(img, (x24, y24), 10, (0, 0, 255), cv2.FILLED)           
            cv2.circle(img, (x26, y26), 10, (0, 0, 255), cv2.FILLED) 
            cv2.circle(img, (x28, y28), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x30, y30), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x32, y32), 10, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (x12, y12), (x14, y14), (255, 255, 255), 3)
            cv2.line(img, (x14, y14), (x16, y16), (255, 255, 255), 3) 
            cv2.line(img, (x12, y12), (x24, y24), (255, 255, 255), 3) 
            cv2.line(img, (x24, y24), (x26, y26), (255, 255, 255), 3)
            cv2.line(img, (x26, y26), (x28, y28), (255, 255, 255), 3)
            cv2.line(img, (x28, y28), (x30, y30), (255, 255, 255), 3)
            cv2.line(img, (x28, y28), (x32, y32), (255, 255, 255), 3)
            cv2.line(img, (x30, y30), (x32, y32), (255, 255, 255), 3)
            

            return counters
        except:
            doNothing = 0
            
    def isInFrame(self, pointsList, img):
        try:
            imgY, imgX, imgC = img.shape
            countL = 0
            countR = 0
            
            # Points #
            # Left Side
            x11, y11 = pointsList[11][1:] #xy of l shoulder
            x13, y13 = pointsList[13][1:] #xy of l elbow
            x23, y23 = pointsList[23][1:] #xy of l hip
            x25, y25 = pointsList[25][1:] #xy of l knee
            x27, y27 = pointsList[27][1:] #xy of l foot
            
            if x11 > imgX or y11 > imgY:
                countL = countL+1
            
            if x13 > imgX or y13 > imgY:
                countL = countL+1
            
            if x23 > imgX or y23 > imgY:
                countL = countL+1
            
            if x25 > imgX or y25 > imgY:
                countL = countL+1
            
            if x27 > imgX or y27 > imgY:
                countL = countL+1
            
            # Right Side
            x12, y12 = pointsList[12][1:] #xy of r shoulder
            x14, y14 = pointsList[14][1:] #xy of r elbow
            x24, y24 = pointsList[24][1:] #xy of r hip
            x26, y26 = pointsList[26][1:] #xy of r knee
            x28, y28 = pointsList[28][1:] #xy of r foot
            
            if x12 > imgX or y12 > imgY:
                countR = countR+1
            
            if x14 > imgX or y14 > imgY:
                countR = countR+1
            
            if x24 > imgX or y24 > imgY:
                countR = countR+1
            
            if x26 > imgX or y26 > imgY:
                countR = countR+1
            
            if x28 > imgX or y28 > imgY:
                countR = countR+1
            
            
            if countL > 1 or countR > 1:
                return False
            

            return True
        except:
            doNothing = 0


def runExerciseRecogination():
    successfullyHidden = False
    cap = cv2.VideoCapture(-1)
    #cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    wireframe = CreateWireframeER()
    exercise = ExercisesER()

    global counters
    counters = [0,0,0,0]
    durations = [0,0,0,0,0,0]

    countersPrev = [0,0,0]

    squatsGoodCount = 0
    pushUpsGoodCount = 0
    sitUpsGoodCount = 0

    currentDT = datetime.datetime.now()
    global startTime
    startTime = currentDT.strftime("%Y-%m-%dT%H:%M:%S")

    while True:
        img = cap.read()[1]
        newSize = (1200, 800)
        img = cv2.resize(img, newSize)
        img = wireframe.findPose(img, False)
        pointList = wireframe.findPosition(img, False)

        rectangleColor =  (67, 67, 67)
        textColor = (255, 255, 255)
        textSize = 1.5

        if exercise.isInFrame(pointList, img) == True:
        
            countersPrev[0] = counters[0]
            countersPrev[1] = counters[1]
            countersPrev[2] = counters[2]
        
            # Determine Exercise #
            exercise.drawSquatsPoints(pointList, counters, durations, img)
            exercise.drawPushUpsPoints(pointList, counters, durations, img)
            exercise.drawSitUpsPoints(pointList, counters, durations, img)
     
            
            # Feedback #
            if counters[3] == 0:
                squatsGoodCount = squatsGoodCount+(counters[0]-countersPrev[0])
                    
                cv2.rectangle(img, (730, 265), (1265, 0), rectangleColor, cv2.FILLED)
                cv2.rectangle(img, (730, 265), (1265, 0), rectangleColor)
                cv2.putText(img, (str("Squat Form:")), (845, 35), cv2.FONT_HERSHEY_PLAIN, 2, textColor, 1)
                cv2.putText(img, (str("1) Stand with your side to the camera")), (740, 65), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("2) Back straight")), (740, 95), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("3) Knees in line with your toes")), (740, 125), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("4) Both arms perpendicular to you")), (740, 155), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("5) Feet spread shoulder width apart")), (740, 185), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("6) Thighs/hips parallel to floor")), (740, 215), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("7) Do not squat too far down")), (740, 245), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                    
            if counters[3] == 1:
                pushUpsGoodCount = pushUpsGoodCount+(counters[1]-countersPrev[1])
                    
                cv2.rectangle(img, (730, 265), (1265, 0), rectangleColor, cv2.FILLED)
                cv2.rectangle(img, (730, 265), (1265, 0), rectangleColor)
                cv2.putText(img, (str("Push-Up Form:")), (845, 35), cv2.FONT_HERSHEY_PLAIN, 2, textColor, 1)
                cv2.putText(img, (str("1) Lie on stomach in a straight line")), (740, 65), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("2) Do not lock your elbows")), (740, 95), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("3) Hands next to your chest")), (740, 125), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("4) Push up with your arms")), (740, 155), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("5) Elbows close to your sides")), (740, 185), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("6) Head straight")), (740, 215), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("7) Feet together")), (740, 245), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                            
            if counters[3] == 2:
                sitUpsGoodCount = sitUpsGoodCount+(counters[2]-countersPrev[2])
                    
                cv2.rectangle(img, (730, 265), (1265, 0), rectangleColor, cv2.FILLED)
                cv2.rectangle(img, (730, 265), (1265, 0), rectangleColor)
                cv2.putText(img, (str("Sit-Up Form:")), (865, 35), cv2.FONT_HERSHEY_PLAIN, 2, textColor, 1)
                cv2.putText(img, (str("1) Lie down on your back")), (740, 65), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("2) Bend your knees")), (740, 95), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)                
                cv2.putText(img, (str("3) Hands on chest or behind head")), (740, 125), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("4) Exhale on the sit up")), (740, 155), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("5) Sit up slowly")), (740, 185), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("6) Do your sit up in one motion")), (740, 215), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                cv2.putText(img, (str("7) Do not sit up too far")), (740, 245), cv2.FONT_HERSHEY_PLAIN, textSize, textColor, 1)
                
        else:
            cv2.rectangle(img, (655, 720), (0, 595), (0,0,250), cv2.FILLED)
            cv2.putText(img, (str("Make sure you are in frame!")), (20, 670), cv2.FONT_HERSHEY_PLAIN, 2.5, (0, 0, 0), 2)


        # Display Counters #
        cv2.rectangle(img, (0, 0), (143, 265), rectangleColor, cv2.FILLED)
        cv2.rectangle(img, (0, 0), (143, 265), rectangleColor)
        
        if int(counters[1]) < 10: 
            cv2.putText(img, (str(int(counters[1]))), (55, 45), cv2.FONT_HERSHEY_PLAIN, 3, textColor, 4)
        else:
            cv2.putText(img, (str(int(counters[1]))), (40, 45), cv2.FONT_HERSHEY_PLAIN, 3, textColor, 4)
        cv2.putText(img, (str("Push-Ups")), (10, 70), cv2.FONT_HERSHEY_PLAIN, 1.5, textColor, 2)

        if int(counters[2]) < 10: 
            cv2.putText(img, (str(int(counters[2]))), (55, 130), cv2.FONT_HERSHEY_PLAIN, 3, textColor, 4)
        else:
            cv2.putText(img, (str(int(counters[2]))), (40, 130), cv2.FONT_HERSHEY_PLAIN, 3, textColor, 4)
        cv2.putText(img, (str("Sit-Ups")), (25, 155), cv2.FONT_HERSHEY_PLAIN, 1.5, textColor, 2)

        if int(counters[0]) < 10: 
            cv2.putText(img, (str(int(counters[0]))), (55, 215), cv2.FONT_HERSHEY_PLAIN, 3, textColor, 4)
        else:
            cv2.putText(img, (str(int(counters[0]))), (40, 215), cv2.FONT_HERSHEY_PLAIN, 3, textColor, 4)
        cv2.putText(img, (str("Squats")), (30, 240), cv2.FONT_HERSHEY_PLAIN, 1.5, textColor, 2)
        

        cv2.imshow("VizFit Exercise Webcam", img)
        cv2.resizeWindow("VizFit Exercise Webcam",newSize)


        if successfullyHidden == False:
            if cv2.getWindowProperty("VizFit Exercise Webcam", cv2.WND_PROP_VISIBLE) >= 1:
                widget.hide()
                successfullyHidden = True

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.getWindowProperty("VizFit Exercise Webcam", cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()
    cap.release()

    currentDT = datetime.datetime.now()
    global endTime
    endTime = currentDT.strftime("%Y-%m-%dT%H:%M:%S")


class HomeWindow(QDialog):
    def __init__(self):
        super(HomeWindow, self).__init__()
        loadUi("HomeWindowImproved.ui", self)

        logo = QPixmap('logo4.png')
        self.logo.setPixmap(logo)

        self.passwordEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.loginButton.clicked.connect(self.verifyLogin)
        self.registerButton.clicked.connect(self.goToRegisterWindow)

    def verifyLogin(self):
        username = self.usernameEntry.text()
        password = self.passwordEntry.text()

        if (username == "" and password == ""):
            self.output.setText("Please enter your username and password.")
            self.output.setStyleSheet('font: 75 12pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
        elif (username == ""):
            self.output.setText("Please enter your username.")
            self.output.setStyleSheet('font: 75 12pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
        elif (password == ""):
            self.output.setText("Please enter your password.")
            self.output.setStyleSheet('font: 75 12pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
        else: 
            hasError = False
            global returnedUserId

            try:
                response = api.login(username,password).json()
                returnedUsername = str(response["username"])
                returnedPassword = str(response["password"])
                returnedUserId = str(response["userId"])
            except:
                returnedUsername = "None"
                returnedPassword = "None"
                returnedUserId = -1
                hasError = True

            if hasError == False:
                if returnedUsername != "None" and returnedPassword != "None":
                    self.goToWelcomeWindow()
                else:
                    self.output.setText("Your username or password is incorrect. Try again!")
                    self.output.setStyleSheet('font: 75 12pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
            else:
                self.output.setText("A server error has occured. Try again later.")
                self.output.setStyleSheet('font: 75 12pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')

    def goToWelcomeWindow(self):
        global welcome
        welcome = WelcomeWindow()

        try:
            widget.removeWidget(home)
        except:
            widget.removeWidget(homeInit)

        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToRegisterWindow(self):
        global register
        register = RegisterWindow()

        try:
            widget.removeWidget(home)
        except:
            widget.removeWidget(homeInit)

        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex()+1)


class RegisterWindow(QDialog):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        loadUi("RegisterWindow.ui", self)

        logo = QPixmap('logo4.png')
        self.logo.setPixmap(logo)
        
        self.passwordEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPasswordEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        
        global registrationSuccessful
        registrationSuccessful = False

        self.registerButton.clicked.connect(self.verifyRegisteration)
        self.homeButton.clicked.connect(self.goToHomeWindow)

    def verifyRegisteration(self):
        username = self.usernameEntry.text()
        password = self.passwordEntry.text()
        confirmPassword = self.confirmPasswordEntry.text()

        if (username == "" or password == "" or confirmPassword == ""):
            self.output.setText("Not all fields were entered. Try again!")
            self.output.setStyleSheet('font: 75 12pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
        elif password != confirmPassword:
            self.output.setText("The passwords do not match. Try again!")
            self.output.setStyleSheet('font: 75 12pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
        else:
            global registrationSuccessful
            registrationSuccessful = False
            hasError = False

            try:
                response = api.register(username,password).text
                print(response)
            except:
                response = "-999"
                hasError = True

            if hasError == False:
                if response != "-999":
                    registrationSuccessful = True
                    self.goToHomeWindow()
                else:
                    self.output.setText("That username already exists. Try another!")
                    self.output.setStyleSheet('font: 75 12pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
            else:
                self.output.setText("A server error has occured. Try again later.")
                self.output.setStyleSheet('font: 75 12pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')

    def goToHomeWindow(self):
        global home
        home = HomeWindow()
        
        widget.removeWidget(register)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)

        if registrationSuccessful:
            home.output.setText("Successfully registered!")
            home.output.setStyleSheet('font: 75 15pt "Arial"; color: rgb(106, 168, 79); qproperty-alignment: AlignCenter')


class WelcomeWindow(QDialog):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        loadUi("WelcomeWindow.ui", self)

        logo = QPixmap('logo4.png')
        self.logo.setPixmap(logo)

        self.beginExercisingButton.clicked.connect(self.goToExerciseRecogination)
        self.analyticsButton.clicked.connect(self.goToAnalytics)
        self.logoutButton.clicked.connect(self.goToHomeWindow)

    def goToExerciseRecogination(self):
        widget.removeWidget(welcome)

        runExerciseRecogination()

        widget.show()

        global resultInit
        resultInit = ResultWindow()

        widget.addWidget(resultInit)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToAnalytics(self):
        webbrowser.open("localhost:8080/")

    def goToHomeWindow(self):
        global home
        home = HomeWindow()
        
        widget.removeWidget(welcome)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)


class ResultWindow(QDialog):
    def __init__(self):
        super(ResultWindow, self).__init__()
        loadUi("ResultWindow.ui", self)

        logo = QPixmap('logo4.png')
        self.logo.setPixmap(logo)

        numSquats = math.floor(counters[0])
        numPushups = math.floor(counters[1])
        numSitups = math.floor(counters[2])

        if numSquats == 0 and numPushups == 0 and numSitups == 0:
            self.output.setText("Session not recorded.")
            self.output.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
        else:
            hasError = False

            try:
                response = api.createWorkout(1, returnedUserId, startTime, endTime, numPushups, numSitups, numSquats)
                response = response.status_code
            except:
                response = 500
                hasError = True

            if hasError == False:
                if response == 200:
                    self.output.setText("Session successfully recorded!")
                    self.output.setStyleSheet('font: 75 16pt "Arial"; color: rgb(106, 168, 79); qproperty-alignment: AlignCenter')
                else:
                    self.output.setText("Error! Session not recorded.")
                    self.output.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
            else:
                self.output.setText("Error! Session not recorded.")
                self.output.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')    

        self.pushupsResults.setText(str(numPushups))
        self.pushupsResults.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 255, 255); qproperty-alignment: AlignCenter')

        self.situpsResults.setText(str(numSitups))
        self.situpsResults.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 255, 255); qproperty-alignment: AlignCenter')

        self.squatsResults.setText(str(numSquats))
        self.squatsResults.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 255, 255); qproperty-alignment: AlignCenter')

        self.analyticsButton.clicked.connect(self.goToAnalytics)
        self.beginExercisingButton.clicked.connect(self.goToExerciseRecogination)
        self.logoutButton.clicked.connect(self.goToHomeWindow)

    def goToAnalytics(self):
        webbrowser.open("localhost:8080/")

    def goToExerciseRecogination(self):
        runExerciseRecogination()

        widget.removeWidget(resultInit)

        global result2
        result2 = Result2Window()
        widget.addWidget(result2)
        widget.setCurrentIndex(widget.currentIndex()+1)

        widget.show()

    def goToHomeWindow(self):
        global home
        home = HomeWindow()
        
        widget.removeWidget(resultInit)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Result2Window(QDialog):
    def __init__(self):
        super(Result2Window, self).__init__()
        loadUi("ResultWindow.ui", self)

        logo = QPixmap('logo4.png')
        self.logo.setPixmap(logo)

        numSquats = math.floor(counters[0])
        numPushups = math.floor(counters[1])
        numSitups = math.floor(counters[2])

        if numSquats == 0 and numPushups == 0 and numSitups == 0:
            self.output.setText("Session not recorded.")
            self.output.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
        else:
            hasError = False

            try:
                response = api.createWorkout(1, returnedUserId, startTime, endTime, numPushups, numSitups, numSquats)
                response = response.status_code
            except:
                response = 500
                hasError = True

            if hasError == False:
                if response == 200:
                    self.output.setText("Session successfully recorded!")
                    self.output.setStyleSheet('font: 75 16pt "Arial"; color: rgb(106, 168, 79); qproperty-alignment: AlignCenter')
                else:
                    self.output.setText("Error! Session not recorded.")
                    self.output.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')
            else:
                self.output.setText("Error! Session not recorded.")
                self.output.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 0, 0); qproperty-alignment: AlignCenter')    

        self.pushupsResults.setText(str(numPushups))
        self.pushupsResults.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 255, 255); qproperty-alignment: AlignCenter')

        self.situpsResults.setText(str(numSitups))
        self.situpsResults.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 255, 255); qproperty-alignment: AlignCenter')

        self.squatsResults.setText(str(numSquats))
        self.squatsResults.setStyleSheet('font: 75 16pt "Arial"; color: rgb(255, 255, 255); qproperty-alignment: AlignCenter')

        self.analyticsButton.clicked.connect(self.goToAnalytics)
        self.beginExercisingButton.clicked.connect(self.goToExerciseRecogination)
        self.logoutButton.clicked.connect(self.goToHomeWindow)

    def goToAnalytics(self):
        webbrowser.open("localhost:8080/")

    def goToExerciseRecogination(self):
        runExerciseRecogination()

        widget.removeWidget(result2)

        global resultInit
        resultInit = ResultWindow()
        widget.addWidget(resultInit)
        widget.setCurrentIndex(widget.currentIndex()+1)

        widget.show()

    def goToHomeWindow(self):
        global home
        home = HomeWindow()
        
        widget.removeWidget(result2)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)



app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
homeInit = HomeWindow()

widget.addWidget(homeInit)

widget.setWindowTitle("VizFit Exercise Application")
widget.setFixedWidth(700)
widget.setFixedHeight(510)

widget.show()

try:
    sys.exit(app.exec_())
except:
    doNothing = 0