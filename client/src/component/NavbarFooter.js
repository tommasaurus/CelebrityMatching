import React from "react";
import "./NavbarFooter.css";

export const Navbar = ({ navigateTo }) => {
  return (
    <nav className='navbar'>
      <div className='navbar-container'>
        <a href='#' className='navbar-logo' onClick={() => navigateTo("home")}>
          PornTwin
        </a>
        <div className='navbar-buttons'>
          <button
            className='navbar-button'
            onClick={() => navigateTo("contact")}
          >
            Contact
          </button>
          <button
            className='navbar-button'
            onClick={() => navigateTo("donate")}
          >
            Donate
          </button>
        </div>
      </div>
    </nav>
  );
};

export const Footer = ({ navigateTo }) => {
  return (
    <footer className='footer'>
      <div className='footer-content'>
        <div className='footer-section'>
          <h3>Product</h3>
          <ul>
            <li>
              <a href='#' onClick={() => navigateTo("twin")}>
                Twin
              </a>
            </li>
            <li>
              <a href='#' onClick={() => navigateTo("onlyfans")}>
                OnlyFans
              </a>
            </li>
          </ul>
        </div>
        <div className='footer-section'>
          <h3>Company</h3>
          <ul>
            <li>
              <a href='#' onClick={() => navigateTo("terms")}>
                Terms of Service
              </a>
            </li>
            <li>
              <a href='#' onClick={() => navigateTo("privacy")}>
                Privacy Policy
              </a>
            </li>
          </ul>
        </div>
        <div className='footer-section'>
          <h3>Get in touch</h3>
          <div className='navbar-buttons'>
            <button
              className='navbar-button'
              onClick={() => navigateTo("contact")}
            >
              Contact
            </button>
            <button
              className='navbar-button'
              onClick={() => navigateTo("donate")}
            >
              Donate
            </button>
          </div>
        </div>
      </div>
      <div className='footer-bottom'>
        <p>&copy; 2024 PornTwin. All rights reserved.</p>
      </div>
    </footer>
  );
};
