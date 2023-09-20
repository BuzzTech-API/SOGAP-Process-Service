import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from database import schemas
from sqlalchemy.orm import Session
from models import evidence_crud, oauth2, gcs, send_mail
from database.database import get_db
from typing import Annotated, Optional

# mail
from typing import List

from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse


router = APIRouter(tags=["Evidences"])


## Evidencias rotas


@router.get("/evidences/{id}", response_model=Optional[schemas.Evidence])
def get_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para buscar uma evidencia pelo id"""
    return evidence_crud.get_evidence(id=id, db=db)


@router.get("/evidences/", response_model=Optional[list[schemas.Evidence]])
def get_all_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    db: Session = Depends(get_db),
):
    """Rota para buscar todas evidencia"""
    return evidence_crud.get_all_evidence( db=db)


@router.post("/evidences/", response_model=Optional[schemas.Evidence])
def create_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    evidence: schemas.EvidenceCreate,
    db: Session = Depends(get_db),
):

    """Rota para criar uma nova evidencia"""
    return evidence_crud.create_evidence(db=db, evidence=evidence)


@router.put("/evidences/", response_model=Optional[schemas.Evidence])
def update_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    evidence: schemas.Evidence,
    db: Session = Depends(get_db),
):
    """Rota para alterar uma evidencia pelo id"""
    return evidence_crud.update_evidence(evidence=evidence, db=db)


@router.delete("/evidences/{id}")
def delete_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para deletar uma evidencia pelo id"""
    return evidence_crud.delete_evidence(id=id, db=db)

@router.post("/uploadfile/{emails}")
async def create_upload_file(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    emails: str,
    file: UploadFile = File(...)
):
    """Rota para fazer upload de algum arquivo"""
    link = await gcs.GCStorage().upload_file(file) #chama a função que o upload do arquivo para a nuvem

    
    lista_emails = emails.split('&') #pega a string vindo do frontend, separa os emails e adciona em uma lista
    send_mail.EmailSchema = lista_emails

    # mensagem principal que vai chegar no email dos responsáveis
    html = """
    <h5>Processo</h5>
    <br>
    <h5>Dados da evidencia</h5>
    """ 


    message = MessageSchema( #conteudos da mensagem
        subject="Fastapi-Mail module", #
        recipients=send_mail.EmailSchema, #emails
        attachments=[file], #arquivos
        body=html, #mensagem principal
        subtype=MessageType.html)

    fm = FastMail() #função que envia os emails
    await fm.send_message(message)

    if JSONResponse(status_code=200): #retorna o link e uma mensagem avisando que o email foi enviado
        return link, {"email foi enviado"}
    
