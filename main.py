import cv2
import cvzone as cz
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller,Key
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=HandDetector(detectionCon=0.8,maxHands=2)
#detector initializes an instance of the HandDetector function
#detectionCon is detection confidence , if increased the accuracy increases, if decreased accuracy decreases and detection is slow.

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L",";"],
        ["Z", "X", "C", "V", "B", "N", "M",",",".","/"],
        ["Space","<-"]]

finalText=""
keyboard=Controller()
class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.size=size
        self.text=text

def drawAll(img,button_list):
    for button in button_list:
        x,y=button.pos
        w,h=button.size
        cz.cornerRect(img,(x,y,w,h),20,rt=0)
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        #Draws a filled rectangle on the image
        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
        #Line places text on the image

    return img

button_list = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key == "Space":
            button_list.append(Button([100 * j + 50, 100 * i + 50], key, [300, 85]))  # Larger button for Space
        elif key == "<-":
            button_list.append(Button([100 * j + 350, 100 * i + 50], key, [200, 85]))  # Larger button for Backspace
        else:
            button_list.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    success,img=cap.read()
    #Success indicates whether the frame was read or not
    # print("Success",success)
    #img is represented as numpy in shape(height,width,channels) where each element is represents the color intensity
    #print("img",img)
    if not success:
        print("Failed to capture image")
        break

    hands,img=detector.findHands(img)
    #hands contains the landmarks detected on the hand by the hand detection module
    # print("hands ",hands)
    #duplicate of img
    # print("info",bboxInfo)

    img = drawAll(img,button_list)
    # img=myButton.draw(img)
    # img=myButton1.draw(img)
    # img=myButton2.draw(img)

    if hands:
        for button in button_list:
            x,y=button.pos
            w,h=button.size

            if x< hands[0]["lmList"][8][0]<x+w and y<hands[0]["lmList"][8][1]<y+h :
                cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
                #Draws a filled rectangle on the image
                cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                #Line places text on the image

                if len(hands[0]["lmList"])>=13:
                    p1=tuple(hands[0]["lmList"][8][:2])
                    #Index finger tip landmark
                    p2=tuple(hands[0]["lmList"][12][:2])
                    #Middle Finger finger tip landmark
                    l, _, _ = detector.findDistance(p1,p2, img)

                ## When clicked
                if l<40 :
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    if button.text == "<-":
                        finalText = finalText[:-1]  # Remove the last character
                        keyboard.press(Key.backspace)  # Press backspace key

                    elif button.text == "Space":
                        finalText += " "
                        keyboard.press(Key.space)  # Press space key
                    else:
                        finalText += button.text
                        keyboard.press(button.text)
                sleep(0.2)



    cv2.rectangle(img,(50,600),(1200,700),(175,0,175),cv2.FILLED)
    cv2.putText(img,finalText,(60,680),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),4)

    cv2.imshow("Image",img)
    #displays the image in a window titled image
    key=cv2.waitKey(1)
    #waitkey is used to delay hte key press by 1ms
    if key==27:#escape=27 i.e break
        break


cap.release()
#stops capturing the video from the source such as webcam or file
cv2.destroyAllWindows()
#closes all the opencv windows