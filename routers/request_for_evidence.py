from fastapi import APIRouter, Depends, HTTPException
from database import schemas
from sqlalchemy.orm import Session
from models import request_for_evidence_crud, oauth2
from database.database import get_db
from typing import Annotated, Optional

router = APIRouter(tags=["Request_For_Evidence"])


## Pedidos De Evidencia rotas


@router.get("/request_for_evidence/{id}", response_model=Optional[schemas.RequestForEvidence])
def get_request_for_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para buscar o pedido de evidencia pelo id"""
    return request_for_evidence_crud.get_request_for_evidence(id=id, db=db)

@router.get("/request_for_evidence/", response_model=Optional[list[schemas.RequestForEvidence]])
def get_all_request_for_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    db: Session = Depends(get_db),
):
    """Rota para buscar o pedido de evidencia pelo id"""
    return request_for_evidence_crud.get_all_request_for_evidence( db=db)


@router.post("/request_for_evidence/", response_model=Optional[schemas.RequestForEvidence])
def create_request_for_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    request_for_evidence: schemas.RequestForEvidenceCreate,
    db: Session = Depends(get_db),
):
    """Rota para criar um pedido de evidencia pelo id"""
    return request_for_evidence_crud.create_request_for_evidence(
        db=db, request_for_evidence=request_for_evidence
    )


@router.put("/request_for_evidence/", response_model=Optional[schemas.RequestForEvidence])
def update_request_for_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    request_for_evidence: schemas.RequestForEvidence,
    db: Session = Depends(get_db),
):
    """Rota para alterar o pedido de evidencia pelo id"""
    return request_for_evidence_crud.update_request_for_evidence(
        request_for_evidence=request_for_evidence, db=db
    )


@router.delete("/request_for_evidence/{id}")
def delete_request_for_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para deletar o pedido de evidencia pelo id"""
    return request_for_evidence_crud.delete_request_for_evidence(id=id, db=db)
