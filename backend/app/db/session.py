# app/db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.test", override=True)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
print(f"Using DATABASE_URL: {DATABASE_URL}")  # DATABASE_URL 값 확인

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from app.db.models import User, Artwork, ArtTag, Like, UserActivity
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")