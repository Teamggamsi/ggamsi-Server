from fastapi import APIRouter, HTTPException, Request, Query, Depends

from app.core.security import createToken, validateToken
from pydantic import BaseModel

from app.core.database import Connect

import bcrypt

from app.schemas.users import *

router = APIRouter()

@router.post("/login")
async def 로그인(LoginQueryParam: LoginQueryParam):
    data = dict(LoginQueryParam)
    connection, cursor = await Connect()
    cursor.execute("select * from users where email = %s", (data["email"]))
    row = cursor.fetchone()
    try:
        if not row is None:
            if bcrypt.checkpw(data["password"].encode('utf-8'), row[2].encode('utf-8')):
                return {
                    "success": True,
                    "token": await createToken(row[3])
                }
            else:
                return {
                    "success":False,
                    "message": "비밀번호가 올바르지 않습니다."
                }
        else:
            return {
                "success": False,
                "message": "아이디가 존재하지 않습니다."
            }
    except Exception as e:
        return {
            "success": False,
            "message": "서버에서 오류가 발생하였습니다."
        }

@router.get("/token")
async def 토큰으로_유저정보_불러오기(request: Request):
    authorization = request.headers.get('Authorization')
    tokenData = await validateToken(authorization)
    if tokenData:
        connection, cursor = await Connect()
        cursor.execute("select * from users where email = %s", (tokenData))
        row = cursor.fetchone()

        return {
            "success": True,
            "user": tokenData,
            "userName": row[3]
        }
    else:
        return {
            "success": False,
            "user": None,
            "userName": None,
        }

@router.post("/register")
async def 회원기입(data: RequestData):
    connection, cursor = await Connect()
    requestData = dict(data)
    cursor.execute("select * from users where email = %s", (requestData["email"]))
    row = cursor.fetchone()
    if row is None:
    
        cursor.execute("select * from users where nickname = %s", (requestData["nickname"]))
        row = cursor.fetchone()

        if not row is None:
            return {
                "result": False,
                "message": "이미 해당 닉네임이 존재합니다."
            }
        password = requestData["password"].encode("utf-8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
        cursor.execute("INSERT INTO users(email, password, nickname) VALUES(%s, %s, %s);", (requestData["email"], hashed, requestData["nickname"]))
        connection.commit()
        connection.close()
        return {
            "result": True,
            "token": await createToken(requestData["nickname"])
        }
    else:
        connection.close()
        return {
            "result": False,
            "message": "이미 해당 아이디가 존재 합니다."
        }