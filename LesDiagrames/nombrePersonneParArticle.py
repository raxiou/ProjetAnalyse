import psycopg2

# Fonction pour exécuter les commandes SQL
def execute_sql(connection, cursor, sql_commands):
    try:
        for command in sql_commands:
            cursor.execute(command)
        connection.commit()
        print("Les commandes SQL ont été exécutées avec succès.")
    except psycopg2.Error as e:
        print("Erreur lors de l'exécution des commandes SQL :", e)

# Fonction principale
def main():
    # Paramètres de connexion à la base de données PostgreSQL
    db_params = {
        'dbname': 'analyse',
        'user': 'analyse',
        'password': 'password',
        'host': 'localhost',
        'port': '5432',
        'options': '-c search_path=dbo,bdd'
    }

    # Commandes SQL à exécuter
    sql_commands = [
        "drop schema if exists bdd CASCADE;",
        "create schema bdd;",
        "set schema 'bdd';",
        # Les autres commandes SQL ici
    ]

    # Connexion à la base de données
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Exécution des commandes SQL
        execute_sql(connection, cursor, sql_commands)

        # Fermeture de la connexion
        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        print("Erreur lors de la connexion à la base de données PostgreSQL :", e)

# Point d'entrée du programme
if __name__ == "__main__":
    main()
