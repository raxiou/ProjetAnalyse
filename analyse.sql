-- Active: 1707835900493@@localhost@5432@analyse
drop schema if exists bdd CASCADE;
create schema bdd;
set schema 'bdd';

CREATE TABLE _auteur (
    pid VARCHAR(200) ,
    lastname VARCHAR(200),
    secondname VARCHAR(200),
    firstname VARCHAR(200),
    CONSTRAINT auteur_pk PRIMARY KEY (pid)
);

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

CREATE TABLE _revue (
    idArticle BIGINT,
    nom VARCHAR(200),
    vol INT,
    num INT,
    rang VARCHAR(200),
    Constraint revue_pk PRIMARY Key(idArticle)
);

CREATE TABLE _venue (
    idArticle BIGINT,
    nom VARCHAR(200),
    dateDebut DATE,
    dateFin DATE,
    rang VARCHAR(200),
    localisation VARCHAR(300),
    Constraint vevue_pk PRIMARY Key(idArticle)
);

CREATE Table _labo (
    idLabo INT,
    nom VARCHAR(200),
    Constraint  labo_pk PRIMARY KEY(idLabo)
);

CREATE TABLE _travailau (
    idLabo INT,
    idAuteur VARCHAR(200),
    dateDebut DATE,
    dateFin DATE,
    CONSTRAINT travailau_pk PRIMARY KEY (idLabo, idAuteur),
    CONSTRAINT travailau_fk FOREIGN KEY (idLabo) REFERENCES _labo(idLabo),
    CONSTRAINT travailau_fk1 FOREIGN KEY (idAuteur) REFERENCES _auteur(pid)
);

CREATE Table _refere (
    quiRefere BIGINT,
    quiEstRefere BIGINT,
    CONSTRAINT refere_pk PRIMARY KEY(quiRefere, quiEstRefere),
    CONSTRAINT refere_fk FOREIGN KEY (quiRefere) REFERENCES _article(idArticle),
    CONSTRAINT refere_fk1 FOREIGN KEY (quiEstRefere) REFERENCES _article(idArticle)
);

CREATE TABLE _ecrit (
    idArticle BIGINT,
    idAuteur VARCHAR(200),
    CONSTRAINT ecrit_pk PRIMARY KEY (idArticle, idAuteur),
    CONSTRAINT ecrit_fk FOREIGN KEY (idArticle) REFERENCES _article(idArticle),
    CONSTRAINT ecrit_fk1 FOREIGN KEY (idAuteur) REFERENCES _auteur(pid)
);
