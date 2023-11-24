from typing import List
from fastapi import UploadFile

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr

from dotenv import dotenv_values

#credenciais
credentials = dotenv_values("./.env")


class EmailSchema(BaseModel):
    email: List[EmailStr]

content = {"Email enviado com sucesso!"}

conf = ConnectionConfig(
    MAIL_USERNAME = credentials['EMAIL'],
    MAIL_PASSWORD = 'apzh jhqd pzrk jivt', #Senha de app dentro de Segurança/Verificação em duas etapas
    MAIL_FROM = credentials['EMAIL'],
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_email(emails: str, file: UploadFile, requestNome: str, processoNome: str, etapaNome: str):
    lista_emails = emails.split('&') #pega a string vindo do frontend, separa os emails e adciona em uma lista
    lista_email_limpa = [i for i in lista_emails if i !='']
    EmailSchema = lista_email_limpa
    
    # mensagem principal que vai chegar no email dos responsáveis
    html = f"""
    <h5>Processo - {processoNome}</h5>
    <br>
    <h5>Etapa - {etapaNome}</h5>
    <br>
    <h5>Dados da evidencia - {requestNome}</h5>
    """ 
    await file.seek(0)
    message = MessageSchema( #conteudos da mensagem
        subject="Evidencia", #titulo do email
        recipients=EmailSchema, #emails
        attachments=[file], #arquivos
        body=html, #mensagem principal
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
