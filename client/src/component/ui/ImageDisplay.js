import React, { useState, useEffect } from 'react';

function ImageDisplay({ imageName }) {
    const [imageSrc, setImageSrc] = useState('');

    useEffect(() => {
        // Construct the image URL using the FastAPI endpoint
        const imageUrl = `http://127.0.0.1:8000/images/${imageName}`;
        setImageSrc(imageUrl);
    }, [imageName]);

    return (
        <div className="image-display">
            {imageSrc ? (
                <img src={imageSrc} alt="Matched Celebrity" />
            ) : (
                <p>Loading image...</p>
            )}
        </div>
    );
}

export default ImageDisplay;
