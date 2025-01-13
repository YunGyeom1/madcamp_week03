import React, { useEffect, useState } from "react";
import Masonry from "react-masonry-css";
import "./Home.css";

const Home = () => {
  const [artworks, setArtworks] = useState([]);

  // API 호출 함수
  const fetchArtworks = async () => {
    try {
      const response = await fetch("http://localhost:8000/get"); // API 경로
      console.log("Response received:", response);
      if (!response.ok) {
        throw new Error("Failed to fetch artworks");
      }
      const data = await response.json();
      setArtworks(data); // artworks 상태 업데이트
    } catch (error) {
      console.error(error);
    }
  };

  const breakpointColumns = {
    default: 3, // 기본 열 수
    1100: 2, // 너비 1100px 이하일 때 3열
    768: 1, // 너비 768px 이하일 때 2열
    500: 1, // 너비 500px 이하일 때 1열
  };

  // 첫번째 useEffect 데이터 가져오기
  useEffect(() => {
    fetchArtworks();
  }, []);

  return (
    <div className="Home">
      <Masonry
        breakpointCols={breakpointColumns}
        className="my-masonry-grid"
        columnClassName="my-masonry-grid_column"
      >
        {artworks.map((artwork) => (
          <div className="grid-item" key={artwork.id}>
            <img
              src={artwork.image_url}
              alt={artwork.artist_name || "Artwork"}
              className="artwork-image"
            />
            <div className="artwork-details">
              <h3 className="artwork-title">{artwork.title}</h3>
              <div className="artwork-subdetails">
                <p className="artwork-artist">{artwork.artist_name}</p>
                <p className="artwork-year">{artwork.year}</p>
              </div>
            </div>
          </div>
        ))}
      </Masonry>
    </div>
  );
};

export default Home;
