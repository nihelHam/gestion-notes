import mysql.connector
import streamlit as st
import pandas as pd
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

def afficher_etudiants():
    conn = connecter_bd()
    df = pd.read_sql("SELECT * FROM etudiant", conn)
    conn.close()
    return df

def afficher_classes():
    conn = connecter_bd()
    df = pd.read_sql("SELECT * FROM classe", conn)
    conn.close()
    return df

def afficher_matieres():
    conn = connecter_bd()
    df = pd.read_sql("SELECT * FROM matiere", conn)
    conn.close()
    return df

def afficher_professeurs():
    conn = connecter_bd()
    df = pd.read_sql("SELECT * FROM professeur", conn)
    conn.close()
    return df

def ajouter_etudiant(nom, prenom, email, date_naissance, classe_id):
    conn = connecter_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO etudiant (nom, prenom, adresse_mail, date_naissance, id_classe) VALUES (%s, %s, %s, %s, %s)",
                   (nom, prenom, email, date_naissance, classe_id))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Étudiant ajouté avec succès!")

def ajouter_classe(nom_classe, niveau):
    conn = connecter_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO classe (nom_classe, niveau) VALUES (%s, %s)", (nom_classe, niveau))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Classe ajoutée avec succès!")

def ajouter_matiere(nom_matiere):
    conn = connecter_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO matiere (nom_matiere) VALUES (%s)", (nom_matiere,))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Matière ajoutée avec succès!")

def ajouter_professeur(nom, prenom, email, mot_de_passe):
    conn = connecter_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO professeur (nom, prenom, adresse_mail, mot_de_passe) VALUES (%s, %s, %s, %s)",
                   (nom, prenom, email, mot_de_passe))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Professeur ajouté avec succès!")

# Interface utilisateur Streamlit
st.title("Espace Enseignant")

menu = ["Afficher Étudiants", "Afficher Classes", "Afficher Matières", "Afficher Professeurs", "Ajouter Étudiant", "Ajouter Classe", "Ajouter Matière", "Ajouter Professeur"]
choice = st.sidebar.selectbox("Choisissez une option", menu)

if choice == "Afficher Étudiants":
    st.subheader("Liste des Étudiants")
    df_etudiants = afficher_etudiants()
    st.dataframe(df_etudiants)

elif choice == "Afficher Classes":
    st.subheader("Liste des Classes")
    df_classes = afficher_classes()
    st.dataframe(df_classes)

elif choice == "Afficher Matières":
    st.subheader("Liste des Matières")
    df_matieres = afficher_matieres()
    st.dataframe(df_matieres)

elif choice == "Afficher Professeurs":
    st.subheader("Liste des Professeurs")
    df_professeurs = afficher_professeurs()
    st.dataframe(df_professeurs)

elif choice == "Ajouter Étudiant":
    st.subheader("Ajouter un Étudiant")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    email = st.text_input("Email")
    date_naissance = st.date_input("Date de Naissance")
    classe_id = st.number_input("ID Classe", min_value=1)

    if st.button("Ajouter Étudiant"):
        ajouter_etudiant(nom, prenom, email, date_naissance, classe_id)

elif choice == "Ajouter Classe":
    st.subheader("Ajouter une Classe")
    nom_classe = st.text_input("Nom Classe")
    niveau = st.text_input("Niveau")

    if st.button("Ajouter Classe"):
        ajouter_classe(nom_classe, niveau)

elif choice == "Ajouter Matière":
    st.subheader("Ajouter une Matière")
    nom_matiere = st.text_input("Nom Matière")

    if st.button("Ajouter Matière"):
        ajouter_matiere(nom_matiere)

elif choice == "Ajouter Professeur":
    st.subheader("Ajouter un Professeur")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de Passe", type='password')

    if st.button("Ajouter Professeur"):
        ajouter_professeur(nom, prenom, email, mot_de_passe)
