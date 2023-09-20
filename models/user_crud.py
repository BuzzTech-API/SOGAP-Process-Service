from sqlalchemy.orm import Session
from database import schemas
from database.database import Base, get_db
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from typing import List
from models import process_crud, step_crud, process_user_crud, user_step_crud


class User(Base):

    """Aqui é criado a tabela de Usuario que será iniciada no banco
    aqui tem todos os seus atributos além de 2 campos extras que ajudam na hora de fazer as buscas no banco que são os
    relationship retorna uma lista de item, o process é classe ProcessUser e o steps é da classe StepUser
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(60))
    email = Column(String(64), unique=True, index=True)
    password = Column(String(64))
    role = Column(String(60))
    team = Column(String(60))
    is_active = Column(Boolean, default=True)
    processes: Mapped[List[process_user_crud.ProcessUser]] = relationship(
        back_populates="user"
    )
    steps: Mapped[List[user_step_crud.UserStep]] = relationship(back_populates="user")


def get_user(db: Session, id: int):
    """Recebe uma sessão do banco e id e realiza a busca no banco, retornando esse usuário"""
    return db.query(User).filter(User.id == id).first()


def get_user_by_email(db: Session, email: str):
    """Recebe uma sessão do banco e email e realiza a busca no banco, retornando o usuário com esse email"""
    return db.query(User).filter(User.email == email).first()


def get_all_user(db: Session, skip: int = 0, limit: int = 100):
    """Recebe uma sessão do banco, podendo ser utilizando skip e o limit para paginação, por padrão ele busca na tabela usuarios e pega os 100 primeiros usuarios e retorna eles"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """Recebe uma sessão do banco e a class UserCreate com os dados de criação de um Usuário e adiciona no banco e salva as alteraçãos e atualiza o db_user atribuindo a ele o id que foi gerado no banco e retorna ele com o id dele"""
    db_user = User(
        email=user.email,
        name=user.name,
        password=user.password,
        role=user.role,
        team=user.team,
        is_active=user.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.User):
    """Recebe uma sessão do banco e o Usuario completo para alteração, primeiro ele chega se aquele usuário existe no banco depois altera todos os campos com o que recebeu do esquema e atualiza o db_user e retorna ele"""
    db_user = db.query(User).filter(User.id == user.id).first()

    if db_user:
        db_user.email = user.email
        db_user.name = user.name
        db_user.password = user.password
        db_user.cargo = user.cargo
        db_user.team = user.team
        db_user.is_active = user.is_active

        db.commit()
        db.refresh(db_user)

    return db_user


def delete_user(db: Session, id: int):
    """Recebe o sessão do banco e o id do usuario a ser deletado, primeiro realiza a busca dele no banco, se ele existir, o deleta e salva a alteração no banco"""
    db_user = db.query(User).filter(User.id == id).first()

    if db_user:
        db.delete(db_user)
        db.commit()

    return db_user
