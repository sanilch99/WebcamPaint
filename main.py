import cv2
import numpy as np

#setting frame size
frameHeight = 480
frameWidth = 640

# for using webcam as source
cap = cv2.VideoCapture(0)

#setting width with id 3 and height with id 4 and brightness with id 10
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,100)

# color lists
myColors = [[49,59,0,106,137,255],[0,45,0,30,255,255]]

myColorValue = [[128,0,0],[0,69,255]]

myPoints =  []
#[x, y, colorId]

def findColor(img,myColorValue):
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # creating a mask based on lower and upper bounds of hue , saturation and value
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHsv, lower, upper)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValue[count],cv2.FILLED)
        #cv2.imshow(str(color[0]), mask)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count += 1
    return newPoints

def getContours(img):
    # retr external takes the extreme outer countours ( method of extraction )
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        # finding area for each
        area = cv2.contourArea(cnt)
        #drawing the contour ( imageToDrawOn,Contour,index,color,thickness)
        #cv2.drawContours(imgContour,cnt,-1,(255,0,0),3)
        # giving minimum threshold for area to remove noise
        if area > 500 :
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            # calculate curve length to get approx edge
            per = cv2.arcLength(cnt,closed=True)
            # play around with the resolution value -> this approx gives the corner point
            approx = cv2.approxPolyDP(cnt,0.02*per,True)
            # will give us x , y , widht , height of all objects
            x, y, width, height = cv2.boundingRect(approx)
    return x+w//2 ,y

def drawOnCanvas(myPoints,myColorValue):
    for point in myPoints:
        x = point[0]
        y = point[1]
        count = point[2]
        cv2.circle(imgResult,(x,y),10,myColorValue[count],cv2.FILLED)

#video is a sequence of images
while True:
    success , img = cap.read()
    imgResult = img.copy()
    # success will store true or false
    newPoints = findColor(img,myColorValue)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValue)
    cv2.imshow("video",imgResult)
    # waits for delay and waits for q to exit
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break