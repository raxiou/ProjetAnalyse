import csv
import requests
import psycopg2


def get_csv_data(file_path):
    # Ouvrir le fichier CSV en mode lecture
    with open(file_path, 'r') as file:
        # Créer un lecteur CSV
        csv_reader = csv.reader(file)
        # Lire les données du fichier CSV
        data = [row for row in csv_reader]
    return data

def main():
    # Connexion à la base de données
    conn = psycopg2.connect(dbname="analyse",
                            user="analyse",
                            password="password",
                            host="localhost",
                            port="5432",
                            options="-c search_path=dbo,bdd")

    # Ouverture d'un curseur pour effectuer des opérations de base de données
    cur = conn.cursor()

    # Récupérer les données du fichier CSV
    data = get_csv_data('baseDeDonnee/conf.csv')
    print(data[0])
    #['MTD', 'Honolulu, USA', '2011-05-23', '2011-05-23', '']

    # Exécution de la requête pour insérer les données dans la table _conference
    for row in data:
        cur.execute(f"INSERT INTO _conference (nom, dateDebut, dateFin, localisation) VALUES ('{row[0]}', '{row[2]}', '{row[3]}', '{row[1]}');")
        conn.commit()
        print("Insertion réussie")
    
    # Fermeture du curseur
    cur.close()

    # Fermeture de la connexion
    conn.close()

# Point d'entrée du programme
if __name__ == "__main__":
    main()

