from pydantic import BaseModel
from datetime import date
from typing import List

class EvidenceBase(BaseModel):
    link: str
    idRequestForEvidence: int
    deliveryDate: date

class EvidenceCreate(EvidenceBase):
    pass

class Evidence(EvidenceBase):
    id: int

    class Config:
        from_attributes = True


class RequestForEvidenceBase(BaseModel):
    requiredDocument: str
    description: str
    step_id: int
    user_id: int
    evidenceValidationDate: date
    deliveryDate: date
    is_validated: bool
    is_actived: bool

class RequestForEvidenceCreate(RequestForEvidenceBase):
    pass

class RequestForEvidence(RequestForEvidenceBase):
    id: int
    evidences: List[Evidence]

    class Config:
        from_attributes = True


class StepBase(BaseModel):
    name: str
    endDate: date
    endingDate: date
    process_id: int
    objective: str
    priority: str
    order: int
    is_active: bool

class StepCreate(StepBase):
    pass

class Step(StepBase):
    id: int
    requests: List[RequestForEvidence]

    class Config:
        from_attributes = True


class ProcessBase(BaseModel):
    title: str
    objective: str
    endingDate: date
    createDate: date
    lastUpdate: date
    is_active: bool
    priority: str
    status: str

class ProcessCreate(ProcessBase):
    pass


class ProcessUpdate(ProcessBase):
    id: int
    
    class Config:
        from_attributes = True

class Process(ProcessBase):
    id: int
    steps: List[Step]

    class Config:
        from_attributes = True



class UserBase(BaseModel):
    name: str
    email: str
    role: str
    team: str
    is_active: bool

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    

    class Config:
        from_attributes = True





class ProcessUserBase(BaseModel):
    user_id: int
    process_id: int

class ProcessUserCreate(ProcessUserBase):
    pass

class ProcessUser(ProcessUserBase):
    user: User
    process: Process    
    class Config:
        from_attributes = True

class ProcessUserOnlyUser(ProcessUserBase):
    user: User  
    class Config:
        from_attributes = True




class ProcessAll(ProcessBase):
    id: int
    steps: List[Step]
    users: List[ProcessUserOnlyUser]

    class Config:
        from_attributes = True





class UserStepBase(BaseModel):
    user_id: int
    step_id: int

class UserStepCreate(UserStepBase):
    pass

class UserStep(UserStepBase):
    step: Step
    user: User
    class Config:
        from_attributes = True




class UserGet(UserBase):
    id: int
    processes: List[ProcessUser]
    steps: List[UserStep]

    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None
    team: str | None = None

    class Config:
        from_attributes = True