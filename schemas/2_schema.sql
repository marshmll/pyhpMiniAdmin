CREATE TABLE professores (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    nome VARCHAR(100) NOT NULL, 
    data_nasc DATE NOT NULL, 
    cpf VARCHAR(11), 
    reg_profissional INTEGER NOT NULL, 
    formacao VARCHAR(100) NOT NULL, 
    PRIMARY KEY (id, reg_profissional)
);

CREATE TABLE turmas (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    serie VARCHAR(30) NOT NULL, 
    turno CHAR(1) NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE disciplinas (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    nome VARCHAR(20) NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE salas (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    loc_num INTEGER NOT NULL, 
    loc_bloco VARCHAR(20) NOT NULL, 
    capacidade INTEGER NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE alunos (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    nome VARCHAR(100) NOT NULL, 
    data_nasc DATE NOT NULL, 
    cpf VARCHAR(11), 
    matricula INTEGER NOT NULL, 
    data_matricula DATE NOT NULL, 
    turma_id INTEGER NOT NULL, 
    PRIMARY KEY (id, matricula), 
    FOREIGN KEY(turma_id) REFERENCES turmas (id)
);

CREATE TABLE ministerios (
    professor_id INTEGER NOT NULL, 
    turma_id INTEGER NOT NULL, 
    disciplina_id INTEGER NOT NULL, 
    datavinculo DATETIME NOT NULL, 
    ano INTEGER NOT NULL, 
    PRIMARY KEY (professor_id, turma_id, disciplina_id), 
    FOREIGN KEY(professor_id) REFERENCES professores (id), 
    FOREIGN KEY(turma_id) REFERENCES turmas (id), 
    FOREIGN KEY(disciplina_id) REFERENCES disciplinas (id)
);

CREATE TABLE aulas (
    sala_id INTEGER NOT NULL, 
    turma_id INTEGER NOT NULL, 
    disciplina_id INTEGER NOT NULL, 
    datahora_inicio DATETIME NOT NULL, 
    duracao INTEGER NOT NULL, 
    PRIMARY KEY (sala_id, turma_id, disciplina_id), 
    FOREIGN KEY(sala_id) REFERENCES salas (id), 
    FOREIGN KEY(turma_id) REFERENCES turmas (id), 
    FOREIGN KEY(disciplina_id) REFERENCES disciplinas (id)
);