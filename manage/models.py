from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)  # 길이 지정
    password = Column(String(50))  # 길이 지정
    code = Column(String(1000))  # 길이 지정
    status = Column(String(20), default="SUBMITTED")  # 길이 지정
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
