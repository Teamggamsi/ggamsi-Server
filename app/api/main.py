from fastapi import APIRouter

from app.api.routes import product,upload,like, users

api_router = APIRouter()

api_router.include_router(users.router, tags=["회원가입/로그인"])
api_router.include_router(product.router, tags=["상품 게시"], prefix="/product")
api_router.include_router(like.router, tags=["상품 좋아요"], prefix="/like")
api_router.include_router(upload.router, tags=["이미지 파일 서버"], prefix="/cdn")