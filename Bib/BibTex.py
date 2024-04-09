import json
import requests
import psycopg2

def generate_bibtex_entry(data_tuples, column_names):
    # Définir le type d'entrée BibTeX (dans ce cas, "article")
    entry_type = 'article'
    # Commencer la chaîne de caractères de l'entrée BibTeX avec le type d'entrée et une accolade ouvrante
    bibtex_entry = f"@{entry_type}{{"

    # Extraire les informations spécifiques à chaque article
    idarticle, nom, url, year, page, doi, ee, pid = data_tuples[0][:8]

    # Créer une liste pour stocker les noms complets des auteurs
    authors = []

    # Parcourir les tuples de données pour extraire les noms des auteurs
    for row in data_tuples:
        authors.append("{" + ", ".join(row[8:]) + "}")

    # Ajouter les informations de l'article à l'entrée BibTeX
    bibtex_entry += f"idarticle = {{{idarticle}}}, "
    bibtex_entry += f"nom = {{{nom}}}, "
    bibtex_entry += f"url = {{{url}}}, "
    bibtex_entry += f"year = {{{year}}}, "
    bibtex_entry += f"page = {{{page}}}, "
    bibtex_entry += f"doi = {{{doi}}}, "
    bibtex_entry += f"ee = {{{ee}}}, "
    bibtex_entry += f"pid = {{{pid}}}, "
    bibtex_entry += f"auteurs = {{{', '.join(authors)}}}"

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
    cur.execute("""SELECT _article.idarticle, nom, url, year, page, doi, ee, pid, _auteur.lastname, _auteur.secondname, _auteur.firstname 
                    FROM _article 
                    JOIN _ecrit ON _ecrit.idarticle = _article.idarticle
                    JOIN _auteur ON _auteur.pid = _ecrit.idauteur
                    ORDER BY _article.idarticle;
                    """)
    rows = cur.fetchall()

    ##récupération des noms de colonnes
    colnames = [desc[0] for desc in cur.description]

    ##fermeture du curseur
    cur.close()

    ##génération des entrées BibTeX pour toutes les lignes de la base de données
    bibTex = ""
    current_id = None
    current_entry_data = []

    for row in rows:
        if current_id != row[0]:
            if current_id is not None:
                bibTex += generate_bibtex_entry(current_entry_data, colnames) + "\n\n"
            current_entry_data = [row]
            current_id = row[0]
        else:
            current_entry_data.append(row)

    if current_entry_data:
        bibTex += generate_bibtex_entry(current_entry_data, colnames) + "\n\n"

    ##écriture des entrées BibTeX dans un fichier
    with open('Bib/bibtex_entries.bib', 'w') as file:
        file.write(bibTex)

    ##fermeture de la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
