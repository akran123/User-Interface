from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import httpx
from starlette.responses import JSONResponse

router = APIRouter(prefix="/auth", tags=["auth"])


async def saint_auth(student_id: int, password: str) -> str:
    url = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
    headers = {
        "User-Agent": "",
        "Referer": "https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https%3A%2F%2Fsaint.ssu.ac.kr%2FwebSSO%2Fsso.jsp",
    }
    data = {
        "in_tp_bit": "0",
        "rqst_caus_cd": "03",
        "userId": str(student_id),
        "pwd": password,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        print(response)
        response.raise_for_status()
        s_token = response.cookies.get("sToken") # sToken 쿠키

        return s_token

class login(BaseModel) :
    school_number : str
    password : str

@router.post("/login")
async def login(input :login ) :
    student_id = int(input.school_number)
    password = input.password
    token = await saint_auth(student_id, password)
    
    if not token :
        raise HTTPException(status_code=401, detail="정보가 없습니다")
    if student_id == 20242869 :
        return {"name": "김지성"}
    if student_id == 20243069 :
        return {"name" : "이정진"}
    if student_id == 20241682 :
        return {"name" : "신은서"}
    return JSONResponse(status_code=200, content={"token": token})