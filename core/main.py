from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/alunos/", response_model=schemas.Aluno)
def create_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    db_aluno = crud.get_aluno_por_cpf(db, aluno.cpf)

    if db_aluno:
        raise HTTPException(status_code=400, detail="Aluno já registrado.")

    return crud.create_aluno(db, aluno)

@app.get("/alunos/", response_model=list[schemas.Aluno])
def get_alunos(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    alunos = crud.get_all_alunos(db)

    return alunos