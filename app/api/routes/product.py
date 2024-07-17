from fastapi import APIRouter, HTTPException, Request, Query, Depends, status, Header

from typing import Optional

from app.core.security import createToken, validateToken
from pydantic import BaseModel

from app.core.database import Connect

from app.schemas.product import *

router = APIRouter()

@router.post("/post")
async def 상품_글_작성하기(params: postProductParam):
    data = dict(params)
    token = await validateToken(data["token"])
    if (len(data["token"]) > 0 and token):
        try:
            connection, cursor = await Connect()
            cursor.execute("INSERT INTO products(title, content, delivery, price, tag, image, author) VALUES(%s, %s, %s, %s, %s, %s, %s);", (data["title"], data["content"], data["delivery"], data["price"], data["category"], data["img"], token))
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


@router.post("/products")
async def 상품_목록_불러오기():
    connection, cursor = await Connect()
    cursor.execute("SELECT * FROM products;")
    rows = cursor.fetchall()
    productData = {}
    for i in rows:
        productData[i[0]] = {
             "id": i[0],
            "title": i[1],
            "content": i[2],
            "delivery": i[3],
            "price": i[4],
            "category": i[5],
            "image": i[6],
            "author": i[7]
        }
    connection.close()
    return {
        "success": True,
        "data": productData
    }

@router.post("/products/category")
async def 카테고리로_글_가져오기(params: postProductFromCategory):
    data = dict(params)
    connection, cursor = await Connect()
    cursor.execute("SELECT * FROM products WHERE tag = %s;",(data["category"]))
    rows = cursor.fetchall()
    productData = []
    for i in rows:
        productData.append({
            "id": i[0],
            "title": i[1],
            "content": i[2],
            "delivery": i[3],
            "price": i[4],
            "category": i[5],
            "image": i[6],
            "author": i[7]
        })
    connection.close()
    return {
        "success": True,
        "data": productData
    }

@router.post("/product/id")
async def 상품_아이디로_목록_불러오기(params: postProductFromId):
    data = dict(params)
    connection, cursor = await Connect()
    cursor.execute("SELECT * FROM products WHERE id = %s;", (data["id"]))
    rows = cursor.fetchone()
    connection.close()
    return {
        "success": True,
        "data": {
            "id": rows[0],
            "title": rows[1],
            "content": rows[2],
            "delivery": rows[3],
            "price": rows[4],
            "category": rows[5],
            "image": rows[6],
            "author": rows[7],
        }
    }
