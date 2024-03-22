import tkinter as tk
from tkinter import ttk  # Importer le module ttk pour des styles améliorés
from LesDiagrames import diagrameRepSexe
from LesDiagrames import nombrePersonneParArticle
from Bib import BibTex
from baseDeDonnee import Insertion_article_auteur
from CreationBaseDeDonnee import lancementCreationTable

def inserer_articles_auteurs():
    message_label.config(text="Lancement de l'insertion des articles et des auteurs...")
    Insertion_article_auteur.main()
    message_label.config(text="Insertion terminée.")

def creer_fichier_bibtex():
    message_label.config(text="Lancement de la création du fichier BibTex...")
    BibTex.main()
    message_label.config(text="Création du fichier BibTex terminée.")

def creer_diagramme_sexe():
    message_label.config(text="Lancement de la création du diagramme représentant le sexe des auteurs...")
    diagrameRepSexe.main()
    message_label.config(text="Création du diagramme terminée.")

def creer_diagramme_nombre_articles():
    message_label.config(text="Lancement de la création du diagramme représentant le nombre d'articles par nombre de personne...")
    nombrePersonneParArticle.main()
    message_label.config(text="Création du diagramme terminée.")

def creer_tables():
    message_label.config(text="Lancement de la création des tables dans la base de données...")
    lancementCreationTable.main()
    message_label.config(text="Création des tables terminée.")
# Création de la fenêtre principale
root = tk.Tk()
root.title("Interface de lancement des programmes")

# Définir un style pour les boutons
style = ttk.Style()
style.configure('TButton', padding=5, font=('Arial', 12), width=20)  # Ajuster la largeur des boutons

# Création des boutons
button_creation_tables = ttk.Button(root, text="Créer Tables", command=creer_tables)
button_creation_tables.pack(pady=5, padx=10, fill=tk.X)

button_insertion = ttk.Button(root, text="Insertion Articles/Auteurs", command=inserer_articles_auteurs)
button_insertion.pack(pady=5, padx=10, fill=tk.X)

button_bibtex = ttk.Button(root, text="Créer Fichier BibTex", command=creer_fichier_bibtex)
button_bibtex.pack(pady=5, padx=10, fill=tk.X)

button_sexe = ttk.Button(root, text="Créer Diagramme Sexe", command=creer_diagramme_sexe)
button_sexe.pack(pady=5, padx=10, fill=tk.X)

button_nombre = ttk.Button(root, text="Créer Diagramme Nombre Articles", command=creer_diagramme_nombre_articles)
button_nombre.pack(pady=5, padx=10, fill=tk.X)

# Étiquette pour afficher les messages
message_label = tk.Label(root, text="", font=('Arial', 12))
message_label.pack(pady=5)

# Lancer la boucle principale
root.mainloop()
