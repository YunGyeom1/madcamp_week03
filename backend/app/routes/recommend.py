from sqlalchemy.orm import Session
from app.db.models import Artwork

def get_artworks(session: Session):
    artworks = session.query(Artwork).all()
    return artworks