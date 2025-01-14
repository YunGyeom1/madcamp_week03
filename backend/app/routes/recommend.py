from sqlalchemy.orm import Session
from app.db.models import Artwork, ArtworkVector, Like
#from sentence_transformers import SentenceTransformer, util
from sqlalchemy.sql.expression import func
from typing import List, Tuple
import random

from sqlalchemy.sql.expression import func

# 벡터 저장
# def save_vectors(session: Session, artwork_vectors: List[Tuple[int, List[float]]]):
#     for artwork_id, vector in artwork_vectors:
#         vector_entry = ArtworkVector(artwork_id=artwork_id, vector=vector)
#         session.add(vector_entry)
#     session.commit()

# # 벡터 조회
# def get_vectors(session: Session, artwork_ids: List[int]) -> List[List[float]]:
    # return [
    #     vector_entry.vector
    #     for vector_entry in session.query(ArtworkVector).filter(ArtworkVector.artwork_id.in_(artwork_ids)).all()
    # ]

def get_artworks(session: Session):
    artworks = session.query(Artwork).order_by(func.random()).all()
    return artworks

# def get_similar_artworks(
#     session: Session,
#     input_artwork_ids: List[int],
#     top_n: int = 50 ) -> List[Tuple[Artwork, float]]:
#     """
#     최근 좋아요 기반으로 유사한 작품과 유사도 점수를 반환.

#     Args:
#         session (Session): DB 세션
#         input_artwork_ids (List[int]): 기준이 될 artwork IDs
#         top_n (int): 상위 N개 추천

#     Returns:
#         List[Tuple[Artwork, float]]: 추천 작품과 유사도 점수 리스트
#     """
#     # SentenceTransformer 모델 로드
#     model = SentenceTransformer('all-MiniLM-L6-v2')

#     # 모든 artwork 데이터 가져오기
#     all_artworks = session.query(Artwork).filter(Artwork.description_txt.isnot(None)).all()

#     # 기준 artwork 선택
#     target_artworks = [artwork for artwork in all_artworks if artwork.id in input_artwork_ids]

#     if not target_artworks:
#         # 기준 artwork가 없으면 랜덤 top_n개 반환
#         random.shuffle(all_artworks)
#         return [(artwork, 0.0) for artwork in all_artworks[:top_n]]

#     # description_txt, artist_name, year 결합
#     def combine_fields(artwork):
#         artist_name = (artwork.artist_name + " ") * 5
#         year = (str(artwork.year) + " ") * 3
#         return f"{artist_name.strip()} {year.strip()} {artwork.description_txt or ''}"

#     # 기준 artwork와 모든 artwork의 벡터화
#     target_descriptions = [combine_fields(artwork) for artwork in target_artworks]
#     all_descriptions = [combine_fields(artwork) for artwork in all_artworks]

#     target_vectors = model.encode(target_descriptions, convert_to_tensor=True)
#     content_vectors = model.encode(all_descriptions, convert_to_tensor=True)

#     # 유사도 계산 (각 artwork와 기준 artwork 간의 최대값)
#     similarities = util.pytorch_cos_sim(target_vectors, content_vectors)
#     max_similarities = similarities.max(dim=0).values.cpu().tolist()  # 리스트로 변환

#     # 상위 top_n 추출
#     top_indices = sorted(range(len(max_similarities)), key=lambda i: max_similarities[i], reverse=True)[:top_n]

#     # 결과 반환 (Artwork와 유사도 점수)
#     similar_artworks = [(all_artworks[i], max_similarities[i]) for i in top_indices]
#     return similar_artworks