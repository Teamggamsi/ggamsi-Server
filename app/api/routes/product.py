from fastapi import APIRouter, HTTPException, Request, Query, Depends, status, Header

from typing import Optional

from app.core.security import createToken, validateToken
from pydantic import BaseModel

from app.core.database import Connect

router = APIRouter()


class postProductParam(BaseModel):
    token: str
    title: str
    price:int
    content: str
    img: str
    category: str


@router.post("/post")
async def 상품_글_작성하기(params: postProductParam):
    data = dict(params)
    token = await validateToken(data["token"])
    if (len(data["token"]) > 0 and token):
        try:
            connection, cursor = await Connect()
            cursor.execute("INSERT INTO products(title, content, price, tag, image, author) VALUES(%s, %s, %s, %s, %s, %s);", (data["title"], data["content"], data["price"], data["category"], data["img"], token))
            connection.commit()
            connection.close()
            return {
                "success": True
            }
        except Exception as e:
            print(e)
            return {
                "success": False,
                "message": "서버에서 오류가 발생하였습니다."
            }
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰이 유호하지 않습니다.")

class getParam(BaseModel):
    token: str


@router.get("/products")
async def 상품_목록_불러오기(params: getParam):
    data = dict(params)
    token = await validateToken(data["token"])
    if (len(data["token"]) > 0 and token):
        try:
            connection, cursor = await Connect()
            cursor.execute("SELECT * FROM products;")
            rows = cursor.fetchall()
            productData = {}
            for i in rows:
                productData[i[0]] = {
                    "id": i[0],
                    "title": i[1],
                    "content": i[2],
                    "price": i[3],
                    "category": i[4],
                    "image": i[5],
                    "author": i[6],
                }
            connection.close()
            return {
                "success": True,
                "data": productData
            }
        except Exception as e:
            print(e)
            return {
                "success": False,
                "message": "서버에서 오류가 발생하였습니다."
            }
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰이 유호하지 않습니다.")
    

@router.get("/products/{category}")
async def 카테고리로_글_가져오기(category:str, params: getParam):
    data = dict(params)
    token = await validateToken(data["token"])
    if (len(data["token"]) > 0 and token):
        try:
            connection, cursor = await Connect()
            cursor.execute("SELECT * FROM products WHERE tag = %s;",(category))
            rows = cursor.fetchall()
            productData = {}
            for i in rows:
                productData[i[0]] = {
                    "id": i[0],
                    "title": i[1],
                    "content": i[2],
                    "price": i[3],
                    "category": i[4],
                    "image": i[5],
                    "author": i[6],
                }
            connection.close()
            return {
                "success": True,
                "data": productData
            }
        except Exception as e:
            print(e)
            return {
                "success": False,
                "message": "서버에서 오류가 발생하였습니다."
            }
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰이 유호하지 않습니다.")    

class getDetailParam(BaseModel):
    token: str

@router.get("/product/{id}")
async def 상품_아이디로_목록_불러오기(id: str, params: getDetailParam):
    data = dict(params)
    token = await validateToken(data["token"])
    if (len(data["token"]) > 0 and token):
        try:
            connection, cursor = await Connect()
            cursor.execute("SELECT * FROM products WHERE id = %s;", (id))
            rows = cursor.fetchone()
            cursor.execute("SELECT * FROM likes WHERE article = %s;", (id))
            likeRows = cursor.fetchall()
            cursor.execute("SELECT * FROM likes WHERE article = %s and author = %s;", (id, token))
            likeRow = cursor.fetchone()
            connection.close()
            return {
                "success": True,
                "data": {
                    "id": rows[0],
                    "title": rows[1],
                    "content": rows[2],
                    "price": rows[3],
                    "category": rows[4],
                    "image": rows[5],
                    "is_liked": (not likeRow == None),
                    "likes": len(likeRows),
                    "author": rows[6],
                }
            }
        except Exception as e:
            print(e)
            return {
                "success": False,
                "message": "서버에서 오류가 발생하였습니다."
            }
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰이 유호하지 않습니다.")

