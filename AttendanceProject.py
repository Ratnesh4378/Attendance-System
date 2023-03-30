import cv2
import numpy as np
import face_recognition
import os 
from datetime import datetime
from tkinter import *
root=Tk()
root.geometry("655x433")
root.title("Attendance System")
day_var=StringVar()
date_var=StringVar()
dayLabel=Label(root,text="Enter Day:")

dayEntry=Entry(root,textvariable=day_var)

dateLabel=Label(root,text="Enter date:")

dateEntry=Entry(root,textvariable=date_var)
dayLabel.grid(row=0,column=0)
dayEntry.grid(row=0,column=1)
dateLabel.grid(row=1,column=0)
dateEntry.grid(row=1,column=1)
path= 'ImagesAttendance'
images=[]

classNames=[]
classRoll=[]
myList=os.listdir(path)
#print(myList)
for cl in myList:
    curImg=cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    x=cl.split('.',2)
    #classNames.append(os.path.splitext(cl)[0])
    #classRoll.append(os.path.splitext(cl)[1])
    classNames.append(x[0])
    classRoll.append(x[1])
#print(classNames)
#print(classRoll)
def findEncodings(images):
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(roll,name,file):
    with open(file,'r+') as f:
        myDataList=f.readlines()
        rollList=[]
    
        for line in myDataList:
            entry=line.split(',')
            rollList.append(entry[0])
            
        if roll not in rollList:
            now= datetime.now()
            dtString=now.strftime('%H:%M:%S')
            f.writelines(f'\n{roll},{name},{dtString}')
            







encodeListKnown=findEncodings(images)
#print('Encoding complete')
def solve():
    Date=str(date_var.get())
    dates=Date.split('/',3)
    filename="Attendance "+dates[0]+"-"+dates[1]+"-"+dates[2]+".csv"
    if not os.path.isfile(filename):
        file=open(filename,"w")
        
        file.writelines("Roll No , Name , Time ")
        file.close()
        print("file created successfully")
    cap= cv2.VideoCapture(0)
    
    while True:
        success,img=cap.read()
        imgS=cv2.resize(img,(0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
        facesCurFrame= face_recognition.face_locations(imgS)
        encodesCurFrame=face_recognition.face_encodings(imgS,facesCurFrame)

        for encodeFace,faceloc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex=np.argmin(faceDis)

            if matches[matchIndex]:
                roll=classRoll[matchIndex].upper()
                name=classNames[matchIndex].upper()
                #print(name)
                y1,x2,y2,x1=faceloc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,roll,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(roll,name,filename)
        if cv2.waitKey(1) == 27: 
            break

        cv2.imshow('webcam',img)
        cv2.waitKey(1)

b1=Button(text="start" ,command=solve)
b1.grid(row=2,column=1)
root.mainloop()


# faceloc= face_recognition.face_locations(imgElon)[0]
# encodeElon=face_recognition.face_encodings(imgElon)[0]
# cv2.rectangle(imgElon,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)

# facelocTest= face_recognition.face_locations(imgTest)[0]
# encodeTest=face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest,(facelocTest[3],facelocTest[0]),(facelocTest[1],facelocTest[2]),(255,0,255),2)


# results=face_recognition.compare_faces([encodeElon],encodeTest)
# faceDis=face_recognition.face_distance([encodeElon],encodeTest)

