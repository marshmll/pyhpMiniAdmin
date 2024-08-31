from typing import Optional
from sqlalchemy.orm import Session
from . import models, schemas

def get_aluno(db: Session, aluno_id: int):
    return db.query(models.Aluno).filter(models.Aluno.aluno_id == aluno_id).first()

def get_all_alunos(db: Session):
    return db.query(models.Aluno).all()

def get_aluno_por_cpf(db: Session, cpf: Optional[str]):
    return db.query(models.Aluno).filter(models.Aluno.cpf == cpf).first()

def get_professor(db: Session, professor_id: int):
    return db.query(models.Professor).filter(models.Professor.professor_id == professor_id).first()

def get_disciplina(db: Session, nome: str):
    return db.query(models.Disciplina).filter(models.Disciplina.nome == nome).first()

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