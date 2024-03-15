from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, EmailStr, validator
import re

from sqlalchemy import String, Column, Integer, Identity, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

#Creación de la conexión a la bd
engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")


#Creación de la APP
app = FastAPI()

#Modelo de usuario con pydantic
class User(BaseModel):
    name: str
    email: str
    #Se añade validación de All fields required [400]
    @validator("name", "email")
    def validate_not_empty(cls, value):
        if value == "":
            raise HTTPException(status_code=400, detail="All fields are required")
        return value
    @validator("email")
    def valid_email(cls, value):
        if not email_regex.match(value):
            raise HTTPException(status_code=400, detail="El email no es válido")
        return value


class Base(DeclarativeBase):
    pass

#Modelo de usuario con sqlalchemy
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)


# El puntero para crear tablas en la bd
Base.metadata.create_all(engine)


#Expresión regular para el Email
email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

#Endpoint root/índice
@app.get("/")
def root():
    return {"Message": "Hola, este es el índice"}


#Endpoint all users
@app.get("/all")
def get_users():
    with Session(engine) as session:
        usuarios = session.query(Users).all()
        return usuarios

#Endpoint get user
@app.get("/user/{id}")
def get_user(id: int):
    with Session(engine) as session:
        query = select(Users).where(Users.id == id)
        usuario = session.execute(query).scalars().all()
        if usuario:
            return usuario[0]
        raise HTTPException(status_code=404, detail="User not found")
    
#Endpoint create user
@app.post("/users")
def set_user(data: User):
    with Session(engine) as session:
        usuario= Users(name=data.name, email=data.email)
        session.add(usuario)
        session.commit()
        return {"Message":"User was created succesfully"}
    
#Endpoint update user
@app.put("/user/{id}")
def modify_user(id:int, data:User):
    with Session(engine) as session:
        query = select(Users).where(Users.id == id)
        usuario = session.execute(query).scalars().all()
        if not usuario:
            raise HTTPException(status_code=404, detail="User not found")
        usuario[0].name = data.name
        usuario[0].email = data.email

        session.commit()
        return {"Message": "User updated"}
    
@app.delete("/user/{id}")
def delete_user(id:int):
    with Session(engine) as session:
        query = select(Users).where(Users.id == id)
        usuario = session.execute(query).scalars().all()
        if not usuario:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(usuario[0])
        session.commit()
        return {"Message":"User deleted successfully"}
