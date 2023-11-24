from models import request_for_evidence_crud, step_crud, process_crud
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from database import schemas
from sqlalchemy.orm import Session
from models import evidence_crud, oauth2, gcs, send_mail
from database.database import get_db
from typing import Annotated, Optional

#email
from fastapi_mail import FastMail, MessageSchema, MessageType


router = APIRouter(tags=["Evidences"])


## Evidencias rotas


@router.get("/evidences/{id}", response_model=Optional[schemas.Evidence])
async def get_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para buscar uma evidencia pelo id"""
    return evidence_crud.get_evidence(id=id, db=db)


@router.get("/evidences", response_model=Optional[list[schemas.Evidence]])
async def get_all_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    db: Session = Depends(get_db),
):
    """Rota para buscar todas evidencia"""
    return evidence_crud.get_all_evidence( db=db)


@router.post("/evidences/", response_model=Optional[schemas.Evidence])
async def create_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    evidence: schemas.EvidenceCreate,
    db: Session = Depends(get_db),
):

    """Rota para criar uma nova evidencia"""
    return evidence_crud.create_evidence(db=db, evidence=evidence)


@router.put("/evidences/", response_model=Optional[schemas.Evidence])
async def update_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    evidence: schemas.Evidence,
    db: Session = Depends(get_db),
):
    """Rota para alterar uma evidencia pelo id"""
    return evidence_crud.update_evidence(evidence=evidence, db=db)


@router.delete("/evidences/{id}")
async def delete_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para deletar uma evidencia pelo id"""
    return evidence_crud.delete_evidence(id=id, db=db)

@router.put("/evidences/invalidate/{id}")
async def invalidate_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para deletar uma evidencia pelo id"""
    return evidence_crud.invalidate_evidence(id=id, db=db)

@router.post("/uploadfile/{emails}/{idRequest}")
async def create_upload_file(
    background_tasks: BackgroundTasks,
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    emails: str,
    idRequest: int,
    db: Session = Depends(get_db),
    file: UploadFile = File(...)
): 
    """Rota para fazer upload de algum arquivo"""

    try:

        request = request_for_evidence_crud.get_request_for_evidence(db=db, id=idRequest)
        step = step_crud.get_step(db=db, id=request.step_id)
        process = process_crud.get_process(db=db, id=step.process_id)
        
        link = await gcs.GCStorage().upload_file(file) #chama a função que o upload do arquivo para a nuvem

        background_tasks.add_task(send_mail.send_email, emails, file, request.requiredDocument, process.title, step.name)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

    return link #retorna o link e uma mensagem avisando que o email foi enviado