# tests/utils.py
from app.db.models import User, Artwork, ArtTag, UserActivity
from app.db.session import SessionLocal
import json

# 유저 생성 함수
def create_user(db, email, password):
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 작품 생성 함수
def create_artwork(db, product_id, image_url, artist_name, year):
    artwork = Artwork(product_id=product_id, image_url=image_url, artist_name=artist_name, year=year)
    db.add(artwork)
    db.commit()
    db.refresh(artwork)
    return artwork

# 태그 생성 함수
def create_art_tag(db, artwork_id, tag):
    art_tag = ArtTag(artwork_id=artwork_id, tag=tag)
    db.add(art_tag)
    db.commit()
    db.refresh(art_tag)
    return art_tag


def create_user_activity(db, user_id, listened_artworks, listening_rates):
    # listening_rates는 dict 형태로 전달되어야 함
    activity = UserActivity(
        user_id=user_id, 
        listened_artworks=json.dumps(listened_artworks), 
        listening_rates=json.dumps(listening_rates)  # dict로 저장
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity
