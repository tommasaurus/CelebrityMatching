import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import {
  Upload,
  FileText,
  Zap,
  Lock,
  ChevronLeft,
  ChevronRight,
  CheckCircle,
  AlertCircle,
  X,
  Loader,
  ChevronDownCircle,
  ChevronUpCircle,
} from "lucide-react";
import "./Hero.css";
import ImageDisplay from "../ui/ImageDisplay";
import MatchPopup from "../MatchPopup/MatchPopup";
import logo from "/Users/tommyqu/CelebrityMatching/client/src/OFlogo.png";
import Contact from "../contact/Contact";

const Hero = ({ navigateTo }) => {
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [file, setFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [matches, setMatches] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [showAllMatches, setShowAllMatches] = useState(false);
  const [conversionCount, setConversionCount] = useState(12465);
  const [fileSize, setFileSize] = useState(64);
  const [showViewMatchesButton, setShowViewMatchesButton] = useState(false);
  const [matchesLoaded, setMatchesLoaded] = useState(false);
  const fileInputRef = useRef(null);
  const matchesRef = useRef(null);
  const galleryRef = useRef(null);

  const [currentImage, setCurrentImage] = useState(0);
  const [isHoveringCaption, setIsHoveringCaption] = useState(false);
  const carouselImages = [
    { src: "emma.png", name: "Emma Watson" },
    { src: "irina.png", name: "Irina Shayk" },
    { src: "scarlett.png", name: "Scarlett Johansson" },
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setConversionCount((prevCount) => prevCount + 1);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % carouselImages.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      const uploadedFile = event.target.files[0];
      setFile(uploadedFile);
      setFilePreview(URL.createObjectURL(uploadedFile));
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
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
    setShowViewMatchesButton(false);
    setMatchesLoaded(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleUploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      setShowViewMatchesButton(false);
      const response = await axios.post(
        `http://${process.env.REACT_APP_BACKEND_IP}:80/upload-image/`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(response.data);
      setMatches(response.data.matches);
      setShowViewMatchesButton(true);
      setMatchesLoaded(true);
    } catch (error) {
      console.error("Error uploading image:", error);
    } finally {
      setUploading(false);
    }
  };

  const toggleShowAllMatches = () => {
    setShowAllMatches(!showAllMatches);
  };

  const handleMatchClick = (match, imageSrc) => {
    setSelectedMatch({
        ...match,
        imageSrc,  // Use the blob URL
    });
  };


  const closeMatchPopup = () => {
    setSelectedMatch(null);
  };

  const handleNext = (e) => {
    e.stopPropagation();
    setCurrentImage((prev) => (prev + 1) % carouselImages.length);
  };

  const handlePrev = (e) => {
    e.stopPropagation();
    setCurrentImage(
      (prev) => (prev - 1 + carouselImages.length) % carouselImages.length
    );
  };

  const handleCarouselImageClick = async (imageSrc, imageName) => {
    if (!isHoveringCaption) {
      try {
        // Assuming the images are preloaded locally, no need to fetch the images again
        const file = new File(
          [imageSrc],
          `${imageName.toLowerCase().replace(" ", "_")}.png`,
          {
            type: "image/png",
          }
        );
        setFile(file);
        setFilePreview(imageSrc); // Use the clicked image's source for the preview
        await handleUploadFile(); // This function should handle the file upload
      } catch (error) {
        console.error("Error uploading carousel image:", error);
      } finally {
        setUploading(false);
      }
    }
  };

  const handleGalleryClick = () => {
    navigateTo("scroll");
  };

  const scrollToMatches = () => {
    if (matchesRef.current) {
      matchesRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <>
      <div className='hero-container'>
        <img src={logo} alt='Logo' className='hero-logo' />
        <p className='hero-subtitle'>
          Find your OnlyFans Model doppelgänger by uploading your portrait.
        </p>
        {!filePreview ? (
          <div className='hero-content'>
            <div className='upload-section'>
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
                  Click to browse or drag and drop
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
            </div>

            <div className='or-divider'>
              <div className='or-line'></div>
              <div className='or-text'>OR</div>
              <div className='or-line'></div>
            </div>

            <div className='carousel-section'>
              <div className='carousel'>
                {carouselImages.map((image, index) => (
                  <div
                    key={index}
                    className={`carousel-item ${
                      currentImage === index ? "active" : ""
                    }`}
                    onClick={() =>
                      handleCarouselImageClick(image.src, image.name)
                    }
                  >
                    <img
                      src={image.src}
                      alt={`Carousel ${index + 1}`}
                      className='carousel-image'
                    />
                    <div
                      className='carousel-caption'
                      onMouseEnter={() => setIsHoveringCaption(true)}
                      onMouseLeave={() => setIsHoveringCaption(false)}
                    >
                      <button className='carousel-btn' onClick={handlePrev}>
                        <ChevronLeft size={24} />
                      </button>
                      <span className='carousel-name'>{image.name}</span>
                      <button className='carousel-btn' onClick={handleNext}>
                        <ChevronRight size={24} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className='uploaded-image-container'>
            <h3 className='uploaded-image-title'>Your uploaded image:</h3>
            <img
              src={filePreview}
              alt='Uploaded Preview'
              className='uploaded-image'
            />
            <div className='file-name-container'>
              <span className='file-name'>{file.name}</span>
              <button className='delete-file' onClick={handleDeleteFile}>
                <X size={16} />
              </button>
            </div>
          </div>
        )}
        <div className='action-buttons'>
          {file && !filePreview && (
            <div className='selected-file'>
              <span>{file.name}</span>
            </div>
          )}
          {file && (
            <button
              className={`upload-button ${
                matchesLoaded ? "matches-loaded" : ""
              }`}
              onClick={matchesLoaded ? scrollToMatches : handleUploadFile}
              disabled={uploading}
            >
              {uploading
                ? "Uploading..."
                : matchesLoaded
                ? "Matches"
                : "Find Model"}
            </button>
          )}
        </div>
        {uploading && (
          <div className='loading-spinner'>
            <Loader size={24} />
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
        {matches.length > 0 && (
          <div className='top-matches' ref={matchesRef}>
            <h2>Your Top Matches</h2>
            <div className='matches-container'>
              {matches.slice(0, showAllMatches ? 5 : 3).map((match, index) => (
                <div
                  key={index}
                  className={`match match-${index + 1}`}                  
                >
                  <ImageDisplay
                    imageName={match.image_url}
                    modelId={match.model_id}
                    alt={`${match.name} preview`}
                    width={300}
                    height={300}
                    onImageClick={(imageSrc) => handleMatchClick(match, imageSrc)}  
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
                    <ChevronUpCircle size={20} />
                    Show Less
                  </>
                ) : (
                  <>
                    <ChevronDownCircle size={20} />
                    View More
                  </>
                )}
              </button>
            )}
          </div>
        )}
        <div className='conversion-stats'>
          <p>
            We've already converted{" "}
            <span className='animated-number'>
              {conversionCount.toLocaleString()}
            </span>{" "}
            files with a total size of{" "}
            <span className='animated-number'>{fileSize.toLocaleString()}</span>{" "}
            TB.
          </p>
        </div>
        <div className='gallery-stats'>
          <p>
            View our gallery with{" "}
            <span className='animated-number'>15,000+</span> images{" "}
            <button className='gallery-button' onClick={handleGalleryClick}>
              Gallery
            </button>
          </p>
        </div>
        <div className='instruction-section'>
          <h2 className='instruction-title'>How It Works</h2>
          <div className='instruction-blocks'>
            {[
              {
                icon: <Upload size={32} />,
                title: "Upload a photo",
                description:
                  "Use a clear frontal photo with only one person. Face should be clearly visible for best results.",
              },
              {
                icon: <ChevronRight size={32} />,
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
            ].map((instruction, index) => (
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
          <h3 className='beta-info-title'>
            <AlertCircle size={24} /> Beta Version
          </h3>
          <p className='beta-info-text'>
            We're currently in beta, constantly improving our recognition
            algorithm. Every request you make helps train our neural network, so
            please share with friends! We're committed to high accuracy, using
            multiple angles to create detailed actress templates. Our team works
            daily to refine the system and correct any errors.
          </p>
          <p className='beta-info-highlight'>
            Exciting news: New models added weekly!
          </p>
        </div>

        {selectedMatch && (
          <MatchPopup match={selectedMatch} onClose={closeMatchPopup} />
        )}
      </div>
    </>
  );
};

export default Hero;
