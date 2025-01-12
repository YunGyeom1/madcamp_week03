from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, init_db

from app.routes.auth import register_user, login_user
from app.routes.interaction import add_like, stop_listening
from app.routes.search import search_by_tag
from app.db.session import Base, engine
from app.routes.recommend import get_artworks

from app.schemas import (
    UserRegister,
    UserLogin,
    LikeRequest,
    StopListeningRequest
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # DB 세션 종료
        

app = FastAPI()

# 애플리케이션 시작 시 DB 초기화
@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)


# 회원가입
@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Pydantic 스키마 user 안에 email, password 존재
    new_user = register_user(db, user.email, user.password)
    return {"message": "User registered", "user_id": new_user.id}

# 로그인
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = login_user(db, user.email, user.password)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# Like 추가
@app.post("/like")
def like(req: LikeRequest, db: Session = Depends(get_db)):
    add_like(db, req.user_id, req.product_id)
    return {"message": "Like added"}

# 태그 기반 검색
@app.get("/search")
def search(tag: str, db: Session = Depends(get_db)):
    return search_by_tag(db, tag)

# 모든 Artwork 반환
@app.get("/get")
def get_all_artworks(db: Session = Depends(get_db)):
    return get_artworks(db)

# 청취 중지 시 진행률 저장
@app.post("/stop")
def stop(req: StopListeningRequest, db: Session = Depends(get_db)):
    stop_listening(db, req.user_id, req.artwork_id, req.progress)
    return {"message": "Progress saved"}