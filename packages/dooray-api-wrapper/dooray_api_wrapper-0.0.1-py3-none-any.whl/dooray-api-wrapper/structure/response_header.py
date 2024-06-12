from pydantic import BaseModel


class ResponseHeader(BaseModel):
    isSuccessful: bool
    resultCode: int
    resultMessage: str
