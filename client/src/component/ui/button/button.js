// src/component/ui/button.js
import React from "react";
import "./button.css"; // Create a CSS file for button styles if needed

const Button = ({ children, className, ...props }) => {
  return (
    <button className={`btn ${className}`} {...props}>
      {children}
    </button>
  );
};

export default Button;
