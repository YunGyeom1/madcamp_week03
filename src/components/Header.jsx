import React, { useState, useEffect } from "react";
import { useTheme } from "./ThemeContext";
import logo from "../assets/Logo.svg";
import search from "../assets/search.svg";
import searchbar from "../assets/search_bar.svg";
import dayIcon from "../assets/sun.svg"; // 낮 아이콘
import nightIcon from "../assets/moon.svg";
import "./Header.css";

const Header = () => {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const toggleSearch = () => setIsSearchOpen(!isSearchOpen);

  //낮밤
  const { isNight, toggleTheme } = useTheme();

  return (
    <header className="header">
      <div className="title-container">
        {/* 검색 섹션 */}
        <div className="search-bar">
          <img
            src={search}
            alt="Search"
            className="search-icon"
            onClick={toggleSearch}
          />
        </div>
        <div className="title">
          {<img src={logo} alt="Logo" className="logo" />}
          <div className="title-line"></div>
        </div>
        {/* 네비게이션 */}
        <nav className="nav">
          <img
            src={isNight ? nightIcon : dayIcon}
            alt="Theme Toggle"
            className="theme-toggle-icon"
            onClick={toggleTheme}
          />
        </nav>
      </div>

      {isSearchOpen && (
        <div className="search-container">
          <img src={searchbar} alt="Search Icon" class="search-icon-bar" />
          <input type="text" placeholder="Search..." className="search-input" />
        </div>
      )}
    </header>
  );
};

export default Header;
