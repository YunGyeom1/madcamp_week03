import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Artwork
from app.db.session import Base
from google.cloud import texttospeech
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(dotenv_path="/Users/yungyeom/Downloads/madcamp_week3/main_project/madcamp_week03/backend/.env")

# DB 연결 설정
DATABASE_URL = "sqlite:///./test.db"  # 예시 SQLite DB
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Google TTS 클라이언트 설정 (JSON 키 사용)
service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # .env에 JSON 경로 설정
client = texttospeech.TextToSpeechClient.from_service_account_json(service_account_path)

# MP3 파일 저장 경로 설정
MP3_SAVE_DIR = "../Database/mp3s"
os.makedirs(MP3_SAVE_DIR, exist_ok=True)

def synthesize_speech(text, output_path):
    """TTS 변환 후 MP3 저장"""
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-D",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # MP3 파일 저장
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
        print(f"MP3 saved: {output_path}")
    except Exception as e:
        print(f"Error generating MP3 for text: {text[:30]}... - {e}")

# DB에서 Artwork 데이터 읽기 및 MP3 변환 및 저장
artworks = session.query(Artwork).filter(Artwork.description_txt.isnot(None)).all()

for artwork in artworks:
    try:
        # MP3 파일명 생성: title + product_id
        sanitized_title = artwork.title.replace(" ", "_").replace("/", "_")
        mp3_filename = f"{sanitized_title}_{artwork.product_id}.mp3"
        mp3_path = os.path.join(MP3_SAVE_DIR, mp3_filename)
        description = (artwork.title + " is a work created by " + artwork.artist_name + 
                   " in " + str(artwork.year) + artwork.description_txt)
        # TTS 변환 및 저장
        synthesize_speech(description, mp3_path)

        # DB에 MP3 URL 상대 경로로 업데이트
        artwork.description_mp3_url = f"{MP3_SAVE_DIR}/{mp3_filename}"
        session.add(artwork)
    except Exception as e:
        print(f"Error processing artwork ID {artwork.id}: {e}")

# 변경 사항 커밋
session.commit()
print("DB updated with MP3 URLs.")