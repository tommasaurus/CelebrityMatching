import React, { useState, useEffect, useRef } from "react";
import { Navbar, Footer } from "../navbar/NavbarFooter";
import "../navbar/NavbarFooter.css";
import "./Scroll.css"; 

const InfiniteScrollImages = ({ navigateTo }) => {
  const [images, setImages] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const observerRef = useRef(null);

  // Scroll to the top when the page is loaded
  useEffect(() => {
    window.scrollTo(0, 0);
    loadInitialImages();  // Load initial batch of images
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver(handleObserver, { threshold: 0.5 });
    if (observerRef.current && images.length > 0) {  // Only observe when there are images to observe
      observer.observe(observerRef.current);
    }
    return () => {
      if (observerRef.current) observer.unobserve(observerRef.current);
    };
  }, [images]);

  const loadInitialImages = async () => {
    // Load images only if not already loading
    if (loading) return;
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/random-images?count=5&page=${page}`);
      const data = await response.json();
      if (response.ok) {
        setImages(data.images);  // Set initial batch of images
        setPage((prev) => prev + 1);  // Increment the page
      } else {
        console.error("Failed to load images.");
      }
    } catch (error) {
      console.error("Error fetching images:", error);
    } finally {
      setLoading(false);  // Set loading to false after fetch
    }
  };

  // Load additional images for infinite scroll
  const loadImages = async () => {
    if (loading) return;
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/random-images?count=5&page=${page}`);
      const data = await response.json();
      if (response.ok) {
        setImages((prev) => [...prev, ...data.images]);  // Append new images to the existing ones
        setPage((prev) => prev + 1);  // Increment the page
      } else {
        console.error("Failed to load images.");
      }
    } catch (error) {
      console.error("Error fetching images:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleObserver = (entries) => {
    const target = entries[0];
    if (target.isIntersecting && !loading) {
      loadImages();
    }
  };

  return (
    <div className="scroll-page">
      <Navbar navigateTo={navigateTo} />
      <div className="scroll-container">
        <div className="image-gallery-wrapper"> {/* New wrapper for the white strip */}
          <h1 className="scroll-title">Model Gallery</h1>
          <div className="image-gallery">
            {images.length > 0 ? (
              images.map((image, index) => (
                <div key={index} className="image-wrapper">
                  <img src={`http://127.0.0.1:8000/images/${image.image_url}`} alt={`Image of ${image.name}`} />
                  <p>{image.name}</p>  {/* Display the name below the image */}
                </div>
              ))
            ) : (
              <p>No images found</p>
            )}
          </div>
          <div ref={observerRef} className="loading-indicator">
            {loading && <p>Loading more images...</p>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default InfiniteScrollImages;
