import mediapipe as mp
import numpy as np
import math
import cv2

class CreateWireframe():
    #Based on Source: https://www.youtube.com/watch?v=5kaX3ta398w&t=1127s

    def __init__(self, mode=False, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
 
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)
 
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
 
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList    

class Exercises():
    def drawSquatsPoints(self, pointsList, counters, durations, img):
        try:
            # Points #
            # Left Side
            x11, y11 = pointsList[11][1:]
            x13, y13 = pointsList[13][1:]
            x23, y23 = pointsList[23][1:]
            x25, y25 = pointsList[25][1:]
            x27, y27 = pointsList[27][1:]

            # Right Side
            x12, y12 = pointsList[12][1:]
            x14, y14 = pointsList[14][1:]
            x24, y24 = pointsList[24][1:]
            x26, y26 = pointsList[26][1:]
            x28, y28 = pointsList[28][1:]
            
            
            # Angles #
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

            # Shoulder Percentage
            leftShoulderPercentLF = np.interp(leftShoulderAngle, (0,70),(0,100))
            rightShoulderPercentLF = np.interp(rightShoulderAngle, (0,70),(0,100))

            leftShoulderPercentRF = np.interp(leftShoulderAngle, (270,350),(100,0))
            rightShoulderPercentRF = np.interp(rightShoulderAngle, (270,350),(100,0))
            
            # Average Percentages
            averagePercentLF = (leftKneePercentLF+rightKneePercentLF+leftShoulderPercentLF+rightShoulderPercentLF)/4
            averagePercentRF = (leftKneePercentRF+rightKneePercentRF+leftShoulderPercentRF+rightShoulderPercentRF)/4
            

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
            cv2.circle(img, (x23, y23), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x25, y25), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x27, y27), 10, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (x11, y11), (x13, y13), (255, 255, 255), 3)
            cv2.line(img, (x11, y11), (x23, y23), (255, 255, 255), 3)
            cv2.line(img, (x23, y23), (x25, y25), (255, 255, 255), 3)
            cv2.line(img, (x25, y25), (x27, y27), (255, 255, 255), 3)

            cv2.putText(img, str(int(leftShoulderAngle)), (x11 - 50, y11 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
            cv2.putText(img, str(int(leftKneeAngle)), (x25 - 50, y25 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)

            # Right Side
            cv2.circle(img, (x12, y12), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x14, y14), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x24, y24), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x26, y26), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x28, y28), 10, (0, 0, 255), cv2.FILLED)
            
            cv2.line(img, (x12, y12), (x14, y14), (255, 255, 255), 3)
            cv2.line(img, (x12, y12), (x24, y24), (255, 255, 255), 3)
            cv2.line(img, (x24, y24), (x26, y26), (255, 255, 255), 3)
            cv2.line(img, (x26, y26), (x28, y28), (255, 255, 255), 3) 

            cv2.putText(img, str(int(rightShoulderAngle)), (x12 - 50, y12 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
            cv2.putText(img, str(int(rightKneeAngle)), (x26 - 50, y26 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)

            # Average Percentage & Counter #
            #cv2.putText(img, (str(int(averagePercentRF)) + "%"), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            #cv2.putText(img, (str(int(averagePercentLF)) + "%"), (500, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            #cv2.putText(img, (str(int(counters[0]))), (700, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)


            return counters
        except:
            #print("ERROR!")
            doNothing = 0

    def drawPushUpsPoints(self, pointsList, counters, durations, img):
        try:
            # Points #
            # Left Side
            x11, y11 = pointsList[11][1:]
            x13, y13 = pointsList[13][1:]
            x15, y15 = pointsList[15][1:]
            x23, y23 = pointsList[23][1:]
            x25, y25 = pointsList[25][1:]
            x27, y27 = pointsList[27][1:]
            
            # Right Side
            x12, y12 = pointsList[12][1:]
            x14, y14 = pointsList[14][1:]
            x16, y16 = pointsList[16][1:]
            x24, y24 = pointsList[24][1:]
            x26, y26 = pointsList[26][1:]
            x28, y28 = pointsList[28][1:]
            

            # Angles #
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
            if averagePercentLF <= 50:
                if durations[3] == 1:
                    counters[1] += 0.5
                    durations[3] = 0

            if averagePercentRF == 100:
                if durations[2] == 0:
                    counters[1] += 0.5
                    durations[2] = 1
            if averagePercentRF <= 50:
                if durations[2] == 1:
                    counters[1] += 0.5
                    durations[2] = 0
                

            # Draw to Image #
            # Left Side 
            cv2.circle(img, (x11, y11), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x13, y13), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x15, y15), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x23, y23), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x25, y25), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x27, y27), 10, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (x11, y11), (x13, y13), (255, 255, 255), 3)
            cv2.line(img, (x13, y13), (x15, y15), (255, 255, 255), 3) 
            cv2.line(img, (x11, y11), (x23, y23), (255, 255, 255), 3) 
            cv2.line(img, (x23, y23), (x25, y25), (255, 255, 255), 3)
            cv2.line(img, (x25, y25), (x27, y27), (255, 255, 255), 3)

            cv2.putText(img, str(int(leftElbowAngle)), (x13 - 50, y13 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
            cv2.putText(img, str(int(leftSideAngle)), (x23 - 50, y23 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
            
            # Right Side
            cv2.circle(img, (x12, y12), 10, (0, 0, 255), cv2.FILLED)      
            cv2.circle(img, (x14, y14), 10, (0, 0, 255), cv2.FILLED)       
            cv2.circle(img, (x16, y16), 10, (0, 0, 255), cv2.FILLED)           
            cv2.circle(img, (x24, y24), 10, (0, 0, 255), cv2.FILLED)           
            cv2.circle(img, (x26, y26), 10, (0, 0, 255), cv2.FILLED) 
            cv2.circle(img, (x28, y28), 10, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (x12, y12), (x14, y14), (255, 255, 255), 3)
            cv2.line(img, (x14, y14), (x16, y16), (255, 255, 255), 3) 
            cv2.line(img, (x12, y12), (x24, y24), (255, 255, 255), 3) 
            cv2.line(img, (x24, y24), (x26, y26), (255, 255, 255), 3)
            cv2.line(img, (x26, y26), (x28, y28), (255, 255, 255), 3)
                
            cv2.putText(img, str(int(rightElbowAngle)), (x14 - 50, y14 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
            cv2.putText(img, str(int(rightSideAngle)), (x24 - 50, y24 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)

            # Average Percentage & Counter #
            #cv2.putText(img, (str(int(averagePercentRF)) + "%"), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            #cv2.putText(img, (str(int(averagePercentLF)) + "%"), (500, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            #cv2.putText(img, (str(int(counters[1]))), (700, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)


            return counters
        except:
            doNothing = 0
             
    def drawSitUpsPoints(self, pointsList, counters, durations, img):
        try:
            # Points #
            # Left Side
            x11, y11 = pointsList[11][1:]
            x23, y23 = pointsList[23][1:]
            x25, y25 = pointsList[25][1:]
            x27, y27 = pointsList[27][1:]

            # Right Side
            x12, y12 = pointsList[12][1:]
            x24, y24 = pointsList[24][1:]
            x26, y26 = pointsList[26][1:]
            x28, y28 = pointsList[28][1:]
            
            
            # Angles #
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
                    counters[2] += 0.5
                    durations[4] = 1
            if averagePercentLF <= 65: #Increase to 65 to account for more sensitive angles 
                if durations[4] == 1:
                    counters[2] += 0.5
                    durations[4] = 0

            if averagePercentRF == 100:
                if durations[5] == 0:
                    counters[2] += 0.5
                    durations[5] = 1
            if averagePercentRF <= 65: #Increase to 65 to account for more sensitive angles 
                if durations[5] == 1:
                    counters[2] += 0.5
                    durations[5] = 0


            # Draw to Image #
            # Left Side
            cv2.circle(img, (x11, y11), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x23, y23), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x25, y25), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x27, y27), 10, (0, 0, 255), cv2.FILLED)

            cv2.line(img, (x11, y11), (x23, y23), (255, 255, 255), 3) 
            cv2.line(img, (x23, y23), (x25, y25), (255, 255, 255), 3)
            cv2.line(img, (x25, y25), (x27, y27), (255, 255, 255), 3)
            
            cv2.putText(img, str(int(leftSideAngle)), (x23 - 50, y23 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
            cv2.putText(img, str(int(leftKneeAngle)), (x25 - 50, y25 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)

            # Right Side
            cv2.circle(img, (x12, y12), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x24, y24), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x26, y26), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x28, y28), 10, (0, 0, 255), cv2.FILLED)        
            
            cv2.line(img, (x12, y12), (x24, y24), (255, 255, 255), 3) 
            cv2.line(img, (x24, y24), (x26, y26), (255, 255, 255), 3)
            cv2.line(img, (x26, y26), (x28, y28), (255, 255, 255), 3)

            cv2.putText(img, str(int(rightSideAngle)), (x24 - 50, y24 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
            cv2.putText(img, str(int(rightKneeAngle)), (x26 - 50, y26 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)

            # Average Percentage & Counter #
            #cv2.putText(img, (str(int(averagePercentRF)) + "%"), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            #cv2.putText(img, (str(int(averagePercentLF)) + "%"), (500, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            #cv2.putText(img, (str(int(counters[2]))), (700, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)


            return counters
        except:
            doNothing = 0


cap = cv2.VideoCapture(0)
 
wireframe = CreateWireframe()
exercise = Exercises()

counters = [0,0,0]
durations = [0,0,0,0,0,0]


while True:
    # Create Wireframe from Pre-Built Model #
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img = wireframe.findPose(img, False)
    pointList = wireframe.findPosition(img, False)
    

    # Determine Exercise #
    exercise.drawSquatsPoints(pointList, counters, durations, img)
    exercise.drawPushUpsPoints(pointList, counters, durations, img)
    exercise.drawSitUpsPoints(pointList, counters, durations, img)


    # Display Counters #
    cv2.putText(img, (str(int(counters[0]))), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    cv2.putText(img, (str(int(counters[1]))), (250, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    cv2.putText(img, (str(int(counters[2]))), (700, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)


    # Display #
    cv2.imshow("Image", img)


    # "q" to Quit #
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break