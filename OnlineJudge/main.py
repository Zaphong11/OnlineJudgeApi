from fastapi import FastAPI
from db.database import Base, engine
from routers import submissionsRouter

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(submissionsRouter.router, prefix="/api", tags=["submissions"])
