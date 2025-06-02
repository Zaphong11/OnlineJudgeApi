import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    code = Column(String, nullable=False)
    input = Column(String, nullable=True)
    output = Column(String, nullable=True)
    time_limit = Column(Integer, nullable=False, default=2)
    memory_limit = Column(Integer, nullable=False, default=256)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    
    language = relationship("Language", back_populates="submissions")
    results = relationship("Result", back_populates="submission", cascade="all, delete-orphan")
