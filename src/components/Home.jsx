import React, { useRef, useState } from "react";
import Masonry from "react-masonry-css";
import "./Home.css";

const Home = () => {
  const [artworks, setArtworks] = useState([]);
  const [loadingVideos, setLoadingVideos] = useState({}); // 로딩 상태 관리
  const videoRefs = useRef({});

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

  const handleMouseEnter = (id) => {
    const video = videoRefs.current[id];
    if (video) {
      video.currentTime = video.currentTime || 0; // 멈췄던 위치에서 시작
      video.play(); // 동영상 재생
    }
  };

  const handleMouseLeave = (id) => {
    const video = videoRefs.current[id];
    if (video) {
      video.pause(); // 동영상 멈춤
    }
  };

  const handleVideoLoadStart = (id) => {
    setLoadingVideos((prev) => ({ ...prev, [id]: true })); // 로딩 시작
  };

  const handleVideoLoaded = (id) => {
    setLoadingVideos((prev) => ({ ...prev, [id]: false })); // 로딩 완료
  };

  const breakpointColumns = {
    default: 3, // 기본 열 수
    1100: 2, // 너비 1100px 이하일 때 3열
    768: 1, // 너비 768px 이하일 때 2열
    500: 1, // 너비 500px 이하일 때 1열
  };

  // 첫번째 useEffect 데이터 가져오기
  React.useEffect(() => {
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
          <div
            className="grid-item"
            key={artwork.id}
            onMouseEnter={() => handleMouseEnter(artwork.id)}
            onMouseLeave={() => handleMouseLeave(artwork.id)}
          >
            <div className="media-container">
              {/* 로딩 스피너 */}
              {loadingVideos[artwork.id] && (
                <div className="loading-spinner">Loading...</div>
              )}
              <video
                ref={(el) => (videoRefs.current[artwork.id] = el)} // videoRefs에 저장
                src={artwork.description_mp4_url}
                className="artwork-video"
                muted
                loop
                onLoadStart={() => handleVideoLoadStart(artwork.id)}
                onLoadedData={() => handleVideoLoaded(artwork.id)}
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
