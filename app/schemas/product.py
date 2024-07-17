from pydantic import BaseModel

class postProductParam(BaseModel):
    token: str
    title: str
    price:int
    content: str
    img: str
    category: str

class getParam(BaseModel):
    token: str

class getDetailParam(BaseModel):
    token: str