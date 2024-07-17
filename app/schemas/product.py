from pydantic import BaseModel

class postProductParam(BaseModel):
    token: str
    title: str
    delivery:int
    price:int
    content: str
    img: str
    category: str
