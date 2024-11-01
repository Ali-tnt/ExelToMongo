from pydantic import BaseModel, Field
from typing import Optional

class PhoneNumber(BaseModel):
    mobile: str = Field(..., description="Phone number")

class PhoneNumberUpdate(BaseModel):
    mobile: Optional[str] = Field(None, description="New phone number")

class ProcessingResult(BaseModel):
    total_records: int
    processing_time: float
    success: bool
    message: str