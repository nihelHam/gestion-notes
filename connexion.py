from tkinter import messagebox
import mysql.connector
from tkinter import *
from config import DB_CONFIG  # Assurez-vous que votre fichier config.py contient les bons paramètres
from espace_enseignant import afficher_interface_professeur  # On importe la fonction affichant l'interface du professeur

def verifier_connexion(email, mot_de_passe):
    """Vérifie les informations de connexion de l'enseignant."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        cursor = conn.cursor()

        # Requête pour vérifier l'enseignant
        cursor.execute("""
            SELECT id_professeur, nom, prenom, adresse_mail 
            FROM professeur 
            WHERE adresse_mail = %s AND mot_de_passe = %s
        """, (email, mot_de_passe))
        
        # Cela renvoie un tuple avec id_professeur, nom, prenom, adresse_mail
        resultat = cursor.fetchone()

        cursor.close()
        conn.close()

        return resultat  # Cela doit être un tuple (id_professeur, nom, prenom, adresse_mail)

    except mysql.connector.Error as err:
        messagebox.showerror("Erreur de connexion", f"Erreur: {err}")
        return None

def connecter():
    """Fonction appelée lors de l'appui sur le bouton de connexion."""
    email = entry_email.get()
    mot_de_passe = entry_mdp.get()

    if not email or not mot_de_passe:
        messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs.")
        return

    resultat = verifier_connexion(email, mot_de_passe)
    if resultat:
        # Appel de la fonction pour afficher l'interface de l'espace enseignant
        afficher_interface_professeur(resultat)
        # Fermer la fenêtre de connexion
        fenetre_connexion.destroy()
    else:
        messagebox.showerror("Échec de connexion", "Identifiants invalides.")

# Création de la fenêtre de connexion
fenetre_connexion = Tk()
fenetre_connexion.title("Connexion Enseignant")
fenetre_connexion.geometry("400x300")

# Etiquettes et champs de saisie
label_email = Label(fenetre_connexion, text="Email :")
label_email.pack(pady=10)
entry_email = Entry(fenetre_connexion)
entry_email.pack(pady=10)

label_mdp = Label(fenetre_connexion, text="Mot de passe :")
label_mdp.pack(pady=10)
entry_mdp = Entry(fenetre_connexion, show="*")
entry_mdp.pack(pady=10)

# Bouton de connexion
bouton_connexion = Button(fenetre_connexion, text="Se connecter", command=connecter)
bouton_connexion.pack(pady=20)

# Démarrer la boucle principale de la fenêtre
fenetre_connexion.mainloop()
