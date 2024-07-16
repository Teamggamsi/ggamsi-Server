from fastapi import APIRouter, HTTPException, Request, Query, Depends

from app.core.security import createToken, validateToken
from pydantic import BaseModel

from app.core.database import Connect

import bcrypt

router = APIRouter()


class LoginQueryParam:
    def __init__(
        self,
        email: str = Query(..., description="이메일"),
        password: str = Query(..., description="비밀번호"),
    ):
        self.email = email
        self.password = password


@router.post("/login")
async def login(params: LoginQueryParam = Depends()):
    connection, cursor = await Connect()
    cursor.execute("select * from users where email = %s", (params.email))
    row = cursor.fetchone()
    try:
        if not row is None:
            if bcrypt.checkpw(params.password.encode('utf-8'), row[2].encode('utf-8')):
                return {
                    "success": True,
                    "token": await createToken(params.email)
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

class RequestData:
    def __init__(
        self,
        email: str = Query(..., description="이메일"),
        password: str = Query(..., description="비밀번호"),
        passwordConfirm: str = Query(..., description="비밀번호 확인"),
        nickname: str = Query(..., description="닉네임"),
    ):
        self.email = email
        self.password = password
        self.passwordConfirm = passwordConfirm
        self.nickname = nickname


@router.post("/register")
async def register(data: RequestData = Depends()):
    connection, cursor = await Connect()
    cursor.execute("select * from users where email = %s", (data.email))
    row = cursor.fetchone()
    if row is None:
        if not data.password == data.passwordConfirm:
            return {
                "result": False,
                "message": "비밀번호 확인과 비밀번호가 일치하지 않습니다."
            }

        cursor.execute("select * from users where nickname = %s", (data.nickname))
        row = cursor.fetchone()

        if not row is None:
            return {
                "result": False,
                "message": "이미 해당 닉네임이 존재합니다."
            }
        password = data.password.encode("utf-8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
        cursor.execute("INSERT INTO users(email, password, nickname) VALUES(%s, %s, %s);", (data.email, hashed, data.nickname))
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