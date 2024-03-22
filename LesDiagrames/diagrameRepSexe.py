import psycopg2
import gender_guesser.detector as gender
import matplotlib.pyplot as plt
import json

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

    # Exécution de la requête pour obtenir les prénoms
    cur.execute("""SELECT firstname, lastname, secondname FROM _auteur;""")
    res = cur.fetchall()

    # Extraction des prénoms
    prenoms = []
    for row in res:
        if len(row[1]) != 2:
            prenoms.append(row[1])
        elif len(row[2]) != 2:
            prenoms.append(row[2])

    # Fonction pour obtenir le sexe à partir du prénom
    def get_gender_from_firstname(firstname):
        detector = gender.Detector()
        ret = detector.get_gender(firstname)
        return ret

    # Associer les prénoms à leur sexe
    prenoms_sexe = {}

    for prenom in prenoms:
        try:
            sexe = get_gender_from_firstname(prenom)
        except Exception as e:
            print(e)
            print(f"problème avec {prenom}")
            sexe = "unknown"
        prenoms_sexe[prenom] = sexe

    # Chemin vers le fichier où vous souhaitez enregistrer le dictionnaire
    chemin_fichier = "prenoms_sexe.json"

    # Enregistrer le dictionnaire dans le fichier JSON
    with open(chemin_fichier, 'w') as f:
        json.dump(prenoms_sexe, f)

    print("Dictionnaire enregistré avec succès dans le fichier:", chemin_fichier)


    # Charger le dictionnaire à partir du fichier JSON
    chemin_fichier = "prenoms_sexe.json"
    with open(chemin_fichier, 'r') as f:
        prenoms_sexe = json.load(f)


    # Compter le nombre de prénoms associés à chaque sexe
    comptage_sexe = {"male": 0, "female": 0, "unknown": 0}
    for sexe in prenoms_sexe.values():
        if sexe == "male":
            comptage_sexe["male"] += 1
        elif sexe == "female":
            comptage_sexe["female"] += 1
        else:
            comptage_sexe["unknown"] += 1

    # Générer le camembert de répartition
    labels = ['Male', 'Female']
    sizes = [comptage_sexe["male"], comptage_sexe["female"]]
    colors = ['blue', 'purple']

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equalise l'aspect ratio pour s'assurer que le camembert est circulaire
    plt.title('Répartition des sexes parmi les prénoms')
    plt.show()

if __name__ == "__main__":
    main()
