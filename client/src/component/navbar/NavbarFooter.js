import React from "react";
import logoImage from "/Users/RDua/Desktop/a/Code/CelebrityMatching/client/src/OFlogo.png";
import "./NavbarFooter.css";

export const Navbar = ({ navigateTo }) => {
  const handleHowItWorksClick = () => {
    const scrollPosition = window.innerHeight * 0.7;
    window.scrollTo({
      top: scrollPosition,
      behavior: "smooth",
    });
  };

  return (
    <nav className='navbar'>
      <div className='logo'>
        <button onClick={() => navigateTo("home")} className='logo-button'>
          <img
            src={logoImage}
            alt='OnlyFans Finder Logo'
            className='logo-image'
          />
        </button>
      </div>
      <div className='nav-links'>
        <button
          className='nav-button how-it-works'
          onClick={() => navigateTo("scroll")}
        >
          Gallery
        </button>
        <button className='nav-button' onClick={() => navigateTo("contact")}>
          Contact
        </button>
        <button className='nav-button sign-in'>Sign in</button>
      </div>
    </nav>
  );
};

export const Footer = ({ navigateTo }) => {
  return (
    <footer className='footer'>
      <div className='footer-content'>
        <div className='footer-logo'>
          <button onClick={() => navigateTo("home")} className='logo-button'>
            <img
              src={logoImage}
              alt='OnlyFans Finder Logo'
              className='logo-image'
            />
          </button>
        </div>
        <div className='footer-sections'>
          <div className='footer-section'>
            <h4>Product</h4>
            <ul>
              <li>
                <button
                  onClick={() => navigateTo("home")}
                  className='footer-button'
                >
                  Finder
                </button>
              </li>
              <li>
                <button
                  onClick={() => navigateTo("scroll")}
                  className='footer-button'
                >
                  Gallery
                </button>
              </li>
            </ul>
          </div>
          <div className='footer-section'>
            <h4>Company</h4>
            <ul>
              <li>
                <button
                  onClick={() => navigateTo("privacy-policy")}
                  className='footer-button'
                >
                  Privacy Policy
                </button>
              </li>
              <li>
                <button
                  onClick={() => navigateTo("terms-of-service")}
                  className='footer-button'
                >
                  Terms of Service
                </button>
              </li>
            </ul>
          </div>
          <div className='footer-section'>
            <h4>Get in touch</h4>
            <ul>
              <li>
                <button
                  onClick={() => navigateTo("contact")}
                  className='footer-button'
                >
                  Contact
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div className='footer-bottom'>
        <hr className='footer-line' />
        <p className='copyright'>
          &copy; 2024 OnlyFans Finder. All rights reserved.
        </p>
      </div>
    </footer>
  );
};
