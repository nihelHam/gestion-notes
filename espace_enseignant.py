import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
from config import DB_CONFIG
import csv
import json

def connecter_bd():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

def afficher_interface_professeur(info_utilisateur):
    """Affiche l'interface de l'espace enseignant avec un message de bienvenue."""
    def deconnexion():
        fenetre.destroy()
        messagebox.showinfo("Déconnexion", "Vous êtes déconnecté.")

    fenetre = Tk()
    fenetre.title("Espace Enseignant")

    # Message de bienvenue
    label_bienvenue = Label(fenetre, text=f"Bienvenue, {info_utilisateur[1]} {info_utilisateur[2]} ({info_utilisateur[3]})", font=("Helvetica", 14))
    label_bienvenue.pack(pady=10)

    # Menu latéral
    frame_menu = Frame(fenetre)
    frame_menu.pack(side=LEFT, fill=Y)

    # Boutons d'affichage
    Label(frame_menu, text="Affichage").pack()
    Button(frame_menu, text="Afficher Étudiants", command=afficher_etudiants).pack(fill=X)
    Button(frame_menu, text="Afficher Classes", command=afficher_classes).pack(fill=X)
    Button(frame_menu, text="Afficher Matières", command=afficher_matieres).pack(fill=X)
    Button(frame_menu, text="Afficher Professeurs", command=afficher_professeurs).pack(fill=X)

    # Séparateur
    Label(frame_menu, text="Gestion").pack(pady=10)

    # Boutons de gestion
    Button(frame_menu, text="Ajouter Étudiant", command=ajouter_etudiant).pack(fill=X)
    Button(frame_menu, text="Ajouter Classe", command=ajouter_classe).pack(fill=X)
    Button(frame_menu, text="Ajouter Matière", command=ajouter_matiere).pack(fill=X)
    Button(frame_menu, text="Ajouter Professeur", command=ajouter_professeur).pack(fill=X)
    Button(frame_menu, text="Gérer Absences", command=gerer_absences).pack(fill=X)
    Button(frame_menu, text="Calculer Moyennes", command=calculer_moyennes).pack(fill=X)
    Button(frame_menu, text="Sauvegarder Données", command=sauvegarder_donnees).pack(fill=X)
    Button(frame_menu, text="Charger Données", command=charger_donnees).pack(fill=X)

    # Bouton de déconnexion
    Button(frame_menu, text="Se Déconnecter", command=deconnexion).pack(fill=X)

    # Lancement de la fenêtre
    fenetre.mainloop()

# Gestion des absences
def gerer_absences():
    def enregistrer_absence():
        id_etudiant = entree_id_etudiant.get()
        date_absence = entree_date_absence.get()
        
        conn = connecter_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO absences (id_etudiant, date_absence) VALUES (%s, %s)", (id_etudiant, date_absence))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Succès", "Absence enregistrée avec succès!")
        fenetre_ajout_absence.destroy()

    fenetre_ajout_absence = Toplevel()
    fenetre_ajout_absence.title("Gérer Absences")

    Label(fenetre_ajout_absence, text="ID Étudiant:").grid(row=0, column=0)
    entree_id_etudiant = Entry(fenetre_ajout_absence)
    entree_id_etudiant.grid(row=0, column=1)

    Label(fenetre_ajout_absence, text="Date d'absence (YYYY-MM-DD):").grid(row=1, column=0)
    entree_date_absence = Entry(fenetre_ajout_absence)
    entree_date_absence.grid(row=1, column=1)

    Button(fenetre_ajout_absence, text="Enregistrer", command=enregistrer_absence).grid(row=2, column=1)

# Calcul des moyennes et génération de bulletins
def calculer_moyennes():
    conn = connecter_bd()
    cursor = conn.cursor()
    cursor.execute("""SELECT e.nom, e.prenom, AVG(n.valeur) as moyenne 
                      FROM etudiant e 
                      JOIN note n ON e.id_etudiant = n.id_etudiant
                      GROUP BY e.id_etudiant""")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    fenetre_moyennes = Toplevel()
    fenetre_moyennes.title("Moyennes des Étudiants")

    tree = ttk.Treeview(fenetre_moyennes, columns=("Nom", "Prénom", "Moyenne"), show="headings")
    tree.heading("Nom", text="Nom")
    tree.heading("Prénom", text="Prénom")
    tree.heading("Moyenne", text="Moyenne")
    tree.pack(fill=BOTH, expand=True)

    for row in rows:
        tree.insert("", END, values=row)

    Button(fenetre_moyennes, text="Générer Bulletin", command=lambda: generer_bulletin(rows)).pack()

