from datetime import datetime
from sqlalchemy import update
from sqlalchemy.orm import Session
from . import models, schemas

# "SELECT WHERE" queries =========================================================================================
def get_aluno_por_matricula(db: Session, matricula: int):
    return db.query(models.Aluno).filter(models.Aluno.matricula == matricula).first()

def get_professor_por_registro(db: Session, reg_profissional: int):
    return db.query(models.Professor).filter(models.Professor.reg_profissional == reg_profissional).first()

def get_turma_por_serie_e_turno(db: Session, serie: str, turno: str):
    return db.query(models.Turma).filter(models.Turma.serie == serie, models.Turma.turno == turno).first()

def get_disciplina_por_nome(db: Session, nome: str):
    return db.query(models.Disciplina).filter(models.Disciplina.nome == nome).first()

def get_ministerio_por_ids(db: Session, professor_id: int, turma_id: int, disciplina_id: int):
    return db.query(models.Ministerio).filter(
        models.Ministerio.professor_id == professor_id,
        models.Ministerio.turma_id == turma_id,
        models.Ministerio.disciplina_id == disciplina_id
    ).first()

def get_aula_por_ids_e_datahora(db: Session, sala_id: int, turma_id: int, disciplina_id: int, datahora_inicio: datetime):
    return db.query(models.Aula).filter(
        models.Aula.sala_id == sala_id,
        models.Aula.turma_id == turma_id,
        models.Aula.disciplina_id == disciplina_id,
        models.Aula.datahora_inicio == datahora_inicio
    ).first()

def get_sala_por_bloco_e_num(db: Session, loc_bloco: str, loc_num: int):
    return db.query(models.Sala).filter(models.Sala.loc_bloco == loc_bloco, models.Sala.loc_num == loc_num).first()


# "SELECT *" queries =============================================================================================
def get_all_alunos(db: Session):
    return db.query(models.Aluno).all()

def get_all_professores(db: Session):
    return db.query(models.Professor).all()

def get_all_turmas(db: Session):
    return db.query(models.Turma).all()

def get_all_disciplinas(db: Session):
    return db.query(models.Disciplina).all()

def get_all_ministerios(db: Session):
    return db.query(models.Ministerio).all()

def get_all_aulas(db: Session):
    return db.query(models.Aula).all()

def get_all_salas(db: Session):
    return db.query(models.Sala).all()


# "INSERT" queries
def create_aluno(db: Session, aluno: schemas.AlunoCreate):
    db.begin()
    db_aluno = models.Aluno(
        nome=aluno.nome,
        data_nasc=aluno.data_nasc,
        cpf=aluno.cpf,
        matricula=aluno.matricula,
        data_matricula=aluno.data_matricula,
        turma_id=aluno.turma_id,
    )
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def create_professor(db: Session, professor: schemas.ProfessorCreate):
    db.begin()
    db_professor = models.Professor(
        nome=professor.nome,
        data_nasc=professor.data_nasc,
        cpf=professor.cpf,
        reg_profissional=professor.reg_profissional,
        formacao=professor.formacao,
    )
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

def create_turma(db: Session, turma: schemas.TurmaCreate):
    db.begin()
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
    db.begin()
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
    db.begin()
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
    db.begin()
    db_sala = models.Sala(
        loc_num=sala.loc_num,
        loc_bloco=sala.loc_bloco,
        capacidade=sala.capacidade,
    )
    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)
    return db_sala


# "UPDATE WHERE" queries =========================================================================================
def update_aluno(db: Session, aluno: schemas.Aluno):
    db.begin()
    stmt = (
        update(models.Aluno)
        .where(models.Aluno.id == aluno.id)
        .values(
            nome=aluno.nome,
            data_nasc=aluno.data_nasc,
            cpf=aluno.cpf,
            matricula=aluno.matricula
        )
    )

    db.execute(stmt)
    db.commit()
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno.id).first()
    return db_aluno

def update_professor(db: Session, professor: schemas.Professor):
    db.begin()
    stmt = (
        update(models.Professor)
        .where(models.Professor.id == professor.id)
        .values(
            nome=professor.nome,
            data_nasc=professor.data_nasc,
            cpf=professor.cpf,
            reg_profissional=professor.reg_profissional
        )
    )

    db.execute(stmt)
    db.commit()
    db_professor = db.query(models.Professor).filter(models.Professor.id == professor.id).first()
    return db_professor

def update_turma(db: Session, turma: schemas.Turma):
    db.begin()
    stmt = (
        update(models.Turma)
        .where(models.Turma.id == turma.id)
        .values(
            serie=turma.serie,
            turno=turma.turno
        )
    )
    db.execute(stmt)
    db.commit()
    db_turma = db.query(models.Turma).filter(models.Turma.id == turma.id).first()
    return db_turma

