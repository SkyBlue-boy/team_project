from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class SubmissionRequest(BaseModel):
    username: str
    password: str
    code: str

class SubmissionResponse(BaseModel):
    id: int

class GradeRequest(BaseModel):
    id: int
    status: str


class Submission(BaseModel):
    id: int
    username: str
    password: str
    code: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode: True
