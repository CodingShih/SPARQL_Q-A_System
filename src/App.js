// src/App.js
import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Posts from './components/Posts';
import About from './components/About';
import SPARQLQA from './components/SPARQLQA';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="main-content">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/posts" element={<Posts />} />
        <Route path="/about" element={<About />} />
        <Route path="/qa-system" element={<SPARQLQA />} /> 
      </Routes>
      </div>
 </Router>
  );
}

export default App;



