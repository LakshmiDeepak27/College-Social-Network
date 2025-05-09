import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">Konnectia</Link>
      </div>
      <div className="navbar-links">
        <Link to="/" className="navbar-link">Dashboard</Link>
        <Link to="/alumni" className="navbar-link">Alumni</Link>
        <Link to="/profile/1" className="navbar-link">Profile</Link>
      </div>
    </nav>
  );
};

export default Navbar; 