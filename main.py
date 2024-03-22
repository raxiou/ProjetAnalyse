from flask import Flask, render_template
from baseDeDonnee import Insertion_article_auteur
from Bib import BibTex
from CreationBaseDeDonnee import lancementCreationTable
from LesDiagrames import diagrameRepSexe
from LesDiagrames import nombrePersonneParArticle
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_tables')
def create_tables():
    # Insérer ici la logique pour créer les tables dans la base de données
    lancementCreationTable.main()
    return "Tables créées avec succès!"

@app.route('/insert_articles_authors')
def insert_articles_authors():
    # Insérer ici la logique pour insérer les articles et les auteurs dans la base de données
    Insertion_article_auteur.main()
    return "Articles et auteurs insérés avec succès!"

@app.route('/create_bibtex_file')
def create_bibtex_file():
    # Insérer ici la logique pour créer le fichier BibTex
    BibTex.main()
    return "Fichier BibTex créé avec succès!"

@app.route('/create_sex_diagram')
def create_sex_diagram():
    # Insérer ici la logique pour créer le diagramme représentant le sexe des auteurs
    diagrameRepSexe.main()
    return "Diagramme sur le sexe créé avec succès!"

@app.route('/create_articles_diagram')
def create_articles_diagram():
    # Insérer ici la logique pour créer le diagramme représentant le nombre d'articles par nombre de personne
    nombrePersonneParArticle.main()
    return "Diagramme sur le nombre d'articles créé avec succès!"

if __name__ == '__main__':
    app.run(debug=True)
