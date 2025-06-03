from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

"""
create a submission request schema
"""

class SubmissionRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "language_id": 1,
                "code": "print('Hello, World!')",
                "input": "None",
                "output": "None",
                "time_limit": 1000,  # in milliseconds
                "memory_limit": 256   # in MB
            }
        },
        from_attributes=True
    )

    language_id: int = Field(..., description="ID of the programming language used for the submission")
    code: str = Field(..., description="Source code of the submission")
    input: Optional[str] = Field(None, description="Input data for the submission, if applicable")
    output: Optional[str] = Field(None, description="Expected output for the submission, if applicable")
    time_limit: int = Field(
        default=1000,  # 1 second in milliseconds
        ge=500,        # minimum 500ms (0.5 seconds)
        le=5000,       # maximum 5000ms (5 seconds)
        description="Time limit for the submission in milliseconds"
    )
    
    memory_limit: int = Field(
        default=256,
        ge=64,         # minimum 64 MB
        le=512,        # maximum 512 MB
        description="Memory limit for the submission in MB"
    )
