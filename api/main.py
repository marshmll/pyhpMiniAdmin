from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from . import crud, models, schemas
from .database import SessionLocal, engine

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/alunos/", response_model=list[schemas.Aluno])
def get_alunos(db: Session = Depends(get_db)):
    alunos = crud.get_all_alunos(db)

    return alunos

@app.get("/professores/", response_model=list[schemas.Professor])
def get_professores(db: Session = Depends(get_db)):
	professores = crud.get_all_professores(db)
	
	return professores

@app.get("/turmas/", response_model=list[schemas.Turma])
def get_turmas(db: Session = Depends(get_db)):
    turmas = crud.get_all_turmas(db)

    return turmas

@app.get("/disciplinas/", response_model=list[schemas.Disciplina])
def get_disciplinas(db: Session = Depends(get_db)):
	disciplinas = crud.get_all_disciplinas(db)
	
	return disciplinas

@app.get("/ministerios/", response_model=list[schemas.Ministerio])
def get_ministerios(db: Session = Depends(get_db)):
	ministerios = crud.get_all_ministerios(db)
	
	return ministerios

@app.get("/aulas/", response_model=list[schemas.Aula])
def get_aulas(db: Session = Depends(get_db)):
	aulas = crud.get_all_aulas(db)
	
	return aulas

@app.get("/salas/", response_model=list[schemas.Sala])
def get_salas(db: Session = Depends(get_db)):
	salas = crud.get_all_salas(db)
	
	return salas

@app.post("/alunos/", response_model=schemas.Aluno)
def create_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    db_aluno = crud.get_aluno_por_matricula(db, aluno.matricula)

    if db_aluno:
        raise HTTPException(status_code=409, detail="Aluno já registrado.")

    return crud.create_aluno(db, aluno)

@app.post("/professores/", response_model=schemas.Professor)
def create_professor(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
	db_professor = crud.get_professor_por_registro(db, professor.reg_profissional)
	
	if db_professor:
		raise HTTPException(status_code=409, detail="Professor já registrado.")
		
	return crud.create_professor(db, professor)

@app.post("/turmas/", response_model=schemas.Turma)
def create_turma(turma: schemas.TurmaCreate, db: Session = Depends(get_db)):
	db_turma = crud.get_turma_por_serie_e_turno(db, turma.serie, turma.turno);
	
	if db_turma:
		raise HTTPException(status_code=409, detail="Turma já registrada.")
		
	return crud.create_turma(db, turma)

@app.post("/disciplinas/", response_model=schemas.Disciplina)
def create_disciplina(disciplina: schemas.DisciplinaCreate, db: Session = Depends(get_db)):
	db_disciplina = crud.get_disciplina_por_nome(db, disciplina.nome);
	
	if db_disciplina:
		raise HTTPException(status_code=409, detail="Disciplina já registrada.")
		
	return crud.create_disciplina(db, disciplina)

@app.post("/ministerios/", response_model=schemas.Ministerio)
def create_ministerio(ministerio: schemas.MinisterioCreate, db: Session = Depends(get_db)):
	db_ministerio = crud.get_ministerio_por_ids(db, ministerio.professor_id, ministerio.turma_id, ministerio.disciplina_id)
	
	if db_ministerio:
		raise HTTPException(status_code=409, detail="Ministério já registrado.")
	
	return crud.create_ministerio(db, ministerio)

@app.post("/aulas/", response_model=schemas.Aula)
def get_aulas(aula: schemas.AulaCreate, db: Session = Depends(get_db)):
	db_aula = crud.get_sala_por_ids_e_datahora(db, aula.sala_id, aula.turma_id, aula.disciplina_id, aula.datahora_inicio)
	
	if db_aula:
		raise HTTPException(status_code=409, detail="Aula já registrada.")
	
	return crud.create_aula(db, aula)

@app.post("/salas/", response_model=schemas.Sala)
def get_salas(sala: schemas.SalaCreate, db: Session = Depends(get_db)):
	db_sala = crud.get_sala_por_bloco_e_num(db, sala.loc_bloco, sala.loc_num)
	
	if db_sala:
		raise HTTPException(status_code=409, detail="Sala já registrada.")
		
	return crud.create_sala(db, sala)

@app.delete("/alunos/")
def delete_aluno(id: int, matricula: int, db: Session = Depends(get_db)):
	rows_affected = crud.delete_aluno(db, id, matricula)

	return rows_affected

@app.delete("/professores/")
def delete_professor(id: int, reg_profissional: int, db: Session = Depends(get_db)):
	rows_affected = crud.delete_professor(db, id, reg_profissional)

	return rows_affected

@app.delete("/turmas/")
def delete_turma(id: int, db: Session = Depends(get_db)):
	rows_affected = crud.delete_turma(db, id)

	return rows_affected

@app.delete("/disciplinas/")
def delete_disciplina(id: int, db: Session = Depends(get_db)):
	rows_affected = crud.delete_disciplina(db, id)

	return rows_affected

@app.delete("/ministerios/")
def delete_ministerio(professor_id: int, turma_id: int, disciplina_id: int, db: Session = Depends(get_db)):
	rows_affected = crud.delete_ministerio(db, professor_id, turma_id, disciplina_id)

	return rows_affected

@app.delete("/aulas/")
def delete_aula(sala_id: int, turma_id: int, disciplina_id: int, datahora_inicio: datetime, db: Session = Depends(get_db)):
	rows_affected = crud.delete_aula(db, sala_id, turma_id, disciplina_id, datahora_inicio)

	return rows_affected

@app.delete("/salas/")
def delete_sala(id: int, db: Session = Depends(get_db)):
	rows_affected = crud.delete_sala(db, id)

	return rows_affected