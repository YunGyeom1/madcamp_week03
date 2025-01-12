# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import Base
from app.db.models import Base, User, UserActivity, Artwork, ArtTag, Like 
from app.db.session import init_db, SessionLocal, engine
from app.db.confest import create_user, create_artwork, create_art_tag, create_user_activity  # 함수 임포트

# TestClient를 사용하는 fixture
@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    
# 테스트용 DB 초기화 fixture
@pytest.fixture(scope="function")
def test_db():
    # DB 세션 생성
    db = SessionLocal()
    try:
        # 메모리 DB 초기화 (테이블 생성)
        Base.metadata.create_all(bind=engine)  # 메모리 DB에서 테이블 생성
        yield db
    finally:
        # DB 세션 종료
        db.close()
        # 테스트 후 DB 테이블 삭제
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def saved_user(client, test_db):
    # 회원가입 요청
    response = client.post("/register", json={"email": "testuser@example.com", "password": "1234"})
    assert response.status_code == 200
    assert response.json()["message"] == "User registered"

    # DB에서 사용자 확인
    user = test_db.query(User).filter_by(email="testuser@example.com").first()
    assert user is not None
    return user


def test_login(client, saved_user):
    # 로그인 요청
    response = client.post("/login", json={"email": saved_user.email, "password": "1234"})
    
    # 응답 확인
    assert response.status_code == 200
    assert response.json()["success"]

# test_like.py
def test_like(client, test_db):
    user = create_user(test_db, email="test@example.com", password="1234")
    artwork = create_artwork(test_db, product_id=1, image_url="http://example.com/image.jpg", artist_name="Artist", year=2025)

    # Like 요청
    response = client.post("/like", json={"user_id": user.id, "product_id": artwork.product_id})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Like added"}

# test_search.py
def test_search(client, test_db):
    artwork = create_artwork(test_db, product_id=1, image_url="http://example.com/image.jpg", artist_name="Artist", year=2025)
    tag = create_art_tag(test_db, artwork_id=artwork.id, tag="modern")  # 작품에 'modern' 태그 추가

    # Search 요청
    response = client.get("/search", params={"tag": "modern"})
    
    assert response.status_code == 200
    assert len(response.json()) > 0  # 태그 'modern'을 가진 작품이 하나 이상 반환되어야 함

# test_get.py
def test_get_all_artworks(client, test_db):
    create_artwork(test_db, product_id=1, image_url="http://example.com/image1.jpg", artist_name="Artist1", year=2025)
    create_artwork(test_db, product_id=2, image_url="http://example.com/image2.jpg", artist_name="Artist2", year=2025)

    # Get all artworks 요청
    response = client.get("/get")
    
    assert response.status_code == 200
    assert len(response.json()) == 2  # 두 작품이 반환되어야 함

# test_stop.py
def test_stop(client, test_db):
    user = create_user(test_db, email="test@example.com", password="1234")
    artwork = create_artwork(test_db, product_id=1, image_url="http://example.com/image.jpg", artist_name="Artist", year=2025)

    # UserActivity 생성 시 listening_rates를 dict로 전달
    create_user_activity(test_db, user_id=user.id, listened_artworks=[artwork.id], listening_rates={artwork.id: 50})
    
    # Stop 요청
    response = client.post("/stop", json={"user_id": user.id, "artwork_id": artwork.id, "progress": 60})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Progress saved"}