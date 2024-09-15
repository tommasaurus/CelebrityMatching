import React from "react";
import "./Navbar.css";

const Navbar = ({ navigateTo }) => {
  return (
    <nav className='navbar'>
      <div className='navbar-container'>
        <a href='#' className='navbar-logo' onClick={() => navigateTo("home")}>
          PornTwin
        </a>
        <ul className='navbar-menu'>
          <li className='navbar-item'>
            <a
              href='#'
              className='navbar-link'
              onClick={() => navigateTo("home")}
            >
              Home
            </a>
          </li>
          <li className='navbar-item'>
            <a
              href='#'
              className='navbar-link'
              onClick={() => navigateTo("contact")}
            >
              Contact
            </a>
          </li>
          <li className='navbar-item'>
            <a
              href='#'
              className='navbar-link'
              onClick={() => navigateTo("donate")}
            >
              Donate
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
