from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.request import SubmissionRequest
from schemas.response import SubmissionResponse
from models.submission import Submission
from db.database import get_db

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/submissions", response_model=SubmissionResponse)
async def create_submission(submission: SubmissionRequest, db: db_dependency):
    """create a new submission"""

    if not submission.language_id or not submission.code:
        raise HTTPException(status_code=400, detail="Language ID and code are required")
    
    new_submission = Submission(
        language_id=submission.language_id,
        code=submission.code,
        input=submission.input,
        output=submission.output,
        time_limit=submission.time_limit,
        memory_limit=submission.memory_limit,
        status="pending"
    )
    # Add the new submission to the database
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return new_submission