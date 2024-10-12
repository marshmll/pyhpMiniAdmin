from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

origins = [
    "http://localhost",
    "http://localhost:3000",
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
