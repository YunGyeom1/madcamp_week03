import React, { useState, useEffect } from "react";
import { ThemeProvider } from "./components/ThemeContext";
import "./App.css";
import Header from "./components/Header";
import Home from "./components/Home";

const App = () => {
  return (
    <div className="container">
      <ThemeProvider>
        <Header />
        <Home />
      </ThemeProvider>
    </div>
  );
};

export default App;
