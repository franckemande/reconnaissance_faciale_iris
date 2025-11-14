import sqlite3
import json

# Connexion à la base
conn = sqlite3.connect("DBManagement.db")
cursor = conn.cursor()

# Lire toutes les lignes de la table users
cursor.execute("SELECT * FROM users")

# Parcourir les résultats
for row in cursor.fetchall():
    id, nom, prenom, encodage_json, poste = row
    encodage = json.loads(encodage_json)  # convertir le texte JSON en liste
    print(f"ID: {id}, Nom: {nom}, Prénom: {prenom}, Poste: {poste}")
    print(f"Encodage: {encodage}\n")

conn.close()