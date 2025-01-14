import os
import subprocess
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

def process_video_with_ffmpeg(artwork):
    mp4_path = artwork.image_url.replace(".jpg", ".mp4")
    if not os.path.exists(mp4_path):
        print(f"파일 없음: {mp4_path}")
        return

    reversed_mp4_path = mp4_path.replace(".mp4", "_reversed.mp4")
    reencoded_mp4_path = mp4_path.replace(".mp4", "_reencoded.mp4")
    output_path = mp4_path.replace(".mp4", "2.mp4")
    file_list_path = "file_list.txt"

    try:
        # 원본 동영상 재인코딩
        subprocess.run([
            "ffmpeg", "-i", mp4_path, "-vf", "reverse", "-af", "areverse", reversed_mp4_path
        ], check=True)

        # 역재생 동영상 생성
        with open(file_list_path, "w") as f:
            f.write(f"file '{mp4_path}'\n")
            f.write(f"file '{reversed_mp4_path}'\n")

        # 동영상 병합
        subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", file_list_path, 
            "-c", "copy", output_path
        ], check=True)

        # DB에 description_mp4_url 업데이트
        artwork.description_mp4_url = output_path
        session.commit()
        print(f"저장 완료: {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 에러: {e}")

    finally:
        # 임시 파일 삭제
        if os.path.exists(file_list_path):
            os.remove(file_list_path)
        if os.path.exists(reversed_mp4_path):
            os.remove(reversed_mp4_path)

# DB에서 Artwork 가져오기
artworks = session.query(Artwork).all()

# 동영상 처리
for artwork in artworks:
    process_video_with_ffmpeg(artwork)