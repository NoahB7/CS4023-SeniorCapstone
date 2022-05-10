from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import webbrowser
import threading
import sys
import cv2


class HomeWindow(QDialog):
    def __init__(self):
        super(HomeWindow, self).__init__()
        loadUi("HomeWindowImproved.ui", self)

        logo = QPixmap('logo4.png')
        self.logo.setPixmap(logo)

        self.loginButton.clicked.connect(self.goToWelcomeWindow)

    def goToWelcomeWindow(self):
        global welcome
        welcome = WelcomeWindow()

        try:
            widget.removeWidget(home)
        except:
            widget.removeWidget(homeInit)

        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)


class WelcomeWindow(QDialog):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        loadUi("WelcomeWindow.ui", self)

        logo = QPixmap('logo4.png')
        self.logo.setPixmap(logo)

        self.welcomeUser.setText("Sasha Lawson")

        self.beginExercisingButton.clicked.connect(self.goToWebCamWindow)
        self.logoutButton.clicked.connect(self.goToHomeWindow)

    def goToHomeWindow(self):
        global home
        home = HomeWindow()
        
        widget.removeWidget(welcome)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToWebCamWindow(self):
        thread = threading.Thread(target=self.runExerciseDetection)
        thread.start()
        widget.hide()

        while True:
            if thread.is_alive():
                doNothing = 0
            else:
                widget.show()
                break

        global result
        result = ResultWindow()

        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def runExerciseDetection(self):
        cap = cv2.VideoCapture(0)   

        while True:
            img = cap.read()[1]
            newSize = (1200, 800)
            imgResized = cv2.resize(img, newSize)
            
            cv2.imshow("VizFit Exercise Webcam", imgResized)
            cv2.resizeWindow("VizFit Exercise Webcam",newSize)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if cv2.getWindowProperty("VizFit Exercise Webcam", cv2.WND_PROP_VISIBLE) < 1:
                break

        cv2.destroyAllWindows()
        cap.release()


class ResultWindow(QDialog):
    def __init__(self):
        super(ResultWindow, self).__init__()
        loadUi("ResultWindow.ui", self)

        logo = QPixmap('logo4.png')
        self.logo.setPixmap(logo)

        #self.welcomeUser.setText("Sasha Lawson")

        self.analyticsButton.clicked.connect(self.goToAnalytics)
        self.beginExercisingButton.clicked.connect(self.goToWebCamWindow)
        self.logoutButton.clicked.connect(self.goToHomeWindow)

    def goToAnalytics(self):
        webbrowser.open("https://mackey.cs.uafs.edu/")

    def goToHomeWindow(self):
        global home
        home = HomeWindow()
        
        widget.removeWidget(result)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToWebCamWindow(self):
        thread = threading.Thread(target=self.runExerciseDetection)
        thread.start()
        widget.hide()

        while True:
            if thread.is_alive():
                doNothing = 0
            else:
                widget.show()
                break

        #global result
        #result = ResultWindow()

        #widget.addWidget(result)
        #widget.setCurrentIndex(widget.currentIndex()+1)

    def runExerciseDetection(self):
        cap = cv2.VideoCapture(0)

        while True:
            img = cap.read()[1]
            newSize = (1200, 800)
            imgResized = cv2.resize(img, newSize)
            
            cv2.imshow("VizFit Exercise Webcam", imgResized)
            cv2.resizeWindow("VizFit Exercise Webcam",newSize)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if cv2.getWindowProperty("VizFit Exercise Webcam", cv2.WND_PROP_VISIBLE) < 1:
                break

        cv2.destroyAllWindows()
        cap.release()


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