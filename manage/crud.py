from sqlalchemy.orm import Session
from models import Submission
from schemas import SubmissionRequest
from datetime import datetime

def create_submission(db: Session, submission: SubmissionRequest):
    db_submission = Submission(
        username=submission.username,
        password=submission.password,
        code=submission.code,
        status="SUBMITTED",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def get_oldest_submission(db: Session):
    return db.query(Submission).filter(Submission.status == "SUBMITTED").order_by(Submission.created_at).first()

def update_submission_status(db: Session, submission_id: int, status: str):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if submission:
        submission.status = status
        submission.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

def get_submission(db: Session, submission_id: int):
    return db.query(Submission).filter(Submission.id == submission_id).first()
