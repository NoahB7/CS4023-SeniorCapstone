from PIL import ImageTk as ImgTk
from tkinter import *
import webbrowser
import threading
import cv2


def runExerciseDetection():
    cap = cv2.VideoCapture(0)

    while True:
        img = cap.read()[1]
        cv2.imshow("VizFit Exercise - Webcam", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.getWindowProperty("VizFit Exercise - Webcam", cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()
    cap.release()

def startThread():
    thread1 = threading.Thread(target=runExerciseDetection)
    thread1.start()
    root.withdraw()

    while True:
        if thread1.is_alive():
            doNothing = 0
        else:
            root.deiconify()
            for widget in root.winfo_children():
                widget.destroy()
            break

    showResults()
    

def openToSite():
    webbrowser.open("https://mackey.cs.uafs.edu/")


def showHome():
    def showLogin():
        def toWelcomefromHome():
            top.destroy()
            root.deiconify()

            logoLabel.destroy()
            loginButton.destroy()
            registerButton.destroy()
            instructions.destroy()
            filler.destroy()

            showWelcome()
            
        def closeLogin():
            top.destroy()
            root.deiconify()

        # Hide Home Page #
        root.withdraw()

        top = Toplevel()
        top.title("VizFit - Login")
        top.config(bg="#434343")
        top.resizable(False, False) 
        topCanvas = Canvas(top, width=400, height=100, bg="#434343", highlightthickness=0)
        topCanvas.grid(columnspan=3)


        # User Label & Entry #
        usernameLabel = Label(top, text="User:", font=("Arial",15), fg="#FFFFFF", bg="#434343", anchor="w")
        usernameLabel.grid(columnspan=2, column=0, row=0, padx=0)

        username = Entry(top, width=30)
        username.grid(columnspan=2, column=1, row=0, padx=(0,20), pady=0)


        # Password Label & Entry #
        passwordLabel = Label(top, text="Password:", font=("Arial",15), fg="#FFFFFF", bg="#434343", anchor="w")
        passwordLabel.grid(columnspan=2, column=0, row=1, padx=(0,50), pady=(0,30))

        password = Entry(top, width=30)
        password.grid(columnspan=2, column=1, row=1, padx=(0,20), pady=(0,30))


        # Submit Button #
        submitButton = Button(top, text="Submit", font="Arial", width=12, bg="#6aa84f", command=toWelcomefromHome)
        submitButton.grid(columnspan=3, column=0, row=2, pady=(0,15))
        

        top.protocol("WM_DELETE_WINDOW", closeLogin)


    # Logo Label #
    logo = ImgTk.PhotoImage(file = 'logo4.png')
    logoLabel = Label(image=logo)
    logoLabel.image = logo
    logoLabel.config(border=False)
    logoLabel.grid(columnspan=3, column=0, row=0, pady=(0,0))


    # Login Button #
    loginButton = Button(root, text="Login", font="Arial", height=3, width=12, bg="#6aa84f",command=showLogin)
    loginButton.grid(columnspan=2, column=0, row=1, pady=(0,30))


    # Register Button #
    registerButton = Button(root, text="Register", font="Arial", height=3, width=12, bg="#6aa84f", command=openToSite)
    registerButton.grid(columnspan=2, column=1, row=1, pady=(0,30))


    # Instructions Label #
    instructions = Label(root, text="Please login. Don't have a account? Register!", font=("Arial",20), fg="#FFFFFF", bg="#434343")
    instructions.grid(columnspan=3, column=0, row=3)

    
    # Filler Space #
    filler = Label(root, text="!!!!!!!!!!!!!!!!!!!!!!!!!", font="Arial", fg="#434343", bg="#434343")
    filler.grid(columnspan=3, column=0, row=4)


def showWelcome():
    def toHomefromWelcome():
        logoLabel.destroy()
        welcome.destroy()
        beginButton.destroy()
        logoutButton.destroy()
        filler.destroy()

        showHome()

    # Logo Label #
    logo = ImgTk.PhotoImage(file = 'logo4.png')
    logoLabel = Label(image=logo)
    logoLabel.image = logo
    logoLabel.config(border=False)
    logoLabel.grid(columnspan=3, column=0, row=0, pady=(0,0))

    
    # Welcome Label #
    welcome = Label(root, text="Welcome back, [Insert Name]!", font=("Arial",20), fg="#FFFFFF", bg="#434343")
    welcome.grid(columnspan=3, column=0, row=1, pady=(0,30))


    # Begin Exercise Button #
    beginButton = Button(root, text="Begin Exercising", font="Arial", height=3, width=16, bg="#6aa84f",command=startThread)
    beginButton.grid(column=1, row=2, pady=(15,30))


    # Logout Button #
    logoutButton = Button(root, text="Logout", font="Arial", height=2, width=8, bg="#6aa84f", command=toHomefromWelcome)
    logoutButton.grid(column=1, row=3, pady=(0,30))

    
    # Filler Space #
    filler = Label(root, text="!!!!!!!!!!!!!!!!!!!!!!!!!", font="Arial", fg="#434343", bg="#434343")
    filler.grid(columnspan=3, column=0, row=4)


def showResults():
    def toHomefromResults():
        logoLabel.destroy()
        output1.destroy()
        filler1.destroy()
        output2.destroy()
        squatsLabel.destroy()
        pushUpLabel.destroy()
        sitUpLabel.destroy()
        sqautsResult.destroy()
        pushUpResult.destroy()
        sqautsResult.destroy()
        filler2.destroy()
        beginButton.destroy()
        logoutButton.destroy()

        showHome()

    canvas = Canvas(root, width=700, height=400, bg="#434343", highlightthickness=0)
    canvas.grid(columnspan=3)
    canvas.config(height=300)


    # Logo Label #
    logo = ImgTk.PhotoImage(file = 'logo4.png')
    logoLabel = Label(image=logo)
    logoLabel.image = logo
    logoLabel.config(border=False)
    logoLabel.grid(columnspan=3, column=0, row=0, pady=0)


    # Output1 Label #
    output1 = Label(root, text="Great Job, [Insert Name]!", font=("Arial",25), fg="#FFFFFF", bg="#434343")
    output1.grid(columnspan=3, column=0, row=1, padx=0)

    # Filler Space #
    filler1 = Label(root, text="!!!!!!!!!!!!!!!!!!!!!!!!!", font="Arial", fg="#434343", bg="#434343")
    filler1.grid(columnspan=3, column=0, row=2)

    # Output2 Label #
    output2 = Label(root, text="You completed the following number of exercises:", font=("Arial",15), fg="#FFFFFF", bg="#434343")
    output2.grid(columnspan=3, column=0, row=3, padx=0)


    # Results Label #
    squatsLabel = Label(root, text="Squats:", font=("Arial",25), fg="#FFFFFF", bg="#434343")
    squatsLabel.grid(columnspan=2, column=0, row=4, padx=(30,0))

    pushUpLabel = Label(root, text="Push-Up:", font=("Arial",25), fg="#FFFFFF", bg="#434343")
    pushUpLabel.grid(columnspan=2, column=0, row=5, padx=(0,0))

    sitUpLabel = Label(root, text="Sit-Up:", font=("Arial",25), fg="#FFFFFF", bg="#434343")
    sitUpLabel.grid(columnspan=2, column=0, row=6, padx=(40,0))


    sqautsResult = Label(root, text="500", font=("Arial",25), fg="#FFFFFF", bg="#434343")
    sqautsResult.grid(columnspan=3, column=1, row=4)

    pushUpResult = Label(root, text="50", font=("Arial",25), fg="#FFFFFF", bg="#434343")
    pushUpResult.grid(columnspan=3, column=1, row=5)

    sitUpResult = Label(root, text="5000", font=("Arial",25), fg="#FFFFFF", bg="#434343")
    sitUpResult.grid(columnspan=3, column=1, row=6)


    # Filler Space #
    filler2 = Label(root, text="!!!!!!!!!!!!!!!!!!!!!!!!!", font="Arial", fg="#434343", bg="#434343")
    filler2.grid(columnspan=3, column=0, row=7)


    # Begin Exercise Button #
    beginButton = Button(root, text="Begin Exercise", font="Arial", height=2, width=13, bg="#6aa84f", command=startThread)
    beginButton.grid(columnspan=2, column=0, row=8, pady=(30,30))


    # Logout Button #
    logoutButton = Button(root, text="Logout", font="Arial", height=2, width=13, bg="#6aa84f", command=toHomefromResults)
    logoutButton.grid(columnspan=2, column=1, row=8, pady=(30,30))


root = Tk()

root.title("VizFit Exercise Application")
root.config(bg="#434343")
root.resizable(False, False) 
canvas = Canvas(root, width=700, height=400, bg="#434343", highlightthickness=0)
canvas.grid(columnspan=3)


showHome()


root.mainloop()