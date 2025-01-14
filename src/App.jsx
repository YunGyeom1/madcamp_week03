import React, { useState, useEffect } from "react";
import { ThemeProvider } from "./components/ThemeContext";
import "./App.css";
import Header from "./components/Header";
import Home from "./components/Home";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

const App = () => {
  return (
    <Router>
      <div className="container">
        <ThemeProvider>
          <Header />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<Home />} />
          </Routes>
        </ThemeProvider>
      </div>
    </Router>
  );
};

export default App;
