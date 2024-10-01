// ImageDisplay.js

import React, { useState, useEffect } from 'react';

function ImageDisplay({ imageName, modelId, onImageClick }) {  // Added onImageClick prop
    const [imageSrc, setImageSrc] = useState('');
    const [socialLinks, setSocialLinks] = useState(null);

    useEffect(() => {
        // Fetch the image from the FastAPI endpoint
        const fetchImage = async () => {
            try {
                const response = await fetch(`http://${process.env.REACT_APP_BACKEND_IP}:80/images/${encodeURIComponent(imageName)}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch image');
                }

                // Convert the response to a Blob
                const blob = await response.blob();

                // Create a local URL for the Blob and set it as the image source
                const imageUrl = URL.createObjectURL(blob);

                setImageSrc(imageUrl);
            } catch (error) {
                console.error('Error fetching image:', error);
            }
        };

        if (imageName) {
            fetchImage();
        }
    }, [imageName]);

    // No need to fetch social links here since it's done in MatchPopup

    // Handle image click
    const handleImageClick = () => {
        if (onImageClick) {
            onImageClick(imageSrc, modelId);
        }
    };

    return (
        <div className="image-display" onClick={handleImageClick}>  {/* Added onClick */}
            {/* Removed Image Source debug text */}
            {imageSrc ? (
                <img src={imageSrc} alt="Matched Celebrity" />
            ) : (
                <p>Loading image...</p>
            )}
        </div>
    );
}

export default ImageDisplay;
