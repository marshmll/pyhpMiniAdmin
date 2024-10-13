from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class AlunoBase(BaseModel):
    nome: str
    data_nasc: date
    matricula: int
    data_matricula: date
    turma_id: int
    cpf: Optional[str]

class AlunoCreate(AlunoBase):
	pass

class Aluno(AlunoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ProfessorBase(BaseModel):
    nome: str
    data_nasc: date
    formacao: str
    cpf: Optional[str]
    reg_profissional: int

class ProfessorCreate(ProfessorBase):
	pass

class Professor(ProfessorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class TurmaBase(BaseModel):
	serie: str
	turno: str

class TurmaCreate(TurmaBase):
	pass
	
class Turma(TurmaBase):
	model_config = ConfigDict(from_attributes=True)
	id: int

class DisciplinaBase(BaseModel):
	nome: str

class DisciplinaCreate(DisciplinaBase):
	pass
	
class Disciplina(DisciplinaBase):
	model_config = ConfigDict(from_attributes=True)
	id: int
	
class MinisterioBase(BaseModel):
	datavinculo: datetime
	ano: int
	professor_id: int
	turma_id: int
	disciplina_id: int

class MinisterioCreate(MinisterioBase):
	pass
	
class Ministerio(MinisterioBase):
	model_config = ConfigDict(from_attributes=True)
	
class AulaBase(BaseModel):
	sala_id: int
	turma_id: int
	disciplina_id: int
	datahora_inicio: datetime
	duracao: int
	
class AulaCreate(AulaBase):
	pass
	
class Aula(AulaBase):
	model_config = ConfigDict(from_attributes=True)

class SalaBase(BaseModel):
	loc_num: int
	loc_bloco: str
	capacidade: int
	
class SalaCreate(SalaBase):
	pass
	
class Sala(SalaBase):
	model_config = ConfigDict(from_attributes=True)
	id: int