def update_disciplina(db: Session, disciplina: schemas.Disciplina):
    db.begin()
    stmt = (
        update(models.Disciplina)
        .where(models.Disciplina.id == disciplina.id)
        .values(
            nome=disciplina.nome
        )
    )

    db.execute(stmt)
    db.commit()
    db_disciplina = db.query(models.Disciplina).filter(models.Disciplina.id == disciplina.id).first()
    return db_disciplina

def update_ministerio(db: Session, ministerio: schemas.Ministerio):
    db.begin()
    stmt = (
        update(models.Ministerio)
        .where(
            models.Ministerio.professor_id == ministerio.professor_id,
            models.Ministerio.turma_id == ministerio.turma_id,
            models.Ministerio.disciplina_id == ministerio.disciplina_id
        )
        .values(
            professor_id=ministerio.professor_id,
            turma_id=ministerio.turma_id,
            disciplina_id=ministerio.disciplina_id,
            datavinculo=ministerio.datavinculo,
            ano=ministerio.ano
        )
    )

    db.execute(stmt)
    db.commit()
    db_ministerio = get_ministerio_por_ids(db, ministerio.professor_id, ministerio.turma_id, ministerio.disciplina_id)
    return db_ministerio

def update_aula(db: Session, aula: schemas.Aula):
    db.begin()
    stmt = (
        update(models.Aula)
        .where(
            models.Aula.sala_id == aula.sala_id,
            models.Aula.turma_id == aula.turma_id,
            models.Aula.disciplina_id == aula.disciplina_id,
            models.Aula.datahora_inicio == aula.datahora_inicio,
        )
        .values(
            sala_id=aula.sala_id,
            turma_id=aula.turma_id,
            disciplina_id=aula.disciplina_id,
            datahora_inicio=aula.datahora_inicio,
            duracao=aula.duracao
        )
    )

    db.execute(stmt)
    db.commit()
    db_aula = get_aula_por_ids_e_datahora(db, aula.sala_id, aula.turma_id, aula.disciplina_id, aula.datahora_inicio)
    return db_aula

def update_sala(db: Session, sala: schemas.Sala):
    db.begin()
    stmt = (
        update(models.Sala)
        .where(models.Sala.id == sala.id)
        .values(
            loc_num=sala.loc_num,
            loc_bloco=sala.loc_bloco,
            capacidade=sala.capacidade
        )
    )

    db.execute(stmt)
    db.commit()
    db_sala = db.query(models.Sala).filter(models.Sala.id == sala.id).first()
    return db_sala

# "DELETE WHERE" queries =========================================================================================
def delete_aluno(db: Session, id: int, matricula: int):
    db.begin()
    rows_affected = db.query(models.Aluno).filter(models.Aluno.id == id, models.Aluno.matricula == matricula).delete()
    db.commit()
    return rows_affected

def delete_professor(db: Session, id: int, reg_profissional: int):
    db.begin()
    rows_affected = db.query(models.Professor).filter(
        models.Professor.id == id,
        models.Professor.reg_profissional == reg_profissional
    ).delete()
    db.commit()
    return rows_affected

def delete_turma(db: Session, id: int):
    db.begin()
    rows_affected = db.query(models.Turma).filter(models.Turma.id == id).delete()
    db.commit()
    return rows_affected

def delete_disciplina(db: Session, id: int):
    db.begin()
    rows_affected = db.query(models.Disciplina).filter(models.Disciplina.id == id).delete()
    db.commit()
    return rows_affected

def delete_ministerio(db: Session, professor_id: int, turma_id: int, disciplina_id: int):
    db.begin()
    rows_affected = db.query(models.Ministerio).filter(
        models.Ministerio.professor_id == professor_id,
        models.Ministerio.turma_id == turma_id,
        models.Ministerio.disciplina_id == disciplina_id
    ).delete()
    db.commit()
    return rows_affected

def delete_aula(db: Session, sala_id: int, turma_id: int, disciplina_id: int, datahora_inicio: datetime):
    v
    rows_affected = db.query(models.Aula).filter(
        models.Aula.sala_id == sala_id,
        models.Aula.turma_id == turma_id,
        models.Aula.disciplina_id == disciplina_id,
        models.Aula.datahora_inicio == datahora_inicio
    ).delete()
    db.commit()
    return rows_affected

def delete_sala(db: Session, id: int):
    db.begin()
    rows_affected = db.query(models.Sala).filter(models.Sala.id == id).delete()
    db.commit()
    return rows_affected
