from fastapi import APIRouter, Depends, HTTPException
from database import schemas
from sqlalchemy.orm import Session
from models import step_crud, oauth2
from database.database import get_db
from typing import Annotated, Optional

router = APIRouter(tags=["Steps"])


## Etapas rotas


@router.get("/steps/{id}", response_model=Optional[schemas.Step])
def get_step(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para buscar etapa pelo id"""
    return step_crud.get_step(id=id, db=db)

@router.get("/steps/", response_model=Optional[list[schemas.Step]])
def get_all_step(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    db: Session = Depends(get_db),
):
    """Rota para buscar todas as etapa"""
    return step_crud.get_all_step( db=db)


@router.post("/steps/", response_model=Optional[schemas.Step])
def create_step(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    step: schemas.StepCreate,
    db: Session = Depends(get_db),
):
    """Rota para criar uma nova etapa"""
    return step_crud.create_step(db=db, step=step)


@router.put("/steps/", response_model=Optional[schemas.Step])
def update_step(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    step: schemas.Step,
    db: Session = Depends(get_db),
):
    """Rota para alterar etapa pelo id"""
    return step_crud.update_step(step=step, db=db)


@router.delete("/steps/{id}")
def delete_step(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para deletar etapa pelo id"""
    return step_crud.delete_step(id=id, db=db)
