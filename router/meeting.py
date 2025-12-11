from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid

# 라우터 설정 (사용자가 제공한 코드)
router = APIRouter(prefix="/meeting", tags=["meeting"])

# 1. 이미지를 저장할 로컬 디렉토리 설정
# 프로젝트 루트 경로에 'uploaded_images' 폴더가 생성됩니다.
UPLOAD_DIR = "uploaded_images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)



@router.post("/upload")
async def upload_meeting_photo(file: UploadFile = File(...)):
    try:
        # 파일명 중복 방지를 위해 UUID 사용 (예: a1b2c3... .jpg)
        # file.filename에서 확장자(.jpg, .png 등)만 추출하여 붙입니다.
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # 저장할 전체 경로
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # 서버 디스크에 파일 쓰기
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 클라이언트가 나중에 이미지를 요청할 수 있도록 파일명을 반환
        return {
            "message": "Upload successful",
            "filename": unique_filename,
            "download_url": f"/api/meeting/images/{unique_filename}"  # 아래 GET API 경로
        }

    except Exception as e:
        return {"error": str(e)}


# --- [API 2] 사진 불러오기 (Download/View) ---
@router.get("/images/{filename}")
async def get_meeting_photo(filename: str):
    # 요청받은 파일명의 실제 경로 찾기
    file_path = os.path.join(UPLOAD_DIR, filename)

    # 파일이 존재하는지 확인
    if os.path.exists(file_path):
        # FileResponse를 사용하면 이미지를 직접 반환합니다 (브라우저에서 바로 보임)
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")

