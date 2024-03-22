import psycopg2
import matplotlib.pyplot as plt

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

    # Exécution de la requête pour obtenir le nombre d'articles écrits par chaque personne
    cur.execute("""
        SELECT nombre_personnes, COUNT(*) AS nombre_articles
        FROM (
            SELECT idarticle, COUNT(DISTINCT idauteur) AS nombre_personnes
            FROM _ecrit
            GROUP BY idarticle
        ) AS subquery
        GROUP BY nombre_personnes
        ORDER BY nombre_personnes
    """)
    res = cur.fetchall()

    # Fermeture du curseur et de la connexion à la base de données
    cur.close()
    conn.close()

    # Préparation des données pour le graphique
    nombre_personnes = [row[0] for row in res]
    nombre_articles = [row[1] for row in res]

    # Création du graphique à barres
    plt.bar(nombre_personnes, nombre_articles)
    plt.xlabel('Nombre de personnes ayant écrit l\'article')
    plt.ylabel('Nombre d\'articles')
    plt.title('Nombre d\'articles écrits par nombre de personnes')
    plt.xticks(range(min(nombre_personnes), max(nombre_personnes)+1))  # Étiquettes pour chaque nombre de personnes
    plt.tight_layout()  # Ajustement automatique de la disposition pour éviter la superposition du texte
    plt.show()

if __name__ == "__main__":
    main()
