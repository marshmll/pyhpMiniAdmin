from datetime import date, datetime
from typing import Optional
from sqlalchemy.orm import Session
from . import models, schemas

def get_aluno(db: Session, aluno_id: int):
    return db.query(models.Aluno).filter(models.Aluno.aluno_id == aluno_id).first()

def get_aluno_por_matricula(db: Session, matricula: int):
    return db.query(models.Aluno).filter(models.Aluno.matricula == matricula).first()

def get_all_alunos(db: Session):
    return db.query(models.Aluno).all()

def get_professor(db: Session, professor_id: int):
    return db.query(models.Professor).filter(models.Professor.professor_id == professor_id).first()

def get_professor_por_registro(db: Session, reg_profissional: int):
	return db.query(models.Professor).filter(models.Professor.reg_profissional == reg_profissional).first()

def get_all_professores(db: Session):
	return db.query(models.Professor).all()

def get_turma_por_serie_e_turno(db: Session, serie: str, turno: str):
	return db.query(models.Turma).filter(models.Turma.serie == serie, models.Turma.turno == turno).first()

def get_all_turmas(db: Session):
	return db.query(models.Turma).all()

def get_disciplina_por_nome(db: Session, nome: str):
	return db.query(models.Disciplina).filter(models.Disciplina.nome == nome).first()

def get_all_disciplinas(db: Session):
	return db.query(models.Disciplina).all()

def get_ministerio_por_ids(db: Session, professor_id: int, turma_id: int, disciplina_id: int):
	return db.query(models.Ministerio).filter(models.Ministerio.professor_id == professor_id, models.Ministerio.turma_id == turma_id, models.Ministerio.disciplina_id == disciplina_id).first()

def get_all_ministerios(db: Session):
	return db.query(models.Ministerio).all()

def get_sala_por_ids_e_datahora(db: Session, sala_id: int, turma_id: int, disciplina_id: int, datahora_inicio: datetime):
	return db.query(models.Aula).filter(models.Aula.sala_id == sala_id, models.Aula.turma_id == turma_id, models.Aula.disciplina_id == disciplina_id, models.Aula.datahora_inicio == datahora_inicio).first()

def get_all_aulas(db: Session):
	return db.query(models.Aula).all()

def get_sala_por_bloco_e_num(db: Session, loc_bloco: str, loc_num: int):
	return db.query(models.Sala).filter(models.Sala.loc_bloco == loc_bloco, models.Sala.loc_num == loc_num).first()

def get_all_salas(db: Session):
	return db.query(models.Sala).all()

def create_aluno(db: Session, aluno: schemas.AlunoCreate):
    db_aluno = models.Aluno(
        nome=aluno.nome,
        data_nasc=aluno.data_nasc,
        cpf = aluno.cpf,
        matricula=aluno.matricula,
        data_matricula=aluno.data_matricula,
        turma_id=aluno.turma_id,
    )
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def create_professor(db: Session, professor: schemas.ProfessorCreate):
    db_professor = models.Professor(
        nome=professor.nome,
        data_nasc=professor.data_nasc,
        cpf = professor.cpf,
        reg_profissional=professor.reg_profissional,
        formacao=professor.formacao,
    )
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

def create_turma(db: Session, turma: schemas.TurmaCreate):
    db_turma = models.Turma(
    	serie=turma.serie,
    	turno=turma.turno,
    )
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    return db_turma

def create_disciplina(db: Session, disciplina: schemas.DisciplinaCreate):
    db_disciplina = models.Disciplina(
    	nome=disciplina.nome,
    )
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina

def create_ministerio(db: Session, ministerio: schemas.MinisterioCreate):
	db_ministerio = models.Ministerio(
		professor_id=ministerio.professor_id,
		turma_id=ministerio.turma_id,
		disciplina_id=ministerio.disciplina_id,
		datavinculo=ministerio.datavinculo,
		ano=ministerio.ano,
	)
	db.add(db_ministerio)
	db.commit()
	db.refresh(db_ministerio)
	return db_ministerio

def create_aula(db: Session, aula: schemas.AulaCreate):
	db_aula = models.Aula(
		sala_id=aula.sala_id,
		turma_id=aula.turma_id,
		disciplina_id=aula.disciplina_id,
		datahora_inicio=aula.datahora_inicio,
		duracao=aula.duracao,
	)
	db.add(db_aula)
	db.commit()
	db.refresh(db_aula)
	return db_aula

def create_sala(db: Session, sala: schemas.SalaCreate):
	db_sala = models.Sala(
		loc_num=sala.loc_num,
		loc_bloco=sala.loc_bloco,
		capacidade=sala.capacidade,
	)
	db.add(db_sala)
	db.commit()
	db.refresh(db_sala)
	return db_sala
