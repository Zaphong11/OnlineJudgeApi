from db.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    version = Column(String, nullable=True)
    judge_key = Column(String, unique=True, nullable=False) 
    file_ext = Column(String, nullable=True)

    submissions = relationship("Submission", back_populates="language")