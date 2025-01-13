import React, { useState, useEffect } from "react";
import "./App.css";
import Header from "./components/Header";
import Home from "./components/Home";

const App = () => {
  return (
    <div className="container">
      <Header />
      <Home />
    </div>
  );
};

export default App;