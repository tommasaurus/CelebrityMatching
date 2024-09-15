// src/component/ui/card.js
import React from "react";
import "./card.css"; // Create a CSS file for card styles if needed

export const Card = ({ children, className }) => {
  return <div className={`card ${className}`}>{children}</div>;
};

export const CardContent = ({ children, className }) => {
  return <div className={`card-content ${className}`}>{children}</div>;
};
