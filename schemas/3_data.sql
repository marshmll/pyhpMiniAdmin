INSERT INTO professores (nome, data_nasc, cpf, reg_profissional, formacao) VALUES
('João Silva', '1980-05-14', '12345678901', 1001, 'Matemática'),
('Maria Santos', '1975-09-20', '23456789012', 1002, 'História'),
('Carlos Pereira', '1983-12-11', '34567890123', 1003, 'Biologia'),
('Ana Souza', '1990-03-25', '45678901234', 1004, 'Física'),
('Pedro Martins', '1987-07-08', '56789012345', 1005, 'Química');

INSERT INTO turmas (serie, turno) VALUES
('1º Ano', 'M'),
('2º Ano', 'T'),
('3º Ano', 'M'),
('4º Ano', 'T'),
('5º Ano', 'M');

INSERT INTO disciplinas (nome) VALUES
('Matemática'),
('História'),
('Biologia'),
('Física'),
('Química');

INSERT INTO salas (loc_num, loc_bloco, capacidade) VALUES
(101, 'A', 30),
(102, 'A', 30),
(201, 'B', 40),
(202, 'B', 40),
(301, 'C', 50);

INSERT INTO alunos (nome, data_nasc, cpf, matricula, data_matricula, turma_id) VALUES
('Lucas Oliveira', '2010-06-15', '78901234567', 2001, '2023-02-10', 1),
('Mariana Costa', '2009-03-22', '89012345678', 2002, '2023-02-10', 2),
('Felipe Almeida', '2008-08-11', '90123456789', 2003, '2023-02-10', 3),
('Julia Ferreira', '2007-11-30', '01234567890', 2004, '2023-02-10', 4),
('Renato Lima', '2011-01-17', '12345678091', 2005, '2023-02-10', 5);

INSERT INTO ministerios (professor_id, turma_id, disciplina_id, datavinculo, ano) VALUES
(1, 1, 1, '2023-01-15 08:00:00', 2023),
(2, 2, 2, '2023-01-16 09:00:00', 2023),
(3, 3, 3, '2023-01-17 10:00:00', 2023),
(4, 4, 4, '2023-01-18 11:00:00', 2023),
(5, 5, 5, '2023-01-19 12:00:00', 2023);

INSERT INTO aulas (sala_id, turma_id, disciplina_id, datahora_inicio, duracao) VALUES
(1, 1, 1, '2023-03-01 08:00:00', 60),
(2, 2, 2, '2023-03-02 09:00:00', 60),
(3, 3, 3, '2023-03-03 10:00:00', 60),
(4, 4, 4, '2023-03-04 11:00:00', 60),
(5, 5, 5, '2023-03-05 12:00:00', 60);
