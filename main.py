from database import schemas, database
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.database import SessionLocal, engine
from routers import evidence, process_user, process, request_for_evidence, step, user_step, user, login

database.Base.metadata.create_all(bind=engine)

app = FastAPI(version="5.0.0")

user.create_admin()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique origens específicas
    allow_methods=["*"],  # Ou especifique métodos específicos (GET, POST, etc.)
    allow_headers=["*"],  # Ou especifique cabeçalhos específicos
)

app.include_router(login.router)
app.include_router(evidence.router)
app.include_router(process_user.router)
app.include_router(process.router)
app.include_router(request_for_evidence.router)
app.include_router(step.router)
app.include_router(user_step.router)
app.include_router(user.router)
