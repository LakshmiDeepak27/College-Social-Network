// File: src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Alumni from './pages/Alumni';
import Navbar from './components/layout/Navbar';

const App = () => {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/profile/:userId" element={<Profile />} />
            <Route path="/alumni" element={<Alumni />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;