from sqlalchemy.orm import Session
from app.db.models import Artwork, ArtTag

def search_by_tag(session: Session, tag: str):
    results = (
        session.query(Artwork)
        .join(ArtTag, Artwork.id == ArtTag.artwork_id)
        .filter(ArtTag.tag == tag)
        .all()
    )
    return results