from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

import urllib, secrets, io
from boto3 import client

from PIL import Image, ImageOps
from pathlib import Path


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "images"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


Image.ANTIALIAS = Image.LANCZOS


def resize_image(file: UploadFile):
    read_image = Image.open(file.file)
    read_image = read_image.resize((512, 512))
 
    read_image = read_image.convert("RGB")
    read_image = ImageOps.exif_transpose(read_image)
    return read_image
 
def save_image_to_filesystem(image: Image, file_path: str):
    image.save(file_path, "jpeg", quality=70)
    return file_path

@router.put("/upload")
async def 이미지_업로드(file: UploadFile = File(...)):
    image = resize_image(file)
    tokens = secrets.token_hex(12)
    image = save_image_to_filesystem(image, f"{UPLOAD_DIR}/{tokens}.jpeg")        
    return {"file": f"{tokens}"}

@router.get("/images/{filename}")
async def 이미지_불러오기(filename: str):
    file_location = UPLOAD_DIR / f"{filename}.jpeg"
    if file_location.exists():
        return FileResponse(file_location)
        
    return HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
