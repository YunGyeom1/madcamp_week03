import React, { useState, useEffect } from "react";
import logo from "../assets/Logo.svg";
import search from "../assets/search.svg";
import searchbar from "../assets/search_bar.svg";
import { useNavigate } from "react-router-dom";
import "./Header.css"; 


const Header = () => {
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isSignupOpen, setIsSignupOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const toggleSearch = () => setIsSearchOpen(!isSearchOpen);

  const openLoginModal = () => setIsLoginOpen(true);
  const closeLoginModal = () => setIsLoginOpen(false);

  const openSignupModal = () => setIsSignupOpen(true);
  const closeSignupModal = () => setIsSignupOpen(false);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/search?tag=${searchQuery.trim()}`;
    }
  };


  const handleLoginSubmit = (e) => {
    e.preventDefault();
    console.log("Login submitted");
    closeLoginModal();
  };

  const handleSignupSubmit = (e) => {
    e.preventDefault();
    console.log("Signup submitted");
    closeSignupModal();
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape") {
        closeLoginModal();
        closeSignupModal();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

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
          <button className="nav-button" onClick={openLoginModal}>
            Login
          </button>
          <span>|</span>
          <button className="nav-button" onClick={openSignupModal}>
            Sign Up
          </button>
        </nav>
      </div>

      {isSearchOpen && (
        <div className="search-container">
          <form onSubmit={handleSearchSubmit}>
            <img src={searchbar} alt="Search Icon" className="search-icon-bar" />
            <input
              type="text"
              placeholder="Search..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
            <button type="submit" className="search-btn">Search</button>
          </form>
        </div>
      )}

      {/* 로그인 모달 */}
      {isLoginOpen && (
        <div className="modal-overlay" onClick={closeLoginModal}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Login</h2>
            <form onSubmit={handleLoginSubmit}>
              <input type="email" placeholder="Email" />
              <input type="password" placeholder="Password" />
              <button type="submit" className="login-btn">
                Login
              </button>
            </form>
          </div>
        </div>
      )}

      {/* 회원가입 모달 */}
      {isSignupOpen && (
        <div className="modal-overlay" onClick={closeSignupModal}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Sign Up</h2>
            <form onSubmit={handleSignupSubmit}>
              <input type="email" placeholder="Email" />
              <input type="password" placeholder="Password" />
              <button type="submit" className="signup-btn">
                Sign Up
              </button>
            </form>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
