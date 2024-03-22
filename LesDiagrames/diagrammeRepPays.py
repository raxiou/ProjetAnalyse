import psycopg2
import geopandas as gpd
import matplotlib.pyplot as plt

def clean_country_name(country_name):
    # Retourne le nom de pays nettoyé pour correspondre au format utilisé par geopandas
    country_name = country_name.strip()  # Supprime les espaces en début et en fin de chaîne
    mapping = {
        'USA': 'United States of America',
        'Korea': 'South Korea',
        'Deutschland': 'Germany',
        'Netherlands': 'Netherlands',
        'Brasil': 'Brazil',
        'Japab': 'Japan',
        'Italia': 'Italy',
        'malaysia': 'Malaysia'
        # Ajoutez d'autres mappings si nécessaire
    }
    return mapping.get(country_name, country_name)  # Retourne le mapping si présent, sinon le nom original

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

    # Exécution de la requête pour obtenir les pays
    cur.execute("""Select localisation from _conference;""")
    res = cur.fetchall()
    # Extraction des pays
    pays = []
    for row in res:
        # Séparation ville pays
        row = row[0].split(',')
        pays.append(row[1])

    # Compter le nombre de conférences par pays
    conference_par_pays = {}
    for p in pays:
        p_cleaned = clean_country_name(p)
        if p_cleaned in conference_par_pays:
            conference_par_pays[p_cleaned] += 1
        else:
            conference_par_pays[p_cleaned] = 1

    # Fermeture du curseur
    cur.close()

    # Fermeture de la connexion
    conn.close()

    # Charger les données géographiques des pays
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Joindre les données de la base de données avec les données géographiques
    world['Conference_Count'] = world['name'].map(conference_par_pays)

    # Afficher la carte
    fig, ax = plt.subplots(1, 1)
    ax.set_title('Conference Counts by Country')
    ax.axis('off')
    world.plot(column='Conference_Count', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

    plt.show()

# Point d'entrée du programme
if __name__ == "__main__":
    main()
