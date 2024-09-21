import React, { useState, useRef } from "react";
import axios from "axios";
import {
  Upload,
  FileText,
  Zap,
  Lock,
  User,
  Cpu,
  CheckCircle,
  AlertCircle,
  X,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import "./Hero.css";
import { Navbar, Footer } from "./NavbarFooter";
import ImageDisplay from "./ui/ImageDisplay";

const Hero = ({ navigateTo }) => {
  const [file, setFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [matches, setMatches] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [showAllMatches, setShowAllMatches] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      const uploadedFile = event.target.files[0];
      setFile(uploadedFile);
      setFilePreview(URL.createObjectURL(uploadedFile));
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      setFile(droppedFile);
      setFilePreview(URL.createObjectURL(droppedFile));
    }
  };

  const handleDeleteFile = () => {
    setFile(null);
    setFilePreview(null);
    fileInputRef.current.value = "";
  };

  const handleUploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      const response = await axios.post(
        "http://127.0.0.1:8000/upload-image/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(response.data);
      setMatches(response.data.onlyfans_matches);
    } catch (error) {
      console.error("Error uploading image:", error);
    } finally {
      setUploading(false);
    }
  };

  const instructions = [
    {
      icon: <User size={32} />,
      title: "Upload a photo",
      description:
        "Use a clear frontal photo with only one person. Face should be clearly visible for best results.",
    },
    {
      icon: <Cpu size={32} />,
      title: "Face Detection",
      description:
        "Our system detects facial features including eyebrows, eyes, nose, and mouth.",
    },
    {
      icon: <CheckCircle size={32} />,
      title: "Enjoy the result!",
      description:
        "Our Neural Network compares your face with celebrities and suggests the most similar ones.",
    },
  ];

  const toggleShowAllMatches = () => {
    setShowAllMatches(!showAllMatches);
  };

  return (
    <>
      <Navbar navigateTo={navigateTo} />
      <div className='hero-container'>
        <div className='hero-database-section'>
          <p className='hero-skinny-description'>
            Find your identical Star using AI
          </p>
          <h2 className='hero-database-text'>Over 500+ Stars!</h2>
        </div>

        <div className='hero-content'>
          <h1 className='hero-title'>Twin</h1>
          <p className='hero-subtitle'>No data saved. 18+ to use.</p>

          <div
            className={`upload-area ${isDragging ? "dragging" : ""}`}
            onClick={handleUploadClick}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <div className='upload-icon'>
              <Upload size={48} />
            </div>
            <p className='upload-text'>Upload your photo</p>
            <p className='upload-subtext'>
              {isDragging ? "Drop here" : "Click to browse or drag and drop"}
            </p>
            <input
              type='file'
              className='file-input'
              onChange={handleFileChange}
              ref={fileInputRef}
              accept='image/*'
              style={{ display: "none" }}
            />
          </div>

          {file && (
            <div className='selected-file'>
              <span>{file.name}</span>
              <button className='delete-file' onClick={handleDeleteFile}>
                <X size={16} />
              </button>
            </div>
          )}

          <button
            className='upload-button'
            onClick={handleUploadFile}
            disabled={!file || uploading}
          >
            {uploading ? "Uploading..." : "Find Twin"}
          </button>

          {filePreview && (
            <div className='image-preview'>
              <h3>Your Uploaded Image</h3>
              <img
                src={filePreview}
                alt='Uploaded Preview'
                className='preview-image'
              />
            </div>
          )}

          <div className='features'>
            <div className='feature'>
              <FileText size={20} />
              <span>No data saved</span>
            </div>
            <div className='feature'>
              <Zap size={20} />
              <span>AI processing</span>
            </div>
            <div className='feature'>
              <Lock size={20} />
              <span>Private and Secure</span>
            </div>
          </div>
        </div>

        {matches.length > 0 && (
          <div className='top-matches'>
            <h2>Your Top Matches</h2>
            <div className='matches-container'>
              {matches.slice(0, showAllMatches ? 5 : 3).map((match, index) => (
                <div key={index} className={`match match-${index + 1}`}>
                  <ImageDisplay
                    imageName={match.image_path}
                    modelId={match.model_id}
                    alt={`${match.name} preview`}
                    width={300}
                    height={300}
                  />
                  <div className='match-content'>
                    <p>{match.name}</p>
                    <p>Similarity: {(match.similarity * 100).toFixed(2)}%</p>
                  </div>
                </div>
              ))}
            </div>
            {matches.length > 3 && (
              <button
                className='view-more-button'
                onClick={toggleShowAllMatches}
              >
                {showAllMatches ? (
                  <>
                    <ChevronUp size={20} />
                    Show Less
                  </>
                ) : (
                  <>
                    <ChevronDown size={20} />
                    View More
                  </>
                )}
              </button>
            )}
          </div>
        )}

        <div className='instruction-section'>
          <h2 className='instruction-title'>How It Works</h2>
          <div className='instruction-blocks'>
            {instructions.map((instruction, index) => (
              <div key={index} className='instruction-block'>
                <div className='instruction-icon'>{instruction.icon}</div>
                <h3 className='instruction-block-title'>{instruction.title}</h3>
                <p className='instruction-block-description'>
                  {instruction.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className='beta-info-section'>
          <div className='beta-info-content'>
            <h3 className='beta-info-title'>
              <AlertCircle size={24} /> Beta Version
            </h3>
            <p className='beta-info-text'>
              We're currently in beta, constantly improving our recognition
              algorithm. Every request you make helps train our neural network,
              so please share with friends! We're committed to high accuracy,
              using multiple angles to create detailed actress templates. Our
              team works daily to refine the system and correct any errors.
            </p>
            <p className='beta-info-highlight'>
              Exciting news: New stars added weekly!
            </p>
          </div>
        </div>
        <div className='onlyfans-twin-announcement'>
          <h2>OnlyfansTwin coming soon...</h2>
        </div>
      </div>
      <Footer navigateTo={navigateTo} />
    </>
  );
};

export default Hero;
