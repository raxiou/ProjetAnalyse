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
    # Commandes SQL à exécuter
    sql_commands = [
        "drop schema if exists bdd CASCADE;",
        "create schema bdd;",
        "set schema 'bdd';",
        """
        CREATE TABLE _auteur (
            pid VARCHAR(200) ,
            lastname VARCHAR(200),
            secondname VARCHAR(200),
            firstname VARCHAR(200),
            CONSTRAINT auteur_pk PRIMARY KEY (pid)
        );
        """,

        """
        CREATE Table _article (
            idArticle SERIAL,
            nom VARCHAR(500),
            url VARCHAR(200),
            year INT,
            Page VARCHAR(200),
            doi VARCHAR(200),
            ee VARCHAR(200),
            CONSTRAINT article_pk PRIMARY KEY (idArticle)
        );
        """,
            
        """
        CREATE TABLE _revue (
            idArticle BIGINT,
            nom VARCHAR(200),
            vol INT,
            num INT,
            rang VARCHAR(200),
            Constraint revue_pk PRIMARY Key(idArticle)
        );
        """,

        """
        CREATE TABLE _venue (
            idArticle BIGINT,
            nom VARCHAR(200),
            dateDebut DATE,
            dateFin DATE,
            rang VARCHAR(200),
            localisation VARCHAR(300),
            Constraint vevue_pk PRIMARY Key(idArticle)
        );
        """,
        """
        CREATE TABLE _conference (
            idConference SERIAL,
            nom VARCHAR(200),
            dateDebut DATE,
            dateFin DATE,
            localisation VARCHAR(200),
            Constraint conference_pk PRIMARY Key(idConference)
        );
        """,

        """
        CREATE Table _refere (
            quiRefere BIGINT,
            quiEstRefere BIGINT,
            CONSTRAINT refere_pk PRIMARY KEY(quiRefere, quiEstRefere),
            CONSTRAINT refere_fk FOREIGN KEY (quiRefere) REFERENCES _article(idArticle),
            CONSTRAINT refere_fk1 FOREIGN KEY (quiEstRefere) REFERENCES _article(idArticle)
        );
        """,

        """
        CREATE TABLE _ecrit (
            idArticle BIGINT,
            idAuteur VARCHAR(200),
            CONSTRAINT ecrit_pk PRIMARY KEY (idArticle, idAuteur),
            CONSTRAINT ecrit_fk FOREIGN KEY (idArticle) REFERENCES _article(idArticle),
            CONSTRAINT ecrit_fk1 FOREIGN KEY (idAuteur) REFERENCES _auteur(pid)
        );
        """
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
