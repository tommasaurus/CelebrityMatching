// ModelPopup.js
import React, { useEffect, useState } from "react";
import { X } from "lucide-react";
import {
  FaInstagram,
  FaTwitter,
  FaFacebook,
  FaYoutube,
  FaImdb,
  FaTiktok,
  FaTwitch,
} from "react-icons/fa";
import { SiOnlyfans } from "react-icons/si";
import { BsGlobe } from "react-icons/bs";
import "./ModelPopup.css";

const ModelPopup = ({ model, onClose }) => {
  const [isVisible, setIsVisible] = useState(false);
  const [socialLinks, setSocialLinks] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  useEffect(() => {
    const fetchSocialLinks = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(
          `http://${process.env.REACT_APP_BACKEND_IP}:80/get-social-links-by-name/${encodeURIComponent(
            model.name
          )}`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch social links");
        }
        const data = await response.json();
        setSocialLinks(data.social_links);
      } catch (error) {
        console.error("Error fetching social links:", error);
      } finally {
        setIsLoading(false);
      }
    };

    if (model.name) {
      fetchSocialLinks();
    }
  }, [model.name]);

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        handleClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  const handleClose = () => {
    setIsVisible(false);
    setTimeout(onClose, 300); // Wait for the fade-out animation to complete
  };

  const socialPlatforms = [
    { name: "instagram", icon: FaInstagram, color: "#E1306C" },
    { name: "twitter", icon: FaTwitter, color: "#1DA1F2" },
    { name: "facebook", icon: FaFacebook, color: "#4267B2" },
    { name: "youtube", icon: FaYoutube, color: "#FF0000" },
    { name: "imdb", icon: FaImdb, color: "#F5C518" },
    { name: "onlyfans", icon: SiOnlyfans, color: "#00AFF0" },
    { name: "fansly", icon: BsGlobe, color: "#00AFF0" },
    { name: "tiktok", icon: FaTiktok, color: "#010101" },
    { name: "twitch", icon: FaTwitch, color: "#9146FF" },
    { name: "www", icon: BsGlobe, color: "#4A90E2" },
    { name: "onlyfansfree", icon: SiOnlyfans, color: "#00AFF0" },
    { name: "mym", icon: BsGlobe, color: "#00AFF0" },
    { name: "x", icon: FaTwitter, color: "#000000" },
    { name: "other", icon: BsGlobe, color: "#4A90E2" },
  ];

  return (
    <div
      className={`model-popup-overlay ${isVisible ? "visible" : ""}`}
      role="dialog"
      aria-modal="true"
      aria-labelledby="model-popup-title"
    >
      <div className={`model-popup-content ${isVisible ? "visible" : ""}`}>
        <button className="model-popup-close" onClick={handleClose}>
          <X size={24} />
        </button>
        <div className="model-popup-image">
          {model.image_url ? (
            <img src={model.image_url} alt={`${model.name}`} />
          ) : (
            <p>Loading image...</p>
          )}
        </div>
        <div className="model-popup-info">
          <h2 id="model-popup-title">{model.name}</h2>
          <div className="model-popup-social-links">
            {isLoading && <p>Loading social links...</p>}
            {!isLoading && socialLinks && (
              <>
                {socialPlatforms.map(
                  (platform) =>
                    socialLinks[platform.name] && (
                      <a
                        key={platform.name}
                        href={socialLinks[platform.name]}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="social-button"
                        style={{ backgroundColor: platform.color }}
                      >
                        <platform.icon size={20} />
                        <span>{platform.name}</span>
                      </a>
                    )
                )}
              </>
            )}
            {!isLoading && !socialLinks && <p>No social links found.</p>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelPopup;
