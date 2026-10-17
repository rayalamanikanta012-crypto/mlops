from pydantic import BaseModel, Field, field_validator


class EmailRequest(BaseModel):
    subject: str = Field(default="", max_length=500)
    body: str = Field(..., max_length=20000)

    @field_validator("body")
    @classmethod
    def body_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Email body must not be empty")
        return v


class PredictionResponse(BaseModel):
    label: str
    is_spam: bool
    spam_probability: float
    confidence: float
