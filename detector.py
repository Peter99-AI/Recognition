import cv2
import numpy as np
from PIL import Image
import pickle
import pymysql

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)
rec=cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/trainningData.yml")
id=0
#set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (135, 206, 235)

#get data from sqlite by ID
def getProfile(id):
    conn = pymysql.connect(host='localhost',
                        user='root',
                        password='chuanh255',                             
                        db='Recognition',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

    cmd="SELECT * FROM People WHERE id="+str(id)
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

while(True):
    #camera read
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getProfile(id)
        #set text to window
         
        if(profile!=None):            
            cv2.putText(img, "Name: " + str(profile['name']), (x,y+h+30), fontface, fontscale, fontcolor ,2)
            cv2.putText(img, "Age: " + str(profile['age']), (x,y+h+60), fontface, fontscale, fontcolor ,2)
            cv2.putText(img, "Gender: " + str(profile['gender']), (x,y+h+90), fontface, fontscale, fontcolor ,2)
        
        cv2.imshow('Face',img)      
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()