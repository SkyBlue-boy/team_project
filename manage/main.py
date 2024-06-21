from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import crud  # Your existing CRUD operations
import models  # Your existing models
import schemas  # Your existing schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS 설정 추가
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://172.17.67.157:3000",  # user 서버의 IP 주소와 포트 번호 추가
    "http://172.17.67.186:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

class SubmissionRequest(BaseModel):
    username: str
    password: str
    code: str

class SubmissionResponse(BaseModel):
    id: int

class GradeRequest(BaseModel):
    id: int
    status: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submission", response_model=SubmissionResponse)
def create_submission(request: SubmissionRequest, db: Session = Depends(get_db)):
    submission = crud.create_submission(db=db, submission=request)
    return SubmissionResponse(id=submission.id)

@app.get("/new")
def get_new_submission(db: Session = Depends(get_db)):
    submission = crud.get_oldest_submission(db=db)
    if submission:
        crud.update_submission_status(db=db, submission_id=submission.id, status="PROCESSING")
        return {"id": submission.id, "code": submission.code}
    raise HTTPException(status_code=404, detail="No new submissions found")

@app.patch("/submission")
async def update_submission_status(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        logger.info(f"Received PATCH data: {data}")
    except Exception as e:
        logger.error(f"Error parsing JSON: {e}")
        raise HTTPException(status_code=422, detail="Invalid JSON data")

    try:
        grade_request = GradeRequest(**data)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail="Invalid input data")
    
    result = crud.update_submission_status(db=db, submission_id=grade_request.id, status=grade_request.status)
    if not result:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"status": "success"}

@app.get("/submission")
def get_submission(username: str, password: str, id: int, db: Session = Depends(get_db)):
    submission = crud.get_submission(db=db, submission_id=id)
    if submission and submission.username == username and submission.password == password:
        return {
            "id": submission.id,
            "username": submission.username,
            "password": submission.password,
            "created_at": submission.created_at,
            "updated_at": submission.updated_at,
            "status": submission.status
        }
    raise HTTPException(status_code=404, detail="Submission not found or unauthorized")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
