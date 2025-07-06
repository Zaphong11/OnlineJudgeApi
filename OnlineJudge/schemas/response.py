from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class SubmissionResponse(BaseModel):
    id: int
    language_id: int
    code: str
    input: Optional[str] = None
    output: Optional[str] = None
    time_limit: int
    memory_limit: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ResultResponse(BaseModel):
    id: int
    submission_id: int
    status: str
    time: Optional[int]
    memory: Optional[int]
    message: Optional[str]
    output: Optional[str]

    class Config:
        from_attributes = True