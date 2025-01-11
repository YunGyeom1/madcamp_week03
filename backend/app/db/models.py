from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.session import Base

class ArtTag(Base):
    __tablename__ = 'arttag'

    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, ForeignKey('artwork.id'), nullable=False)
    tag = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    priority = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    artwork = relationship("Artwork", back_populates="tags")

class Artwork(Base):
    __tablename__ = 'artwork'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, unique=True, nullable=False)
    image_url = Column(String, nullable=False)
    description_txt = Column(String, nullable=True)
    description_mp4_url = Column(String, nullable=True)
    description_mp3_url = Column(String, nullable=True)
    artist_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    tags = relationship("ArtTag", back_populates="artwork")

class Like(Base):
    __tablename__ = 'like'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('artwork.product_id'), primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class UserActivity(Base):
    __tablename__ = 'user_activity'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    listened_artworks = Column(JSON, nullable=True)  # 설명 들은 작품 목록
    listening_rates = Column(JSON, nullable=True)    # 각 작품 청취율
    liked_artworks = Column(JSON, nullable=True)     # 좋아요 누른 작품 목록
    viewed_artworks = Column(JSON, nullable=True)

class ArtworkVector(Base):
    __tablename__ = 'artwork_vector'

    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, ForeignKey('artwork.id'), nullable=False, unique=True)
    vector = Column(JSON, nullable=False)  # 벡터를 JSON으로 저장