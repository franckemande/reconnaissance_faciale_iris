import sqlite3
import json

# Connexion à la base (ou création si elle n'existe pas)
conn = sqlite3.connect("DBManagement.db")
cursor = conn.cursor()

# Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    encodage TEXT NOT NULL, 
    poste TEXT CHECK(poste IN ('patron', 'employe', 'client')) NOT NULL
);
""")

#fonction d'insertion
def inserer_user(nom, prenom, encodage, poste):
    """
    Insère un nouvel utilisateur dans la base de données SQLite.
    
    Paramètres :
        nom (str)       : Nom de l'utilisateur
        prenom (str)    : Prénom de l'utilisateur
        encodage (list) : Liste (ou tableau) de réels représentant l'encodage du visage
        poste (str)     : Poste de l'utilisateur ('patron', 'employe' ou 'client')
    """
    # Vérification du poste
    if poste not in ['patron', 'employe', 'client']:
        raise ValueError("Le poste doit être 'patron', 'employe' ou 'client'")

    # Connexion à la base
    conn = sqlite3.connect("DBManagement.db")
    cursor = conn.cursor()

    # Insertion
    cursor.execute("""
        INSERT INTO users (nom, prenom, encodage, poste)
        VALUES (?, ?, ?, ?)
    """, (nom, prenom, json.dumps(encodage), poste))

    # Sauvegarde et fermeture
    conn.commit()
    conn.close()
    print(f"Utilisateur {prenom} {nom} ajouté avec succès !")

conn.commit()
conn.close()
print("Table users créée avec succès ")


inserer_user("marie", "miguel", [],"employe")