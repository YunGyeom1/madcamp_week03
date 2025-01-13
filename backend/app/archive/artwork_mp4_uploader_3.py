import os
import time
import requests
from dotenv import load_dotenv
import json
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Artwork
from app.db.session import Base

image_set = [5, 7, 33, 37, 41, 51, 52, 54, 56, 57, 58, 59, 60, 70, 71, 72, 73, 74, 75, 83, 88, 89, 121, 122, 123, 124, 125, 126, 127,
    128, 134, 135, 136, 137, 138, 139, 140]

image_set += [1]
# .env 파일에서 API 키 불러오기
load_dotenv(dotenv_path="/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/backend/.env")
HAILUO_AI_API_KEY = os.getenv("HAILUO_AI_API_KEY")
if not HAILUO_AI_API_KEY:
    raise RuntimeError("HAILUO_AI_API_KEY is not set in the .env file")

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL) 
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


PROMPT = "Description of your video"  # 필요시 수정
MODEL = "video-01"  # Hailuo AI 모델 ID
OUTPUT_DIR = "videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def check_url_valid(url: str) -> bool:
    try:
        #print(f"[INFO] URL 유효성 검사: {url}")
        head_resp = requests.head(url, timeout=5)
        if (head_resp.status_code != 200):
            print(f"[INFO] URL 응답 코드: {head_resp.status_code}")
        return head_resp.status_code == 200
    except Exception as e:
        print(f"[ERROR] URL 유효성 검사 실패: {url}")
        return False


def generate_video(uploaded_image_url: str, output_path: str):
    """Hailuo AI로 영상 생성 및 저장"""
    prompt = "object is moving"
    model = "video-01-live2d"
    
    # 1. 작업 생성
    print("[INFO] 영상 생성 작업 제출 중...")
    url_submit = "https://api.minimaxi.chat/v1/video_generation"
    payload = {"prompt": prompt, "model": model, "first_frame_image": uploaded_image_url}
    headers = {
        'authorization': f'Bearer {HAILUO_AI_API_KEY}',
        'content-type': 'application/json',
    }
    response = requests.post(url_submit, headers=headers, json=payload)
    response_data = response.json()
    print(response_data)
    if response.status_code != 200 or 'task_id' not in response_data:
        raise RuntimeError(f"[ERROR] 작업 생성 실패: {response.text}")

    task_id = response_data['task_id']
    print(f"[INFO] 작업 생성 성공, Task ID: {task_id}")

    # 2. 작업 상태 확인 및 대기
    url_query = f"https://api.minimaxi.chat/v1/query/video_generation?task_id={task_id}"
    while True:
        response = requests.get(url_query, headers=headers)
        response_data = response.json()
        status = response_data.get('status')
        print(status)
        if status == 'Success':
            file_id = response_data['file_id']
            print("[INFO] 작업 완료")
            break
        elif status in ['Queueing', 'Processing', 'Preparing']:
            print(f"[INFO] 진행 중... 상태: {status}")
        else:
            raise RuntimeError(f"[ERROR] 작업 실패 또는 알 수 없는 상태: {status}")
        time.sleep(5)

    # 3. 결과 다운로드
    print("[INFO] 결과 다운로드 중...")
    url_retrieve = f"https://api.minimaxi.chat/v1/files/retrieve?file_id={file_id}"
    response = requests.get(url_retrieve, headers=headers)
    response_data = response.json()
    download_url = response_data['file']['download_url']

    video_content = requests.get(download_url).content
    with open(output_path, 'wb') as f:
        f.write(video_content)

    print(f"[INFO] 영상 저장 완료: {output_path}")

# gcs_paths.json 파일 읽기
with open("gcs_paths.json", "r") as f:
    gcs_paths = json.load(f)
# DB에서 Artwork 읽기
artworks = session.query(Artwork).filter(Artwork.id.in_(gcs_paths.keys())).all()

# 영상 생성
for num, artwork in enumerate(artworks):
    try:
        if num+1 in image_set: 
            continue
        
        uploaded_image_url = gcs_paths[str(artwork.id)]["image_url"]
        uploaded_audio_url = gcs_paths[str(artwork.id)]["audio_url"]
        print(uploaded_image_url)
        # URL 유효성 검사
        if not check_url_valid(uploaded_image_url):
            print(f"[WARNING] 이미지 URL 유효하지 않음: {uploaded_image_url}")
        if not check_url_valid(uploaded_audio_url):
            print(f"[WARNING] 오디오 URL 유효하지 않음: {uploaded_audio_url}")

        # 영상 생성
        sanitized_title = artwork.title.replace(" ", "_").replace("/", "_")
        video_dir = "videos2"
        os.makedirs(video_dir, exist_ok=True)
        local_mp4_path = os.path.join(video_dir, f"{sanitized_title}_{num+1}.mp4")
        print(f"[OK] Artwork {artwork.id} 처리 시작 -> {local_mp4_path}")
        generate_video(uploaded_image_url, local_mp4_path)
        artwork.description_mp4_url = local_mp4_path
        session.add(artwork)
        session.commit()

        print(f"[OK] Artwork {artwork.id} 처리 완료 -> {local_mp4_path}")
    except Exception as e:
        print(f"[ERROR] Artwork {artwork.id} 처리 중 오류")
        print(traceback.format_exc())

print("모든 Artwork 처리를 마쳤습니다.")