import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import socket
import os
import speech_recognition as sr

s = socket.socket()

server_ip ="192.168.43.227"
server_port =1234
s.connect((server_ip, server_port))

mic = sr.Microphone()
rec = sr.Recognizer()


data_path = '/Users/Mridul/Desktop/mridul/'

onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

Training_Data, Labels = [], []

for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)

Labels = np.asarray(Labels, dtype=np.int32)
model=cv2.face_LBPHFaceRecognizer.create()

model.train(np.asarray(Training_Data), np.asarray(Labels))
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(img, size=0.5):
    
    # Convert image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return img, []
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi


# Open Webcam
cap = cv2.VideoCapture(0)
count=1
while True:
    if count==2:
        break
    else:
        ret, frame = cap.read()
    
        image, face = face_detector(frame)
    
    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        # Pass face to prediction model
        # "results" comprises of a tuple containing the label and the confidence value
        results = model.predict(face)
        print(results)
        if results[1] < 500:
            confidence = int( 100 * (1 - (results[1])/400) )
            display_string = str(confidence) + '% Confident it is User'
            
        cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)
        
        if confidence > 75:
            cv2.putText(image, "Hey Mridul", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            cv2.imshow('Face Recognition', image )
            count+=1
            break
    
            #enter menu code here
            #remote_ip = input("Enter remote ip: ")
    
            #remote_ip = remote_ip.encode()
            #s.send(remote_ip)
            #remote_password = input("Enter password for remote system: ")
            #remote_password = remote_password.encode()
            #s.send(remote_password)
            

            
            
                       
        else:
            cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            cv2.imshow('Face Recognition', image )

    except:
        cv2.putText(image, "No Face Found", (220, 120) , cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        cv2.imshow('Face Recognition', image )
        pass
        
    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break
cap.release()
cv2.destroyAllWindows()        

print("Hello Mridul !")
print("say abort to exit")
while True:
        with mic as source:
                print("What do you want me to do: ")
                audio = rec.listen(source)
                cmd = rec.recognize_google(audio)
                print(cmd)
                if "click" in cmd:
                    ip=input("Enter ip: ")
                    cmd="click" + " " + ip
                    
                elif cmd == "abort" or cmd == "Abort":
                    answer=input("Are you sure you want to exit(Y/N): ")
                    if answer =="Y" or answer == "y":
                        print("Thank you for using our Product....!!!!")
                        break
                        
        cmd2 = cmd.encode()
        s.send(cmd2)
        output = s.recv(200).decode()
        if "click" in cmd:
            print("the photo is here: {}".format(output))
        else:
            print(output)
