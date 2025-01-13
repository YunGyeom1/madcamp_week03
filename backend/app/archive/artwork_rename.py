from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from app.db.models import Artwork  # 실제 모델 경로에 맞게 수정

# 환경변수 및 DB 설정
load_dotenv(dotenv_path="/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/backend/.env")
DATABASE_URL = "sqlite:///./test.db"  # 예시 DB URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def update_artist_names():
    # DB에서 모든 Artwork 가져오기
    artworks = session.query(Artwork).all()

    for artwork in artworks:
        if artwork.artist_name:
            # '-' 제거 및 각 단어의 첫 글자를 대문자로 변환
            updated_name = " ".join(word.capitalize() for word in artwork.artist_name.replace("-", " ").split())
            artwork.artist_name = updated_name
            print(f"Updated: {artwork.artist_name}")

    # 변경사항 저장
    session.commit()
    print("모든 artist_name이 업데이트되었습니다.")

# 실행
update_artist_names()