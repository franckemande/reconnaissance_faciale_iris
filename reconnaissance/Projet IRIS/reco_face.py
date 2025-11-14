import cv2
import json
import numpy as np

# on charge le modele de detection faciale
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# on charge notre modele de reconnaissance faciale cree
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("lbph_model.yml")

# encodage dans un ficheier json
with open("labels.json", "r", encoding="utf-8") as f:
    label_names = json.load(f)

# on lance la webcam
webcam = cv2.VideoCapture(0)

while True:
    ret, frame = webcam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50,50))

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (200, 200))
        roi_gray = cv2.equalizeHist(roi_gray)  # car le modele de detction a besoin de nuance de gris pour mieux detecter les visages

        # on predit
        label_id, conf = recognizer.predict(roi_gray)
        if conf < 70:
            name = label_names.get(str(label_id)) or label_names.get(label_id, "Inconnu")
            text = f"{name} ({conf:.1f})"
            color = (0, 255, 0)
        else:
            text = f"Inconnu ({conf:.1f})"
            color = (0, 0, 255)

        # on affiche la detction du visage a l'ecran dans des rectangles
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Reconnaissance Faciale", frame)
    
#on sort avec la touche e (on ameliorera la methode de sortie)
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

webcam.release()
cv2.destroyAllWindows()
