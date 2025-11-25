CREATE DATABASE IF NOT EXISTS imdb DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE imdb;

CREATE TABLE genero (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE ator (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE filme (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    duracao VARCHAR(10),
    ano SMALLINT,
    classificacao_etaria VARCHAR(10)
);

CREATE TABLE ranking (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    nota DECIMAL(3, 1),
    posicao INT NOT NULL,
    data DATE NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id)
);

CREATE TABLE genero_filme (
    id_filme INT NOT NULL,
    id_genero INT NOT NULL,
    PRIMARY KEY (id_filme, id_genero),
    FOREIGN KEY (id_filme) REFERENCES filme(id) ON DELETE CASCADE,
    FOREIGN KEY (id_genero) REFERENCES genero(id) ON DELETE CASCADE
);

CREATE TABLE elenco (
    id_ator INT NOT NULL,
    id_filme INT NOT NULL,
    PRIMARY KEY (id_ator, id_filme),
    FOREIGN KEY (id_ator) REFERENCES ator(id) ON DELETE CASCADE,
    FOREIGN KEY (id_filme) REFERENCES filme(id) ON DELETE CASCADE
);