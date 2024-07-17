from fastapi import APIRouter, HTTPException, Request, Query, Depends, status, Header


from app.core.security import createToken, validateToken
from pydantic import BaseModel

from app.core.database import Connect

from app.schemas.like import *

router = APIRouter()

@router.put("/add")
async def 좋아요_추가히기(params: postProductParam):
    data = dict(params)
    token = await validateToken(data["token"])
    if (len(data["token"]) > 0 and token):
        try:
            connection, cursor = await Connect()
            cursor.execute("INSERT INTO likes(article, author) VALUES(%s, %s);", (data["id"], token))
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

@router.delete("/delete")
async def 좋아요_삭제하기(params: postProductParam):
    data = dict(params)
    token = await validateToken(data["token"])
    if (len(data["token"]) > 0 and token):
        try:
            connection, cursor = await Connect()
            cursor.execute("DELETE FROM likes WHERE id = %s and author = %s;", (data["id"], token))
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
