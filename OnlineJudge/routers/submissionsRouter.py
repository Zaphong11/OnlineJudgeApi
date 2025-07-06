from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.request import SubmissionRequest
from schemas.response import SubmissionResponse, ResultResponse
from models.submission import Submission
from models.result import Result
from db.database import get_db
from utils.isolate_util import IsolateUtil, CompilationError, UnsupportedLanguageError, RuntimeExecutionError

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/submissions", response_model=SubmissionResponse)
async def create_submission(submission: SubmissionRequest, db: db_dependency):
    """Create a new submission and judge it"""

    if not submission.language_id or not submission.code:
        raise HTTPException(status_code=400, detail="Language ID and code are required")
    
    # Lưu submission vào DB với trạng thái pending
    new_submission = Submission(
        language_id=submission.language_id,
        code=submission.code,
        input=submission.input,
        output=submission.output,
        time_limit=submission.time_limit,
        memory_limit=submission.memory_limit,
        status="pending"
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    # Chấm code bằng isolate
    isolate = IsolateUtil()
    try:
        isolate.init_sandbox()
        result = isolate.run_code(
            language_id=submission.language_id,
            source_code=submission.code,
            input_data=submission.input or "",
            time_limit=submission.time_limit / 1000,
            memory_limit=submission.memory_limit,
            db_session=db
        )
        new_submission.status = result.get("status", "judged")
        db.commit()
        db.refresh(new_submission)
    except CompilationError as ce:
        new_submission.status = "compilation_error"
        db.commit()
        db.refresh(new_submission)
        raise HTTPException(status_code=400, detail=f"Compilation error: {str(ce)}")
    except UnsupportedLanguageError as ule:
        new_submission.status = "language_error"
        db.commit()
        db.refresh(new_submission)
        raise HTTPException(status_code=400, detail=f"Unsupported language: {str(ule)}")
    except RuntimeExecutionError as re:
        new_submission.status = "runtime_error"
        db.commit()
        db.refresh(new_submission)
        raise HTTPException(status_code=400, detail=f"Runtime error: {str(re)}")
    except Exception as e:
        new_submission.status = "error"
        db.commit()
        db.refresh(new_submission)
        raise HTTPException(status_code=500, detail=f"Judge error: {str(e)}")
    finally:
        isolate.cleanup()

    result_obj = Result(
        submission_id=new_submission.id,
        status=result.get("status", "judged"),
        time=None,  # bạn có thể lấy thời gian thực thi từ result nếu có
        memory=None,  # bạn có thể lấy memory từ result nếu có
        message=result.get("stderr", ""),  # hoặc stdout tuỳ ý
        output=result.get("output", "")
    )
    db.add(result_obj)
    db.commit()
    db.refresh(result_obj)

    return new_submission

@router.get("/results/{submission_id}", response_model=ResultResponse)
def get_result(submission_id: int, db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.submission_id == submission_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result