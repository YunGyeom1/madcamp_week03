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

# 대상 디렉토리
source_directory = "/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/Database/western_artworks/faces"

# 파일 이름 변경 함수
def update_file_paths_in_db(base_directory, db_field_prefix, target_prefix):
    try:
        # 데이터베이스에서 모든 Artwork 조회
        artworks = session.query(Artwork).all()

        for artwork in artworks:
            original_path = artwork.description_mp4_url

            # 경로가 주어진 `db_field_prefix`로 시작하는지 확인
            if original_path and original_path.startswith(db_field_prefix):
                # 상대 경로로 변환
                relative_path = original_path.replace(db_field_prefix, target_prefix, 1)

                # 데이터베이스 업데이트
                artwork.description_mp4_url = relative_path
                session.commit()

                print(f"Updated: {original_path} -> {relative_path}")
            else:
                print(f"Skipped: {original_path} (does not match prefix)")

        print("Database update completed.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # 세션 종료
        session.close()


# 설정값
base_directory = "/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/Database/western_artworks/faces"
db_field_prefix = base_directory
target_prefix = "../Database/western_artworks/faces"

# 함수 실행
update_file_paths_in_db(base_directory, db_field_prefix, target_prefix)