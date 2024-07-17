from pydantic import BaseModel

class postProductParam(BaseModel):
    token: str
    id: int