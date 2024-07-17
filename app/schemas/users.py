from pydantic import BaseModel

class LoginQueryParam(BaseModel):
    email: str
    password: str

class RequestData(BaseModel):
    email: str
    password: str
    nickname: str