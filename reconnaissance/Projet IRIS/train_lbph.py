import os
import cv2
import numpy as np

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_PATH = "lbph_model.yml"

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
if face_cascade.empty():
    raise IOError("Impossible de charger la cascade. Vérifie le chemin.")

def prepare_dataset(dataset_dir):
    faces = []
    labels = []
    label_names = {}
    current_label = 0

    for person_name in os.listdir(dataset_dir):
        person_path = os.path.join(dataset_dir, person_name)
        if not os.path.isdir(person_path):
            continue
        label_names[current_label] = person_name
        for filename in os.listdir(person_path):
            filepath = os.path.join(person_path, filename)
            img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            # detection visage (assume un visage par photo)
            rects = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(50,50))
            if len(rects) == 0:
                continue
            x,y,w,h = rects[0]  # prendre le premier
            face = img[y:y+h, x:x+w]
            face = cv2.resize(face, (200,200))
            face = cv2.equalizeHist(face)
            faces.append(face)
            labels.append(current_label)
        current_label += 1
    return faces, labels, label_names

faces, labels, label_names = prepare_dataset(DATASET_DIR)
if len(faces) == 0:
    raise ValueError("Aucun visage trouvé dans le dataset. Vérifie les chemins et images.")

# créer et entrainer LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
recognizer.train(faces, np.array(labels))
recognizer.write(MODEL_PATH)

# sauvegarder mapping label->nom
import json
with open("labels.json", "w") as f:
    json.dump(label_names, f, ensure_ascii=False, indent=2)

print("Entraînement terminé. Modèle sauvé:", MODEL_PATH)
