import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.cloud import storage
from dotenv import load_dotenv
from app.db.models import Artwork
from app.db.session import Base
from urllib.parse import unquote
import re

load_dotenv(dotenv_path="/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/backend/.env")

# 환경 변수 확인
BUCKET_NAME = os.getenv("BUCKET_NAME")
if not BUCKET_NAME:
    raise RuntimeError("BUCKET_NAME is not set in the .env file")

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL) 
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

storage_client = storage.Client()

def sanitize_filename(filename: str) -> str:
    """
    URL 인코딩된 문자 및 특수문자를 안전한 파일명으로 변환
    """
    # URL 인코딩 해제
    decoded = unquote(filename)
    
    # 특수문자 대체 규칙
    replace_map = {
        " ": "_",       # 공백
        "'": "",        # 작은따옴표
        ",": "",        # 쉼표
        "é": "e",       # e with acute
        "á": "a",       # a with acute
        "(": "",        # 여는 괄호
        ")": "",        # 닫는 괄호
        "\"": "",       # 큰따옴표
        "–": "-",       # 대시 (유니코드)
        "‘": "",        # 왼쪽 작은따옴표
        "’": "",        # 오른쪽 작은따옴표
    }
    
    # 특수문자 대체
    for char, replacement in replace_map.items():
        decoded = decoded.replace(char, replacement)

    # 추가적인 URL 인코딩 제거
    decoded = unquote(decoded)
    
    # 안전한 파일명: 알파벳, 숫자, 밑줄, 하이픈만 허용
    sanitized = re.sub(r"[^a-zA-Z0-9_\-.]", "", decoded)
    
    return sanitized
def upload_to_gcs(local_path: str, gcs_path: str) -> str:
    try:
        print(f"[INFO] GCS 업로드 시작: {local_path} -> {gcs_path}")
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(gcs_path)
        blob.upload_from_filename(local_path)
        print(f"[INFO] GCS 업로드 성공: {gcs_path}")
        return blob.public_url
    except Exception as e:
        print(f"[ERROR] GCS 업로드 실패: {local_path} -> {gcs_path}")
        print(f"오류 메시지: {str(e)}")
        raise

print("DB에서 Artwork를 읽어옵니다...")
artworks = session.query(Artwork).filter(Artwork.description_txt.isnot(None)).all()
print(f"{len(artworks)}개 Artwork를 처리합니다.")

gcs_paths = {}
for artwork in artworks:
    try:
        if not artwork.image_url or not artwork.description_mp3_url:
            print(f"[SKIP] Artwork {artwork.id} -> 이미지/MP3 경로가 없음.")
            continue

        # 파일명 공백 제거 및 GCS 경로 설정
        image_basename = sanitize_filename(os.path.basename(artwork.image_url))
        mp3_basename = sanitize_filename(os.path.basename(artwork.description_mp3_url))
        gcs_image_path = f"temp_images/{image_basename}"
        gcs_mp3_path = f"temp_audio/{mp3_basename}"

        uploaded_image_url = upload_to_gcs(artwork.image_url, gcs_image_path)
        uploaded_audio_url = upload_to_gcs(artwork.description_mp3_url, gcs_mp3_path)

        gcs_paths[artwork.id] = {
            "image_url": uploaded_image_url,
            "audio_url": uploaded_audio_url
        }
    except Exception as e:
        print(f"[ERROR] Artwork {artwork.id} 업로드 중 오류")
        continue

# 업로드 정보 저장
with open("gcs_paths.json", "w") as f:
    json.dump(gcs_paths, f, indent=4)

print("모든 Artwork 업로드 정보를 gcs_paths.json에 저장했습니다.")