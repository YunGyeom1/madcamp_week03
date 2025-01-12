import React, { useEffect, useState } from "react";
import Packery from "packery";
import "./Home.css";

const Home = () => {
  const [artworks, setArtworks] = useState([]);

  // API 호출 함수
  const fetchArtworks = async () => {
    try {
      const response = await fetch("http://localhost:8000/get"); // API 경로
      if (!response.ok) {
        throw new Error("Failed to fetch artworks");
      }
      const data = await response.json();
      setArtworks(data); // artworks 상태 업데이트
    } catch (error) {
      console.error(error);
    }
  };

  // Packery 초기화 함수
  const initializePackery = () => {
    const gridElement = document.querySelector(".grid");
    new Packery(gridElement, {
      itemSelector: ".grid-item",
      gutter: 20,
    });
  };

  // 첫번째 useEffect 데이터 가져오기
  useEffect(() => {
    fetchArtworks();
  }, []);

  //두번째 useEffect Packery 초기화
  useEffect(() => {
    if (artworks.length > 0) {
      initializePackery();
    }
  }, [artworks]);

  return (
    <div className="Home">
      <div className="grid">
        {artworks.map((artwork) => (
          <div className="grid-item" key={artwork.id}>
            <img
              src={artwork.image_url}
              alt={artwork.artist_name || "Artwork"}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
