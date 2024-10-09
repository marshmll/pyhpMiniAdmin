from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProfessorBase(BaseModel):
    nome: str
    data_nasc: date
    formacao: str


class ProfessorCreate(ProfessorBase):
    cpf: Optional[str]
    reg_profissional: int


class Professor(ProfessorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
