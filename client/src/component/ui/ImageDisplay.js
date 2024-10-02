import React, { useState, useEffect } from 'react';

function ImageDisplay({ imageName, modelId, onImageClick }) {  // Added onImageClick prop
    const [imageSrc, setImageSrc] = useState('');

    useEffect(() => {
        // Fetch the pre-signed URL from the FastAPI endpoint
        const fetchImageUrl = async () => {
            try {
                const response = await fetch(`http://${process.env.REACT_APP_BACKEND_IP}:80/images/${encodeURIComponent(imageName)}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch image URL');
                }

                const data = await response.json();
                const imageUrl = data.image_url;

                setImageSrc(imageUrl);
            } catch (error) {
                console.error('Error fetching image URL:', error);
            }
        };

        if (imageName) {
            fetchImageUrl();
        }
    }, [imageName]);

    // Handle image click
    const handleImageClick = () => {
        if (onImageClick) {
            onImageClick(imageSrc, modelId);
        }
    };

    return (
        <div className="image-display" onClick={handleImageClick}>  
            {imageSrc ? (
                <img src={imageSrc} alt="Matched Celebrity" />
            ) : (
                <p>Loading image...</p>
            )}
        </div>
    );
}

export default ImageDisplay;