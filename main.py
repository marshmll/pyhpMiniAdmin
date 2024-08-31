from datetime import date
from datetime import datetime
from typing import *
from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine("sqlite://", echo=True)

def main():
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        turma = Turma(
            id=1,
            serie="3 medio B",
            turno="M"
        )

        session.add(turma)
        session.commit()

        renan = Aluno(
            nome="Renan Andrade",
            data_nasc=date(2006, 7, 24),
            cpf="12345678901",
            matricula=12983192783,
            data_matricula=date.today(),
            turma_id=turma.id
        )

        session.add(renan)
        session.commit()

        stmt = select(Aluno)

        for pessoa in session.scalars(stmt):
            print(pessoa)


class Base(DeclarativeBase):
    pass


class Pessoa(Base):
    __tablename__ = "pessoas"

    id : Mapped[int] = mapped_column(primary_key=True)
    nome : Mapped[str] = mapped_column(String(100))
    data_nasc : Mapped[date] = mapped_column(Date)
    cpf : Mapped[Optional[str]] = mapped_column(String(11))
    type : Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "pessoa",
        "polymorphic_on": "type",
    }

    alunos : Mapped[Optional[Set["Aluno"]]] = relationship(
        back_populates="pessoa", cascade="all, delete-orphan"
    )

    professores : Mapped[Optional[Set["Professor"]]] = relationship(
        back_populates="pessoa", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Pessoa(id={self.id!r}, nome={self.nome!r}, cpf={self.cpf!r})"


class Turma(Base):
    __tablename__ = "turmas"

    id : Mapped[int] = mapped_column(primary_key=True)
    serie : Mapped[str] = mapped_column(String(30))
    turno : Mapped[str] = mapped_column(CHAR(1))

    ministerios : Mapped[Set["Ministerio"]] = relationship(
        back_populates="turma", cascade="all, delete-orphan"
    )

    aulas : Mapped[Optional[Set["Aula"]]] = relationship(
        back_populates="turma", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Turma(id={self.id!r}, serie={self.serie!r}, turno={self.turno!r})"


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id : Mapped[int] = mapped_column(primary_key=True)
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

    id : Mapped[int] = mapped_column(primary_key=True)
    loc_num : Mapped[int] = mapped_column(Integer)
    loc_bloco : Mapped[str] = mapped_column(String(20))
    capacidade : Mapped[int] = mapped_column(Integer)

    aulas : Mapped[Optional["Aula"]] = relationship(
        back_populates="sala", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Sala(id={self.id!r}, loc_num={self.loc_num!r}, loc_bloco={self.loc_bloco!r}, capacidade={self.capacidade!r})"


class Aluno(Pessoa):
    __tablename__ = "alunos"

    pessoa_id : Mapped[int] = mapped_column(ForeignKey("pessoas.id"), primary_key=True)
    matricula : Mapped[int] = mapped_column(Integer, primary_key=True)
    data_matricula : Mapped[date] = mapped_column(Date)
    turma_id : Mapped[int] = mapped_column(ForeignKey("turmas.id"))

    __table_args__ = (
        UniqueConstraint("pessoa_id"),
    )

    __mapper_args__ = {
        "polymorphic_identity": "aluno",
    }

    pessoa : Mapped["Pessoa"] = relationship(
        back_populates="alunos",
    )

    def __repr__(self):
        return f"Aluno(pessoa_id={self.id!r}, nome={self.nome!r}, cpf={self.cpf!r}, matricula={self.matricula!r}, turma_id={self.turma_id!r})"


class Professor(Pessoa):
    __tablename__ = "professores"

    pessoa_id : Mapped[int] = mapped_column(ForeignKey("pessoas.id"), primary_key=True)
    reg_profissional : Mapped[int] = mapped_column(Integer, primary_key=True)
    formacao : Mapped[str] = mapped_column(String(100))

    pessoa : Mapped["Pessoa"] = relationship(back_populates="professores")
    ministerios : Mapped[Optional[Set["Ministerio"]]] = relationship(
        back_populates="professor", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("pessoa_id"),
    )

    __mapper_args__ = {
        "polymorphic_identity": "professor",
    }

    def __repr__(self):
        return f"Professor(pessoa_id={self.id!r}, nome={self.nome!r}, cpf={self.cpf!r}, reg_profissional={self.reg_profissional!r}, formacao={self.formacao!r})"

class Ministerio(Base):
    __tablename__ = "ministerios"

    professor_id : Mapped[int] = mapped_column(ForeignKey("professores.pessoa_id"), primary_key=True)
    turma_id : Mapped[int] = mapped_column(ForeignKey("turmas.id"), primary_key=True)
    disciplina_id : Mapped[int] = mapped_column(ForeignKey("disciplinas.id"), primary_key=True)
    datavinculo : Mapped[datetime] = mapped_column(DateTime)
    ano : Mapped[int] = mapped_column(Integer)

    professor : Mapped["Professor"] = relationship(back_populates="ministerios")
    turma : Mapped["Turma"] = relationship(back_populates="ministerios")
    disciplina : Mapped["Disciplina"] = relationship(back_populates="ministerios")

    def __repr__(self):
        return f"Ministerio(professor_id={self.professor_id!r}, turma_id={self.turma_id!r}, disciplina_id={self.disciplina_id!r}, datavinculo={self.datavinculo!r}, ano={self.ano!r}"


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
        return f"Aula(sala_id={self.sala_id!r}, turma_id={self.turma_id!r}, disciplina_id={self.disciplina_id!r}, datahora_inicio={self.datahora_inicio!r}, duracao={self.duracao!r})"

if __name__ == "__main__":
    main()