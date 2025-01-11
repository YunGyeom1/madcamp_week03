import os
import requests
import json

# 피카소 작품 다운로드 폴더 설정 (week3/Database/picasso_artworks)
base_path = os.path.join("..", "Database")
output_dir = os.path.join(base_path, "picasso_artworks")
os.makedirs(output_dir, exist_ok=True)

# WikiArt API 설정
api_url = "https://www.wikiart.org/en/App/Painting/PaintingsByArtist"
artist_url = "pablo-picasso"

# API 요청
params = {"artistUrl": artist_url, "json": True}
response = requests.get(api_url, params=params)

if response.status_code == 200:
    artworks = response.json()  # 응답 데이터가 리스트일 경우 바로 사용
    
    if isinstance(artworks, list):  # 리스트일 경우 처리
        metadata_list = []
        for i, artwork in enumerate(artworks[:5]):  # 최대 50개 제한
            print(json.dumps(artwork, indent=4, ensure_ascii=False))
            image_url = artwork.get("image")
            title = artwork.get("title", "Untitled").replace("/", "-")
            year = artwork.get("year", "Unknown")
            style = artwork.get("style", "Unknown")
            
            # 이미지 경로
            image_path = os.path.join(output_dir, f"{i+1:02d}_{title}.jpg")
            
            # 이미지 다운로드
            img_data = requests.get(image_url).content
            with open(image_path, "wb") as f:
                f.write(img_data)
            print(f"Downloaded: {title}")
            
            # 메타데이터 저장
            metadata_list.append({
                "title": title,
                "year": year,
                "style": style,
                "image_path": image_path,
                "image_url": image_url
            })
        
        # 메타데이터를 JSON 파일로 저장
        metadata_file = os.path.join(output_dir, "metadata.json")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata_list, f, ensure_ascii=False, indent=4)
        print(f"Metadata saved to {metadata_file}")
    else:
        print("Unexpected data format:", type(artworks))
else:
    print(f"Failed to fetch artworks: {response.status_code}, URL: {response.url}")