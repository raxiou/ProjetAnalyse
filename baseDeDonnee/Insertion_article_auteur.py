import json
import requests
import psycopg2

def get_api():
    # récupère les données de l'API
    api_url = "https://dblp.org/search/publ/api?q=Atomic Charge&format=json&h=200"
    response = requests.get(api_url)

    if response.status_code == 200:
        print("ok")
        contenu = response.json()
        return contenu
    else:
        print("pas bon")
        return False
  
def get_api2():
    # récupère les données de l'API
    api_url = "https://api.crossref.org/works/?filter=doi:10.1109/DEXA.2007.11"
    response = requests.get(api_url)

    if response.status_code == 200:
        print("ok")
        contenu = response.json()
        return contenu
    else:
        print("pas bon")
        return False

def main():
    # Mettre le contenu de test.json dans apelleApi
    with open('baseDeDonnee/test.json', 'r') as f:
        apelleApi = json.load(f)

    ## connexion à une base de données
    conn = psycopg2.connect(dbname="analyse",
                            user="analyse",
                            password="password",
                            host="localhost",
                            port="5432",
                            options="-c search_path=dbo,bdd")

    ## ouverture d'un curseur pour effectuer des opérations de base de données
    cur = conn.cursor()

    longueur = len(apelleApi["result"]["hits"]["hit"])

    for i in range(0, longueur):
        def get_Author(n=0):
            return apelleApi["result"]["hits"]["hit"][n]["info"]["authors"]["author"]

        def get_article(n=0):
            return apelleApi["result"]["hits"]["hit"][n]["info"]

        data = get_Author(i)
        pidL = []
        for n in range(1, len(data)):
            # séparation nom et prénom
            if isinstance(data, list):
                name = data[n]["text"].split(" ")
                pid = data[n]["@pid"]
            else:
                name = data["text"].split(" ")
                pid = data["@pid"]
        
            if len(name) == 2:
                name.append(name[1])
                name[1] = "null"
            pidL.append(pid)
            try:
                # Vérifier si l'auteur existe déjà dans la base de données
                cur.execute("SELECT COUNT(*) FROM _auteur WHERE pid = %s", (pid,))
                result = cur.fetchone()
                if result[0] == 0:
                    # Si l'auteur n'existe pas, l'insérer dans la base de données
                    cur.execute("INSERT INTO _auteur (pid, lastname, secondname, firstname) VALUES (%s, %s, %s, %s)", (pid, name[0], name[1], name[2]))
                    conn.commit()
                    print("Insertion réussie")
                else:
                    print("L'auteur existe déjà dans la base de données")
            except Exception as e:
                print(e)

        conn.commit()
   
        data = get_article(i)

        # préparation des données
        if "doi" in data:
            data["doi"] = data["doi"]
        else:
            data["doi"] = "null"

        if "ee" in data:
            data["ee"] = data["ee"]
        else:
            data["ee"] = "null"
        
        if "pages" in data:
            data["pages"] = data["pages"]
        else:
            data["pages"] = "null"

        # insertion des données dans la base de données
        cur.execute("INSERT INTO _article (nom, url, year, Page, doi, ee) VALUES (%s, %s, %s, %s, %s, %s) RETURNING idarticle", (data["title"], data["url"], data["year"], data["pages"], data["doi"], data["ee"]))
        res = cur.fetchall()

        conn.commit()
        for row in res:
            idArticle = res[0][0]

        ## ajout des personne et des article dans la table association
        print(f"idArticle :{idArticle}, PID:{pidL}")
        
        for pid in pidL:
            cur.execute("INSERT INTO _ecrit(idarticle, idauteur) VALUES(%s, %s)", (idArticle, pid))
        
        conn.commit()

    ## fermeture du curseur
    cur.close()

    ## fermeture de la connexion
    conn.close()

if __name__ == "__main__":
    main()
