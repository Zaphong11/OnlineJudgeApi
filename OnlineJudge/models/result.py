import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from db.database import Base
from sqlalchemy.orm import relationship

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    output = Column(String, nullable=True)
    status = Column(String, nullable=False)
    time = Column(Integer, nullable=True)
    memory = Column(Integer, nullable=True)
    message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    submission = relationship("Submission", back_populates="results")