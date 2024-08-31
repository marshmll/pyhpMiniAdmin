from pydantic import BaseModel
from datetime import date
from typing import Optional

# Base is the shared data.
class AlunoBase(BaseModel):
    nome: str
    data_nasc: date
    matricula: int
    data_matricula: date
    turma_id: int

# Create is the sensible data 
class AlunoCreate(AlunoBase):
    cpf: Optional[str]

# The standard class is for reading data.
class Aluno(AlunoBase):
    id: int

    class Config:
        orm_mode = True


class ProfessorBase(BaseModel):
    nome: str
    data_nasc: date
    formacao: str


class ProfessorCreate(ProfessorBase):
    cpf: Optional[str]
    reg_profissional: int


class Professor(ProfessorBase):
    id: int

    class Config:
        orm_mode = True