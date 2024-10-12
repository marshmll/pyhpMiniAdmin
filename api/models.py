from sqlalchemy.orm import declarative_base
from datetime import date, datetime
from typing import Optional, Set
from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, UniqueConstraint, CHAR 
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()

class Aluno(Base):
    __tablename__ = "alunos"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome : Mapped[str] = mapped_column(String(100))
    data_nasc : Mapped[date] = mapped_column(Date)
    cpf : Mapped[Optional[str]] = mapped_column(String(11))
    matricula : Mapped[int] = mapped_column(Integer, primary_key=True)
    data_matricula : Mapped[date] = mapped_column(Date)
    turma_id : Mapped[int] = mapped_column(ForeignKey("turmas.id"))

    turma : Mapped["Turma"] = relationship(
        back_populates="alunos",
    )

    def __repr__(self):
        return f"Aluno(id={self.id!r}, nome={self.nome!r}, cpf={self.cpf!r}, matricula={self.matricula!r}, turma_id={self.turma_id!r})"


class Professor(Base):
    __tablename__ = "professores"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome : Mapped[str] = mapped_column(String(100))
    data_nasc : Mapped[date] = mapped_column(Date)
    cpf : Mapped[Optional[str]] = mapped_column(String(11))
    reg_profissional : Mapped[int] = mapped_column(Integer, primary_key=True)
    formacao : Mapped[str] = mapped_column(String(100))

    ministerios : Mapped[Optional[Set["Ministerio"]]] = relationship(
        back_populates="professor", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Professor(id={self.id!r}, nome={self.nome!r}, cpf={self.cpf!r}, reg_profissional={self.reg_profissional!r}, formacao={self.formacao!r})"


class Turma(Base):
    __tablename__ = "turmas"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    serie : Mapped[str] = mapped_column(String(30))
    turno : Mapped[str] = mapped_column(CHAR(1))

    ministerios : Mapped[Set["Ministerio"]] = relationship(
        back_populates="turma", cascade="all, delete-orphan"
    )

    aulas : Mapped[Optional[Set["Aula"]]] = relationship(
        back_populates="turma", cascade="all, delete-orphan"
    )

    alunos : Mapped[Optional[Set["Aluno"]]] = relationship(
        back_populates="turma",
    )

    def __repr__(self) -> str:
        return f"Turma(id={self.id!r}, serie={self.serie!r}, turno={self.turno!r})"


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome : Mapped[str] = mapped_column(String(20))

    ministerios : Mapped[Optional[Set["Ministerio"]]] = relationship(
        back_populates="disciplina", cascade="all, delete-orphan"
    )

    aulas : Mapped[Optional[Set["Aula"]]] = relationship(
        back_populates="disciplina", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Disciplina(id={self.id!r}, nome={self.nome!r})"


class Sala(Base):
    __tablename__ = "salas"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    loc_num : Mapped[int] = mapped_column(Integer)
    loc_bloco : Mapped[str] = mapped_column(String(20))
    capacidade : Mapped[int] = mapped_column(Integer)

    aulas : Mapped[Optional["Aula"]] = relationship(
        back_populates="sala", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Sala(id={self.id!r}, loc_num={self.loc_num!r}, loc_bloco={self.loc_bloco!r}, capacidade={self.capacidade!r})"



class Ministerio(Base):
    __tablename__ = "ministerios"

    professor_id : Mapped[int] = mapped_column(ForeignKey("professores.id"), primary_key=True)
    turma_id : Mapped[int] = mapped_column(ForeignKey("turmas.id"), primary_key=True)
    disciplina_id : Mapped[int] = mapped_column(ForeignKey("disciplinas.id"), primary_key=True)
    datavinculo : Mapped[datetime] = mapped_column(DateTime)
    ano : Mapped[int] = mapped_column(Integer)

    professor : Mapped["Professor"] = relationship(back_populates="ministerios")
    turma : Mapped["Turma"] = relationship(back_populates="ministerios")
    disciplina : Mapped["Disciplina"] = relationship(back_populates="ministerios")

    def __repr__(self):
        return f"Ministerio(professor_id={self.professor_id!r}, turma_id={self.turma_id!r}, disciplina_id={self.disciplina_id!r}, datavinculo={self.datavinculo.strftime('%d/%m/%Y, %H:%M:%S')!r}, ano={self.ano!r})"


class Aula(Base):
    __tablename__ = "aulas"

    sala_id : Mapped[int] = mapped_column(ForeignKey("salas.id"), primary_key=True)
    turma_id : Mapped[int] = mapped_column(ForeignKey("turmas.id"), primary_key=True)
    disciplina_id : Mapped[int] = mapped_column(ForeignKey("disciplinas.id"), primary_key=True)
    datahora_inicio : Mapped[datetime] = mapped_column(DateTime)
    duracao : Mapped[int] = mapped_column(Integer)

    sala : Mapped["Sala"] = relationship(back_populates="aulas")
    turma : Mapped["Turma"] = relationship(back_populates="aulas")
    disciplina : Mapped["Disciplina"] = relationship(back_populates="aulas")

    def __repr__(self):
        return f"Aula(sala_id={self.sala_id!r}, turma_id={self.turma_id!r}, disciplina_id={self.disciplina_id!r}, datahora_inicio={self.datahora_inicio.strftime('%d/%m/%Y, %H:%M:%S')!r}, duracao={self.duracao!r})"
