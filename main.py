import os
import pickle
import numpy as np
# import cv2
# import face_recognition
# import cvzone
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from firebase_admin import storage
from datetime import datetime

# cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendencerealtime-4116b-default-rtdb.firebaseio.com/',
    'storageBucket':'faceattendencerealtime-4116b.appspot.com'
})

bucket = storage.bucket()



cap = cv2.VideoCapture(0)               # capturing 
cap.set(3,640)                             # sizing x
cap.set(4,480)                         # sizing y
imgBackground = cv2.imread('Resources/background.png')       # adding the graphics

# -----------we need to import each mode's image path --------------------------------------
foldeModePath = 'Resources/Modes'
modePathList = os.listdir(foldeModePath)         #make a list of content in a particular directory
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(foldeModePath,path)))           # path of all images of mode in the list
#print(len(imgModeList))

#load encoded files
print("loading encoded file .......")
file = open('EncodeFile6.pkl','rb')
encodeListKnownWithIds = pickle.load(file)
encodeListKnown,studentIds = encodeListKnownWithIds

#print(encodeListKnown)

file.close()
print("encoded file loaded")
print(studentIds)

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)       # having the location  of the face
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)     # encoding of the new face 
    

    imgBackground[162:162+480,55:55+640] = img                #overlapping the webcam on graphic
    imgBackground[44:44+633,808:808+414] = imgModeList[modeType]

    if faceCurFrame:

        for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)     # comparing the new face and the stored face
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)      # distance of the face
            print("matches ",matches)
            print("faceDist ",faceDis)
            matchIndex = np.argmin(faceDis)
            #print("match index ",matchIndex)
    
            if matches[matchIndex]:
                # print("known face detected")
                #print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackgound = cvzone.cornerRect(imgBackground, bbox, rt=0)
    
                id = studentIds[matchIndex]
    
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
        if counter != 0:
            
            if counter == 1:
                # get the data
                studentInfo = db.reference(f'Students/{id}').get()
                #get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                
                
                
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],"%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    
                print(studentInfo)
            if modeType != 3:
    
                if 10 < counter < 20:
                    modeType = 2
    
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]        
                if counter<=10:
    
                    cv2.putText(imgBackgound,str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(imgBackgound,str(studentInfo['major']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackgound,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackgound,str(studentInfo['standing']),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackgound,str(studentInfo['year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackgound,str(studentInfo['starting_year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackgound,str(studentInfo['name']),(808+offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
        
                    # imgBackground[175:175 + 216, 909:909 + 216]= cv2.imread('resources/Modes/5.png')
                    imgBackground[175:175 + 216, 909:909 + 216]= imgStudent
    
    
                counter += 1
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
            
            





        
    # #cv2.imshow('webcam',img)
    # cv2.imshow('face attendance',imgBackground)               # showing the result
    
    # if cv2.waitKey(2) & 0xFF == ord('q'):                     # for breaking the loop
    #     break


    
