from sqlalchemy.orm import Session, joinedload
from app.db.models import Artwork, ArtTag
from sqlalchemy.sql.expression import func

def search_by_tag(session: Session, tag: str):
    results = (
        session.query(Artwork)
        .join(ArtTag, Artwork.id == ArtTag.artwork_id)
        .filter(ArtTag.tag == tag)
        .options(joinedload(Artwork.tags))
        .order_by(func.random())
        .all()
    )
    return results