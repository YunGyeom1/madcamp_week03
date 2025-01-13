import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Artwork  # Artwork 모델 임포트
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(dotenv_path="/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/backend/.env")

# 데이터베이스 연결 설정
DATABASE_URL = "sqlite:///./test.db"  # DB URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 원본 및 대상 디렉토리 설정
source_dir = "/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/backend/videos"
target_dir = "/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/Database/western_artworks/faces"

# 파일 이동 및 DB 업데이트
for artwork in session.query(Artwork).all():
    if artwork.description_mp4_url:
        # 원본 파일 경로
        original_path = os.path.join(source_dir, os.path.basename(artwork.description_mp4_url))
        # 대상 파일 경로
        new_path = os.path.join(target_dir, os.path.basename(artwork.description_mp4_url))
        
        if os.path.exists(original_path):  # 파일이 존재할 경우에만 이동
            # 파일 이동
            shutil.move(original_path, new_path)
            # DB 업데이트
            artwork.description_mp4_url = new_path
            print(f"Updated {artwork.id} -> {new_path}")
        else:
            print(f"File not found: {original_path}")

# 변경 사항 커밋
session.commit()
session.close()