def generer_bulletin(rows):
    # Implémentation pour générer le bulletin au format texte ou CSV
    with open("bulletin.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nom", "Prénom", "Moyenne"])
        for row in rows:
            writer.writerow(row)
    messagebox.showinfo("Succès", "Bulletin généré avec succès au format CSV!")

# Sauvegarde des données
def sauvegarder_donnees():
    data = {}
    conn = connecter_bd()
    cursor = conn.cursor()
    
    # Exemples de données à sauvegarder
    cursor.execute("SELECT * FROM etudiant")
    data['etudiants'] = cursor.fetchall()
    
    cursor.execute("SELECT * FROM classe")
    data['classes'] = cursor.fetchall()
    
    cursor.execute("SELECT * FROM professeur")
    data['professeurs'] = cursor.fetchall()
    
    cursor.close()
    conn.close()

    with open("donnees.json", "w") as json_file:
        json.dump(data, json_file)

    messagebox.showinfo("Succès", "Données sauvegardées avec succès dans donnees.json!")

# Chargement des données
def charger_donnees():
    with open("donnees.json", "r") as json_file:
        data = json.load(json_file)
    
    conn = connecter_bd()
    cursor = conn.cursor()

    # Exemples de chargement de données
    for etudiant in data['etudiants']:
        cursor.execute("INSERT INTO etudiant (nom, prenom, adresse_mail, date_naissance, id_classe) VALUES (%s, %s, %s, %s, %s)", etudiant[1:]) # Exclure l'ID

    for classe in data['classes']:
        cursor.execute("INSERT INTO classe (nom_classe, niveau) VALUES (%s, %s)", classe[1:]) # Exclure l'ID

    for professeur in data['professeurs']:
        cursor.execute("INSERT INTO professeur (nom, prenom, adresse_mail, mot_de_passe) VALUES (%s, %s, %s, %s)", professeur[1:]) # Exclure l'ID

    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Succès", "Données chargées avec succès!")

# Ajout d'un étudiant
def ajouter_etudiant():
    def enregistrer_etudiant():
        nom = entree_nom.get()
        prenom = entree_prenom.get()
        email = entree_email.get()
        date_naissance = entree_date_naissance.get()
        classe_id = entree_classe.get()

        conn = connecter_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO etudiant (nom, prenom, adresse_mail, date_naissance, id_classe) VALUES (%s, %s, %s, %s, %s)",
                       (nom, prenom, email, date_naissance, classe_id))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Succès", "Étudiant ajouté avec succès!")
        fenetre_ajout_etudiant.destroy()
        afficher_etudiants()

    fenetre_ajout_etudiant = Toplevel()
    fenetre_ajout_etudiant.title("Ajouter Étudiant")

    Label(fenetre_ajout_etudiant, text="Nom:").grid(row=0, column=0)
    entree_nom = Entry(fenetre_ajout_etudiant)
    entree_nom.grid(row=0, column=1)

    Label(fenetre_ajout_etudiant, text="Prénom:").grid(row=1, column=0)
    entree_prenom = Entry(fenetre_ajout_etudiant)
    entree_prenom.grid(row=1, column=1)

    Label(fenetre_ajout_etudiant, text="Email:").grid(row=2, column=0)
    entree_email = Entry(fenetre_ajout_etudiant)
    entree_email.grid(row=2, column=1)

    Label(fenetre_ajout_etudiant, text="Date de Naissance:").grid(row=3, column=0)
    entree_date_naissance = Entry(fenetre_ajout_etudiant)
    entree_date_naissance.grid(row=3, column=1)

    Label(fenetre_ajout_etudiant, text="ID Classe:").grid(row=4, column=0)
    entree_classe = Entry(fenetre_ajout_etudiant)
    entree_classe.grid(row=4, column=1)

    Button(fenetre_ajout_etudiant, text="Enregistrer", command=enregistrer_etudiant).grid(row=5, column=1)

