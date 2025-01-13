import React, { useState, useEffect } from "react";
import { ThemeProvider } from "./components/ThemeContext";
import "./App.css";
import Header from "./components/Header";
import Home from "./components/Home";
import Home2 from "./components/Home2";

const App = () => {
  return (
    <div className="container">
      <ThemeProvider>
        <Header />
        <Home />
        {/* <Home2 /> */}
      </ThemeProvider>
    </div>
  );
};

export default App;
