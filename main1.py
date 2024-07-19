from fastapi import FastAPI
from .database import engine
from .import schema, models, Sessionlocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app=FastAPI()

models.Base.metadata.crete_all(engine)

def get_db():
    db=Sessionlocal()
    try:
        yield db

    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post('/user')
def new_user(request:schema.new_user, db:Session):
    hashedPassword = pwd_context.hash(request.password)
    new_user= models.User(name=request.name,password=hashedPassword, email=request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

