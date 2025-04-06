from fastapi import FastAPI
from routers import user, login
from database import Base, engine
from pathlib import Path

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(login.router)