# Affichage des étudiants
def afficher_etudiants():
    conn = connecter_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM etudiant")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    fenetre_etudiants = Toplevel()
    fenetre_etudiants.title("Liste des Étudiants")

    tree = ttk.Treeview(fenetre_etudiants, columns=("ID", "Nom", "Prénom", "Email", "Date de Naissance", "ID Classe"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nom", text="Nom")
    tree.heading("Prénom", text="Prénom")
    tree.heading("Email", text="Email")
    tree.heading("Date de Naissance", text="Date de Naissance")
    tree.heading("ID Classe", text="ID Classe")
    tree.pack(fill=BOTH, expand=True)

    for row in rows:
        tree.insert("", END, values=row)

# Ajout d'une classe
def ajouter_classe():
    def enregistrer_classe():
        nom_classe = entree_nom_classe.get()
        niveau = entree_niveau.get()

        conn = connecter_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classe (nom_classe, niveau) VALUES (%s, %s)", (nom_classe, niveau))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Succès", "Classe ajoutée avec succès!")
        fenetre_ajout_classe.destroy()
        afficher_classes()

    fenetre_ajout_classe = Toplevel()
    fenetre_ajout_classe.title("Ajouter Classe")

    Label(fenetre_ajout_classe, text="Nom Classe:").grid(row=0, column=0)
    entree_nom_classe = Entry(fenetre_ajout_classe)
    entree_nom_classe.grid(row=0, column=1)

    Label(fenetre_ajout_classe, text="Niveau:").grid(row=1, column=0)
    entree_niveau = Entry(fenetre_ajout_classe)
    entree_niveau.grid(row=1, column=1)

    Button(fenetre_ajout_classe, text="Enregistrer", command=enregistrer_classe).grid(row=2, column=1)

# Affichage des classes
def afficher_classes():
    conn = connecter_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classe")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    fenetre_classes = Toplevel()
    fenetre_classes.title("Liste des Classes")

    tree = ttk.Treeview(fenetre_classes, columns=("ID", "Nom Classe", "Niveau"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nom Classe", text="Nom Classe")
    tree.heading("Niveau", text="Niveau")
    tree.pack(fill=BOTH, expand=True)

    for row in rows:
        tree.insert("", END, values=row)

# Ajout d'une matière
def ajouter_matiere():
    def enregistrer_matiere():
        nom_matiere = entree_nom_matiere.get()

        conn = connecter_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO matiere (nom_matiere) VALUES (%s)", (nom_matiere,))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Succès", "Matière ajoutée avec succès!")
        fenetre_ajout_matiere.destroy()
        afficher_matieres()

    fenetre_ajout_matiere = Toplevel()
    fenetre_ajout_matiere.title("Ajouter Matière")

    Label(fenetre_ajout_matiere, text="Nom Matière:").grid(row=0, column=0)
    entree_nom_matiere = Entry(fenetre_ajout_matiere)
    entree_nom_matiere.grid(row=0, column=1)

    Button(fenetre_ajout_matiere, text="Enregistrer", command=enregistrer_matiere).grid(row=1, column=1)

# Affichage des matières
def afficher_matieres():
    conn = connecter_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matiere")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    fenetre_matieres = Toplevel()
    fenetre_matieres.title("Liste des Matières")

    tree = ttk.Treeview(fenetre_matieres, columns=("ID", "Nom Matière"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nom Matière", text="Nom Matière")
    tree.pack(fill=BOTH, expand=True)

    for row in rows:
        tree.insert("", END, values=row)

# Ajout d'un professeur
def ajouter_professeur():
    def enregistrer_professeur():
        nom = entree_nom.get()
        prenom = entree_prenom.get()
        email = entree_email.get()
        mot_de_passe = entree_mot_de_passe.get()

        conn = connecter_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO professeur (nom, prenom, adresse_mail, mot_de_passe) VALUES (%s, %s, %s, %s)",
                       (nom, prenom, email, mot_de_passe))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Succès", "Professeur ajouté avec succès!")
        fenetre_ajout_professeur.destroy()

    fenetre_ajout_professeur = Toplevel()
    fenetre_ajout_professeur.title("Ajouter Professeur")

    Label(fenetre_ajout_professeur, text="Nom:").grid(row=0, column=0)
    entree_nom = Entry(fenetre_ajout_professeur)
    entree_nom.grid(row=0, column=1)

    Label(fenetre_ajout_professeur, text="Prénom:").grid(row=1, column=0)
    entree_prenom = Entry(fenetre_ajout_professeur)
    entree_prenom.grid(row=1, column=1)

    Label(fenetre_ajout_professeur, text="Email:").grid(row=2, column=0)
    entree_email = Entry(fenetre_ajout_professeur)
    entree_email.grid(row=2, column=1)

    Label(fenetre_ajout_professeur, text="Mot de Passe:").grid(row=3, column=0)
    entree_mot_de_passe = Entry(fenetre_ajout_professeur, show="*")
    entree_mot_de_passe.grid(row=3, column=1)

    Button(fenetre_ajout_professeur, text="Enregistrer", command=enregistrer_professeur).grid(row=4, column=1)

# Affichage des professeurs
def afficher_professeurs():
    conn = connecter_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professeur")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    fenetre_professeurs = Toplevel()
    fenetre_professeurs.title("Liste des Professeurs")

    tree = ttk.Treeview(fenetre_professeurs, columns=("ID", "Nom", "Prénom", "Email"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nom", text="Nom")
    tree.heading("Prénom", text="Prénom")
    tree.heading("Email", text="Email")
    tree.pack(fill=BOTH, expand=True)

    for row in rows:
        tree.insert("", END, values=row)

