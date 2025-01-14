import json
import os
import shutil

def get_top_artworks(artists, base_path="../Database/western_artworks", output_file="/app/db/top_artworks.txt"):
    artworks = {}
    
    for artist in artists:
        metadata_path = os.path.join(base_path, artist, "metadata.json")
        try:
            with open(metadata_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                artworks[artist] = [item["title"] for item in data[:10]]  # 상위 10개 작품 제목 추출
        except FileNotFoundError:
            print(f"Metadata not found for artist: {artist}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON for artist: {artist}")
    
    # 결과를 텍스트 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as output:
        for artist, titles in artworks.items():
            output.write(f"{artist}:\n")
            output.write("\n".join(titles) + "\n\n")
    
    print(f"Results saved to {output_file}")


# 사용 예시
artists_list = [
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
get_top_artworks(artists_list)
