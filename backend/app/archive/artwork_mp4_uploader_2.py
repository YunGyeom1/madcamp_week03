import os
import json
import requests
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.db.models import Artwork
from app.db.session import Base
import time

human_list = set(
)
finished_list = [5, 7, 33, 37, 41, 51, 52, 54, 56, 57, 58, 59, 60, 70, 71, 72, 73, 74, 75, 83, 88, 89, 121, 122, 123, 124, 125, 126, 127,
    128, 134, 135, 136, 137, 138, 139, 140]

load_dotenv(dotenv_path="/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/backend/.env")

# 환경 변수 확인
D_ID_API_KEY = os.getenv("D_ID_API_KEY")
if not D_ID_API_KEY:
    raise RuntimeError("D_ID_API_KEY is not set in the .env file")
#print(f"D_ID_API_KEY: {D_ID_API_KEY}")

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL) 
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

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

def generate_video(audio_url: str, image_url: str, output_path: str):
    #image_url = "https://storage.googleapis.com/talkingart-bucket/temp_images/03_Self-Portrait.jpg"
    """D-ID API로 영상을 생성하고 로컬 MP4 파일로 저장"""
    d_id_api_url = "https://api.d-id.com/talks"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {D_ID_API_KEY}"
    }
    payload = {
        "script": {
            "type": "audio",
            "audio_url": audio_url
        },
        "source_url": image_url,
        "config": {
            "stitch": True
        }
    }
    # print(audio_url)
    # print(image_url)

    # 요청 보내기
    response = requests.post(d_id_api_url, headers=headers, data=json.dumps(payload))

    if response.status_code != 201:
        print(f"[DEBUG] D-ID API 응답 상태 코드: {response.status_code}")
        print(f"[DEBUG] D-ID API 응답 내용: {response.text}")
        raise RuntimeError(f"D-ID API 오류: {response.status_code} - {response.text}")
    response_data = response.json()
    talk_id = response_data.get("id")
    print(f"[INFO] 작업 생성 성공, 작업 ID: {talk_id}")

    status_url = f"https://api.d-id.com/talks/{talk_id}"
    cnt = 0
    while True:
        status_response = requests.get(status_url, headers=headers)
        status_data = status_response.json()
        cnt += 1
        if(cnt%6==0):
            print(status_data)
        # 상태 확인
        if status_data.get("status") == "done":
            video_url = status_data.get("result_url")
            if not video_url:
                raise RuntimeError("D-ID API 응답에 영상 URL이 없습니다.")
            print(f"[INFO] 비디오 생성 완료, URL: {video_url}")
            break

        # 상태가 completed가 아니면 잠시 기다리고 재시도
        print(f"[INFO] 비디오 생성 중... 상태: {status_data.get('status')}")
        time.sleep(5)
    # 반환된 JSON에서 영상 URL 추출
    video_response = requests.get(video_url, stream=True)
    if video_response.status_code != 200:
        raise RuntimeError(f"영상 다운로드 실패: {video_response.status_code}")

    with open(output_path, "wb") as f:
        for chunk in video_response.iter_content(chunk_size=1024):
            f.write(chunk)

    print(f"[INFO] 비디오 파일 저장 완료: {output_path}")

# gcs_paths.json 파일 읽기
with open("gcs_paths.json", "r") as f:
    gcs_paths = json.load(f)

# DB에서 Artwork 읽기
artworks = session.query(Artwork).filter(Artwork.id.in_(gcs_paths.keys())).all()

# 영상 생성
for num, artwork in enumerate(artworks):
    try:
        if num+1 not in human_list: continue
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
        video_dir = "videos"
        os.makedirs(video_dir, exist_ok=True)
        local_mp4_path = os.path.join(video_dir, f"{sanitized_title}_{num+1}.mp4")
        print(f"[OK] Artwork {artwork.id} 처리 시작 -> {local_mp4_path}")
        generate_video(uploaded_audio_url, uploaded_image_url, local_mp4_path)
        artwork.description_mp4_url = local_mp4_path
        session.add(artwork)
        session.commit()

        print(f"[OK] Artwork {artwork.id} 처리 완료 -> {local_mp4_path}")
    except Exception as e:
        print(f"[ERROR] Artwork {artwork.id} 처리 중 오류")
        print(traceback.format_exc())

print("모든 Artwork 처리를 마쳤습니다.")