import React, { useState, useEffect } from "react";
import { useTheme } from "./ThemeContext";
import { useNavigate } from "react-router-dom";
import logo from "../assets/Logo.svg";
import logoDay from "../assets/daylogo.svg";
import search from "../assets/search.svg";
import daysearch from "../assets/daysearch.svg";
import searchbar from "../assets/search_bar.svg";
import dayIcon from "../assets/sun.svg"; // 낮 아이콘
import nightIcon from "../assets/moon.svg";
import "./Header.css";

const Header = () => {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const toggleSearch = () => setIsSearchOpen(!isSearchOpen);
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const [isFlipped, setIsFlipped] = useState(false); // 카드 뒤집힘 상태 관리

  const handleCardClick = () => {
    setIsFlipped((prev) => !prev); // 클릭 시 상태 반전
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/search?tag=${searchQuery.trim()}`;
    }
  };

  const handleLogoClick = () => {
    navigate("/"); // Home 페이지로 이동
  };

  //낮밤
  const { isNight, toggleTheme } = useTheme();

  return (
    <header
      className="header"
      style={{
        background: isNight
          ? "linear-gradient(-45deg, #070707, #5c5b5b)"
          : "linear-gradient(-45deg, #E9CC75, #E5DFDF)",
        transition: "background 0.7s ease",
      }}
    >
      <div className="title-container">
        {/* 검색 섹션 */}
        <div className="search-bar">
          <img
            src={isNight ? search : daysearch}
            alt="Search"
            className="search-icon"
            onClick={toggleSearch}
          />
        </div>
        <div
          className="title"
          onClick={handleLogoClick}
          style={{ cursor: "pointer" }}
        >
          {<img src={isNight ? logo : logoDay} alt="Logo" className="logo" />}
          <div
            className="title-line"
            style={{
              background: isNight ? "#efe1b6" : "#5A5959",
            }}
          ></div>
        </div>
        {/* 네비게이션 */}
        <div
          className={`toggle-card ${isFlipped ? "flipped" : ""}`}
          onClick={() => {
            handleCardClick(); // 카드 뒤집힘 상태 변경
            toggleTheme(); // 낮/밤 전환
          }}
        >
          {/* 카드 앞면 (밤 아이콘) */}
          <div className="toggle-front">
            <img src={nightIcon} alt="Night Mode" className="theme-icon" />
          </div>
          {/* 카드 뒷면 (낮 아이콘) */}
          <div className="toggle-back">
            <img src={dayIcon} alt="Day Mode" className="theme-icon" />
          </div>
        </div>
      </div>

      {isSearchOpen && (
        <div className="search-container">
          <form onSubmit={handleSearchSubmit}>
            <img
              src={searchbar}
              alt="Search Icon"
              className="search-icon-bar"
            />
            <input
              type="text"
              placeholder="Search..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
            <button type="submit" className="search-btn">
              Search
            </button>
          </form>
        </div>
      )}
    </header>
  );
};

export default Header;
