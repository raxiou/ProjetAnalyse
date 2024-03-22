import json
import requests
import psycopg2

def generate_bibtex_entry(data_tuple, column_names):
    # Définir le type d'entrée BibTeX (dans ce cas, "article")
    entry_type = 'article'
    # Commencer la chaîne de caractères de l'entrée BibTeX avec le type d'entrée et une accolade ouvrante
    bibtex_entry = f"@{entry_type}{{"

    # Parcourir les éléments du tuple
    for i in range(len(column_names)):
        # Ajouter chaque élément avec son nom de colonne correspondant dans l'entrée BibTeX
        bibtex_entry += f"{column_names[i]} = {{{data_tuple[i]}}}"
        # Ajouter une virgule si ce n'est pas le dernier élément
        if i < len(column_names) - 1:
            bibtex_entry += ', '

    # Ajouter une accolade fermante à la fin de l'entrée BibTeX
    bibtex_entry += "}"
    # Retourner l'entrée BibTeX générée
    return bibtex_entry

def main():
    ##connexion à la base de données
    conn = psycopg2.connect(dbname="analyse",
                            user="analyse",
                            password="password",
                            host="localhost",
                            port="5432",
                            options="-c search_path=dbo,bdd")

    ##création du curseur
    cur = conn.cursor()

    ##exécution de la requête SQL
    cur.execute("""SELECT _article.idarticle, nom ,url ,year ,page ,doi ,ee ,pid, lastname, secondname, firstname 
                FROM _article, _auteur, _ecrit
                where _ecrit.idarticle = _article.idArticle
                AND _auteur.pid = _ecrit.idauteur;""")
    rows = cur.fetchall()

    ##récupération des noms de colonnes
    colnames = [desc[0] for desc in cur.description]

    ##fermeture du curseur
    cur.close()

    ##génération des entrées BibTeX pour toutes les lignes de la base de données
    bibTex = ""
    for row in rows:
        bibTex += generate_bibtex_entry(row, colnames) + "\n\n"

    ##écriture des entrées BibTeX dans un fichier
    with open('Bib/bibtex_entries.bib', 'w') as file:
        file.write(bibTex)

    ##fermeture de la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
