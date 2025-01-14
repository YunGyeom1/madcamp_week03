import React, { useRef, useState, useEffect } from "react";
import Masonry from "react-masonry-css";
import { useLocation } from "react-router-dom";
import "./Home.css";

const Home = () => {
  const [artworks, setArtworks] = useState([]);
  const [loadingVideos, setLoadingVideos] = useState({});
  const [query, setSearchQuery] = useState("");
  const videoRefs = useRef({});
  const audioRefs = useRef({});
  const location = useLocation();

  const fetchArtworks = async (query) => {
    try {
      const endpoint = query
        ? `http://localhost:8000/search?tag=${query}` // 검색어가 있을 때
        : "http://localhost:8000/get"; // 검색어가 없을 때 기본 경로
      const response = await fetch(endpoint);
      console.log("Response received:", response);
      if (!response.ok) {
        throw new Error("Failed to fetch artworks");
      }
      const data = await response.json();
      setArtworks(data);
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleMouseEnter = (id) => {
    const video = videoRefs.current[id];
    if (video) {
      video.play();
    }
    const audio = audioRefs.current[id];
    if (audio) {
      audio.play();
    }
  };
  
  const handleMouseLeave = (id) => {
    const video = videoRefs.current[id];
    if (video) {
      video.pause();
    }    
    const audio = audioRefs.current[id];
    if (audio) {
      audio.pause();
    }
  };

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const tag = queryParams.get("tag") || "";
    setSearchQuery(tag);
    fetchArtworks(tag); // 쿼리 파라미터 기반 데이터 로드
  }, [location.search]);

  return (
    <div className="Home">
      <Masonry
        breakpointCols={3}
        className="my-masonry-grid"
        columnClassName="my-masonry-grid_column"
      >
        {artworks.map((artwork) => (
          <div
            className="grid-item"
            key={artwork.id}
            onMouseEnter={() => handleMouseEnter(artwork.id)}
            onMouseLeave={() => handleMouseLeave(artwork.id)}
          >
            <div className="media-container">
              {loadingVideos[artwork.id] && (
                <div className="loading-spinner">Loading...</div>
              )}
              <video
                ref={(el) => (videoRefs.current[artwork.id] = el)}
                src={artwork.description_mp4_url}
                className="artwork-video"
                loop
                muted
                onLoadStart={() => handleVideoLoadStart(artwork.id)}
                onLoadedData={() => handleVideoLoaded(artwork.id)}
              />
              <audio
                ref={(el) => (audioRefs.current[artwork.id] = el)}
                src={artwork.description_mp3_url}
                loop
                
              />
              <img
                src={artwork.image_url}
                alt={artwork.artist_name || "Artwork"}
                className="artwork-image"
              />
            </div>
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