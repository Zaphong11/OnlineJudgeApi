from fastapi import FastAPI
from db.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)
