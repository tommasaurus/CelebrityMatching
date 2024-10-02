// Scroll.js
import React, { useState, useEffect, useRef } from "react";
import ModelPopup from "../ModelPopup/ModelPopup";
import "./Scroll.css";

const InfiniteScrollImages = ({ navigateTo }) => {
  const [images, setImages] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const observerRef = useRef(null);

  useEffect(() => {
    window.scrollTo(0, 0);
    loadInitialImages();
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver(handleObserver, {
      threshold: 0.5,
    });
    if (observerRef.current && images.length > 0) {
      observer.observe(observerRef.current);
    }
    return () => {
      if (observerRef.current) observer.unobserve(observerRef.current);
    };
  }, [images]);

  const loadInitialImages = async () => {
    if (loading) return;
    setLoading(true);
    try {
      const response = await fetch(
        `http://${process.env.REACT_APP_BACKEND_IP}:80/random-images?count=5&page=${page}`
      );
      const data = await response.json();
      if (response.ok) {
        setImages(data.images);
        setPage((prev) => prev + 1);
      } else {
        console.error("Failed to load images.");
      }
    } catch (error) {
      console.error("Error fetching images:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadImages = async () => {
    if (loading) return;
    setLoading(true);
    try {
      const response = await fetch(
        `http://${process.env.REACT_APP_BACKEND_IP}:80/random-images?count=5&page=${page}`
      );
      const data = await response.json();
      if (response.ok) {
        setImages((prev) => [...prev, ...data.images]);
        setPage((prev) => prev + 1);
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

  const handleImageClick = (image) => {
    setSelectedModel(image);
  };

  const closeModelPopup = () => {
    setSelectedModel(null);
  };

  return (
    <div className="scroll-page">
      <div className="scroll-container">
        <div className="image-gallery-wrapper">
          <h1 className="scroll-title">Model Gallery</h1>
          <div className="image-gallery">
            {images.length > 0 ? (
              images.map((image, index) => (
                <div
                  key={index}
                  className="image-wrapper"
                  onClick={() => handleImageClick(image)}
                >
                  <img
                    src={image.image_url}
                    alt={`Image of ${image.name}`}
                  />
                  <p>{image.name}</p>
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

      {/* Render ModelPopup when a model is selected */}
      {selectedModel && (
        <ModelPopup model={selectedModel} onClose={closeModelPopup} />
      )}
    </div>
  );
};

export default InfiniteScrollImages;
