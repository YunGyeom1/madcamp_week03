import os
import requests
import json

# 화가 리스트 (20명으로 확장)
artists = [
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

# 기본 폴더 설정
base_path = os.path.join("..", "Database")
base_dir = os.path.join(base_path, "western_artworks")
os.makedirs(base_dir, exist_ok=True)

# 작품 다운로드 및 메타데이터 저장 함수
def download_artworks(artist_url):
    artist_dir = os.path.join(base_dir, artist_url)
    os.makedirs(artist_dir, exist_ok=True)

    api_url = "https://www.wikiart.org/en/App/Painting/PaintingsByArtist"
    params = {"artistUrl": artist_url, "json": True}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        artworks = response.json()  # 응답이 리스트 형태일 경우 그대로 사용
        if isinstance(artworks, list):  # 리스트 여부 확인
            metadata_list = []
            for i, artwork in enumerate(artworks[:10]):  # 최대 10개 제한
                image_url = artwork.get("image", "")
                title = artwork.get("title", "Untitled").replace("/", "-")
                year = artwork.get("completitionYear", "Unknown")
                style = artwork.get("genre", "Unknown")
                image_path = os.path.join(artist_dir, f"{i+1:02d}_{title}.jpg")
                
                # 이미지 다운로드
                if image_url:
                    try:
                        img_data = requests.get(image_url).content
                        with open(image_path, "wb") as f:
                            f.write(img_data)
                        print(f"{artist_url} - Downloaded: {title}")
                    except Exception as e:
                        print(f"Failed to download image for {title}: {e}")
                        continue
                else:
                    print(f"No image URL for {title}")
                    continue
                
                # 메타데이터 추가
                metadata_list.append({
                    "title": title,
                    "year": year,
                    "style": style,
                    "image_path": image_path,
                    "image_url": image_url
                })
            
            # 메타데이터 저장
            metadata_file = os.path.join(artist_dir, "metadata.json")
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata_list, f, ensure_ascii=False, indent=4)
            print(f"{artist_url} - Metadata saved to {metadata_file}")
        else:
            print(f"Unexpected response format for {artist_url}: {type(artworks)}")
    else:
        print(f"Failed to fetch artworks for {artist_url}: {response.status_code}")

# 사용 예시
artist_urls = ["paul-gauguin",
    "jackson-pollock",
    "henri-rousseau"]  # 테스트용

for artist_url in artists:
    download_artworks(artist_url)