from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.models import Artwork, ArtTag  # 모델 임포트
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv(dotenv_path="/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/backend/.env")

# 데이터베이스 연결 설정
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL) 
Session = sessionmaker(bind=engine)
session = Session()


# ArtTag에 작가 이름, 제목 추가
for artwork in session.query(Artwork).filter(Artwork.id > 150).all():
    # 작가 이름 추가
    artist_tag = ArtTag(
        artwork_id=artwork.id,
        tag=artwork.artist_name,
        created_at=datetime.now(timezone.utc),
        description="Artist Name"
    )
    session.add(artist_tag)

    # 제목 추가
    title_tag = ArtTag(
        artwork_id=artwork.id,
        tag=artwork.title,
        created_at=datetime.now(timezone.utc),
        description="Title"
    )
    session.add(title_tag)

    print(f"Added tags for Artwork ID: {artwork.id}")

# 변경 사항 커밋
session.commit()
session.close()

print("All tags added successfully!")