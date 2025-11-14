import dlib as dl
import numpy as n
import cv2 


webcam = cv2.VideoCapture(0)

while(True):
    ret, frame = webcam.read()
    cv2.imshow("web output", frame)

    if cv2.waitKey(1) & 0xFF == ord("d"):
        break
webcam.release()
cv2.destroyAllWindows()     

