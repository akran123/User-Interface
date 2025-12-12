from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.auth import router as auth_router
from router.meeting import router as meeting_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["*"] (개발 환경에서만)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,prefix="/api")
app.include_router(meeting_router,prefix="/api")
