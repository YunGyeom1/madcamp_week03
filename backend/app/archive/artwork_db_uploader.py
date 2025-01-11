import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Artwork, ArtTag  # 작성한 모델 불러오기
from app.db.session import Base
# DB 연결 설정 (사용자가 수정 가능)
DATABASE_URL = "sqlite:///./test.db"  # 예시 SQLite DB
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

def reset_database():
    """기존 데이터를 삭제하고 테이블을 초기화"""
    print("Resetting database...")
    Base.metadata.drop_all(bind=engine)  # 모든 테이블 삭제
    Base.metadata.create_all(bind=engine)  # 테이블 재생성
    print("Database reset complete.")

reset_database()  # 초기화 함수 호출


artists_list = [
    "pablo-picasso",
    "vincent-van-gogh",
    "claude-monet",
    "leonardo-da-vinci",
    "rembrandt",
    "edgar-degas",
    "paul-cezanne",
    "gustav-klimt",
    "edvard-munch",
    "henri-matisse",
    "salvador-dali",
    "andy-warhol",
    "frida-kahlo",
    "michelangelo-buonarroti",
    "georges-seurat"
]

# Artwork 테이블 채우기
artwork_map = {}

# Description.txt와 Tags.txt 로드 및 ArtTag 추가
for wowow, artist in enumerate(artists_list):
    metadata_file_path = f"../Database/western_artworks/{artist}/metadata.json"
    with open(metadata_file_path, "r") as f:
        metadata = json.load(f)
    for artwork in metadata:
        artist_name = artwork["image_path"].split("/")[-2]  # 경로에서 artist 추출
        new_artwork = Artwork(
            product_id=metadata.index(artwork) + 1 + wowow*10 ,
            artist_name=artist_name,
            year=artwork["year"],
            image_url=artwork["image_path"],
            description_txt=None,  # 일단 None, 다음 단계에서 추가
            title = artwork["title"]
        )
        session.add(new_artwork)
        session.commit()
        artwork_map[artwork["title"]] = new_artwork.id
        print("Added artwork:" + f"{metadata.index(artwork) + 1 + wowow*10}" +  f"{new_artwork}")

    tag_file_path = f"../Database/western_artworks/{artist}/Artwork_Tags.txt"
    with open(tag_file_path, "r") as f:
        tags = f.read().split("\n\n")
        #print(tags)
    for tag_entry in tags:
        if not tag_entry.strip() or "\n" not in tag_entry:
            print(f"Skipping invalid tag_entry: {tag_entry}")
            continue
        #print(tag_entry)
        title, tag_list = tag_entry.split("\n", 1)
        tag_list = tag_list.split(", ")
        artwork_id = artwork_map.get(title)
        if artwork_id:
            for tag in tag_list:
                new_tag = ArtTag(
                    artwork_id=artwork_id,
                    tag=tag,
                    priority=None
                )
                session.add(new_tag)
                print(f"Added tag: {new_tag} for artwork ID: {artwork_id}")
    # Description
    desc_file_path = f"../Database/western_artworks/{artist}/Artwork_Descriptions.txt"
    with open(desc_file_path, "r") as f:
        descriptions = f.read().split("\n\n")
    for description in descriptions:
        if not description.strip() or "\n" not in description:
            print(f"Skipping invalid description: {description}")
            continue
        
        title, desc_text = description.split("\n", 1)
        artwork_id = artwork_map.get(title)
        if artwork_id:
            session.query(Artwork).filter(Artwork.id == artwork_id).update({"description_txt": desc_text})
            session.commit()
            print(f"Updated description for artwork ID: {artwork_id}")
# 세션 커밋 후 종료
session.commit()
session.close()