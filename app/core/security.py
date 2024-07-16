import datetime

import jwt

SECRET_KEY = 'l9s)qu^u4=ofc16+9ap*q!i@yf))8np^7sw*4mts(dji(72)o('


async def createToken(user):
    payload = {
        'user': user,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

async def validateToken(get_token):
    try:
        payload = jwt.decode(get_token, SECRET_KEY, algorithms = 'HS256')
        return payload["user"]
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False