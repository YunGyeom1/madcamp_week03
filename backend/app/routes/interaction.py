from sqlalchemy.orm import Session
from app.db.models import Like, UserActivity
import json

def add_like(session: Session, user_id: int, product_id: int):
    like = Like(user_id=user_id, product_id=product_id)
    session.add(like)
    session.commit()
    return like


def stop_listening(session: Session, user_id: int, artwork_id: int, progress: float):
    user_activity = session.query(UserActivity).filter(UserActivity.user_id == user_id).first()

    if not user_activity:
        # 새 UserActivity 생성
        user_activity = UserActivity(
            user_id=user_id,
            listened_artworks=json.dumps([artwork_id]),  # 'list'로 저장
            listening_rates=json.dumps({artwork_id: progress})  # 'dict'로 저장
        )
        session.add(user_activity)
    else:
        # 기존 UserActivity 업데이트
        listened_artworks = json.loads(user_activity.listened_artworks or "[]")  # 'list'로 로드
        listening_rates = json.loads(user_activity.listening_rates or "{}")  # 'dict'로 로드

        if artwork_id not in listened_artworks:
            listened_artworks.append(artwork_id)

        # listening_rates는 'dict'이므로 'str'로 인덱싱
        listening_rates[str(artwork_id)] = progress

        # 업데이트된 값을 다시 저장
        user_activity.listened_artworks = json.dumps(listened_artworks)
        user_activity.listened_artworks = json.dumps(listened_artworks)

    session.commit()