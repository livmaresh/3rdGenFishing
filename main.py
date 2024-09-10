import cv2
import pyautogui
import pydirectinput
import time
import socket
import threading
from playsound import playsound

biteCheck = True
stream = True

def matchTemplate(img, template,thre):
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    min_val = cv2.minMaxLoc(result)[0]
    thr = thre
    
    return min_val <= thr

def prepLua():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8888))
    clientsocket.send(b"Hello \n")
    sockCheck = True
    while sockCheck:
        outMessage = clientsocket.recv(1024)
        sockCheck = False
    clientsocket.close()

def gameCheck():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8888))
    clientsocket.send(b"Hello \n")
    sockCheck = True
    tempGame = ""
    while sockCheck:
        outMessage = clientsocket.recv(1024)
        tempGame = str(outMessage.decode('utf-8')).replace("\n","").replace(" ","")
        print(tempGame + " detected.")
        sockCheck = False
    clientsocket.close()
    if("Ruby" in tempGame): return "Ruby"
    elif("Sapphire" in tempGame): return "Sapphire"
    elif("Emerald" in tempGame): return "Emerald"
    elif("FireRed" in tempGame): return "Fire Red"
    elif("LeafGreen" in tempGame): return "Leaf Green"
    else: return ""

def checkBite():
    global biteCheck
    global stream 
    while(stream):
        if(biteCheck):
            pyautogui.screenshot("test.png")
            if(matchTemplate(cv2.imread('test.png'),biteTemplate,.025)):
                pydirectinput.press("z")

def checkOther():
    global biteCheck
    global stream
    global counter
    while(stream):
        pyautogui.screenshot("test2.png")
        if(matchTemplate(cv2.imread("test2.png"),hookTemplate,.065)):
            biteCheck = False
            pydirectinput.press("z")
            hookCheck = True
            while(hookCheck):
                pyautogui.screenshot("test2.png")
                if(matchTemplate(cv2.imread("test2.png"),template,.05)):
                    counter = counter + 1
                    sockCheck = True
                    print("Found a match. Checking for shiny roll.")
                    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    clientsocket.connect(('localhost', 8888))
                    clientsocket.send(b"Hello \n")
                    while sockCheck:
                        outMessage = clientsocket.recv(1024)
                        print("The shiny roll is " + str(outMessage.decode('utf-8')).replace("\n","") + ". This was attempt " + str(counter) + ".")
                        sid = int(outMessage.decode('utf-8'))
                        sockCheck = False
                    clientsocket.close()
                    if(sid < 8):
                        playsound("./assets/shinysound.mp3",block=False)
                        print("Congratulations! You have found a shiny!")
                        time.sleep(5)
                        stream = False
                    else:
                        pydirectinput.press("right")
                        time.sleep(.25)
                        pydirectinput.press("down")
                        time.sleep(.25)
                        pydirectinput.press("z")
                        time.sleep(.25)
                        pydirectinput.press("z")
                        time.sleep(3)
                        pydirectinput.press("shift")
                    hookCheck = False
                    biteCheck = True
                else:
                    pydirectinput.press("x")
        elif(matchTemplate(cv2.imread("test2.png"),nibbleTemplate,.07)):
            pydirectinput.press("z")
            time.sleep(.2)
            pydirectinput.press("shift")
        elif(matchTemplate(cv2.imread("test2.png"),gotAway,.025)):
            pydirectinput.press("z")
            time.sleep(.2)
            pydirectinput.press("shift")

prepLua()
sid = 99999
counter = 0
firstPass = True
game = gameCheck()


nibbleTemplate = cv2.imread('./assets/notEvenANibble.png')
biteTemplate = cv2.imread('./assets/ohABite2.png')
hookTemplate = cv2.imread('./assets/onTheHook.png')
gotAway = cv2.imread('./assets/gotAway.png')
if(game == "Ruby" or game == "Sapphire"):
    template = cv2.imread("./assets/fightBoxRS.png")
elif(game == "Fire Red" or game == "Leaf Green" or game == "Emerald"):
    template = cv2.imread("./assets/fightBox.png")

time.sleep(5)
pydirectinput.keyDown("enter")
pydirectinput.press("left")
pydirectinput.keyUp("enter")
pydirectinput.press("x")
print("Prep finished, script is starting.")
pydirectinput.press("shift")

if(game == "Ruby" or game == "Sapphire" or game == "Emerald"):
    t1 = threading.Thread(target=checkBite)
    t2 = threading.Thread(target=checkOther)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
else:
    while(stream):
        pyautogui.screenshot("test.png")
        time.sleep(1)
        if(matchTemplate(cv2.imread("test.png"),hookTemplate,.065)):
            biteCheck = False
            pydirectinput.press("z")
            hookCheck = True
            while(hookCheck):
                pyautogui.screenshot("test.png")
                if(matchTemplate(cv2.imread("test.png"),template,.05)):
                    counter = counter + 1
                    sockCheck = True
                    print("Found a match. Checking for shiny roll.")
                    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    clientsocket.connect(('localhost', 8888))
                    clientsocket.send(b"Hello \n")
                    while sockCheck:
                        outMessage = clientsocket.recv(1024)
                        print("The shiny roll is " + str(outMessage.decode('utf-8')).replace("\n","") + ". This was attempt " + str(counter) + ".")
                        sid = int(outMessage.decode('utf-8'))
                        sockCheck = False
                    clientsocket.close()
                    if(sid < 8):
                        playsound("./assets/shinysound.mp3",block=False)
                        print("Congratulations! You have found a shiny!")
                        time.sleep(5)
                        stream = False
                    else:
                        pydirectinput.press("right")
                        time.sleep(.25)
                        pydirectinput.press("down")
                        time.sleep(.25)
                        pydirectinput.press("z")
                        time.sleep(.25)
                        pydirectinput.press("z")
                        time.sleep(3)
                        pydirectinput.press("shift")
                    hookCheck = False
                    biteCheck = True
                else:
                    pydirectinput.press("x")
        elif(matchTemplate(cv2.imread("test2.png"),nibbleTemplate,.07)):
            pydirectinput.press("z")
            time.sleep(.2)
            pydirectinput.press("shift")