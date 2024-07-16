from fastapi import APIRouter, HTTPException, Request

from core.security import createToken, validateToken
from pydantic import BaseModel

from core.database import Connect

import bcrypt

router = APIRouter()

class LoginData(BaseModel):
    email:str
    password:str

@router.post("/login")
async def login(data: LoginData):
    requestData = dict(data)
    connection, cursor = await Connect()
    cursor.execute("select * from users where email = %s", (requestData["email"]))
    row = cursor.fetchone()
    try:
        if not row is None:
            if bcrypt.checkpw(requestData["password"].encode('utf-8'), row[2].encode('utf-8')):
                return {
                    "success": True,
                    "token": await createToken(requestData["email"])
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


class TokenData(BaseModel):
    token: str


@router.get("/token")
async def tokens(request: Request):
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

class RequestData(BaseModel):
    email: str
    password: str
    passwordConfirm: str
    nickname: str

@router.post("/register")
async def register(data: RequestData):
    requestData = dict(data)
    connection, cursor = await Connect()
    cursor.execute("select * from users where email = %s", (requestData["email"]))
    row = cursor.fetchone()
    if row is None:
        if not requestData["password"] == requestData["passwordConfirm"]:
            return {
                "result": False,
                "message": "비밀번호 확인과 비밀번호가 일치하지 않습니다."
            }

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
            "result": True
        }
    else:
        connection.close()
        return {
            "result": False,
            "message": "이미 해당 아이디가 존재 합니다."
        }