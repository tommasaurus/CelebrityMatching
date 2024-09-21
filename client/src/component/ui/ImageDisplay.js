import React, { useState, useEffect } from 'react';

function ImageDisplay({ imageName, modelId }) {
    const [imageSrc, setImageSrc] = useState('');
    const [socialLinks, setSocialLinks] = useState(null);

    useEffect(() => {
        // Construct the image URL using the FastAPI endpoint
        const imageUrl = `http://127.0.0.1:8000/images/${imageName}`;
        setImageSrc(imageUrl);
    }, [imageName]);

    useEffect(() => {
        // Fetch the social links using the modelId
        const fetchSocialLinks = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/get-social-links/${modelId}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch social links');
                }
                const data = await response.json();
                setSocialLinks(data.social_links);
                console.log(data)
            } catch (error) {
                console.error('Error fetching social links:', error);
            }
        };

        if (modelId) {
            fetchSocialLinks();
        }
    }, [modelId]);

    return (
        <div className="image-display">
            {imageSrc ? (
                <img src={imageSrc} alt="Matched Celebrity" />
            ) : (
                <p>Loading image...</p>
            )}
            
            {/* Display social links as hidden fields */}
            {socialLinks && (
                <div className="social-links">
                    <input type="hidden" name="name" value={socialLinks.name} />
                    {socialLinks.www && <input type="hidden" name="www" value={socialLinks.www} />}
                    {socialLinks.instagram && <input type="hidden" name="instagram" value={socialLinks.instagram} />}
                    {socialLinks.onlyfans && <input type="hidden" name="onlyfans" value={socialLinks.onlyfans} />}
                    {socialLinks.onlyfansfree && <input type="hidden" name="onlyfansfree" value={socialLinks.onlyfansfree} />}
                    {socialLinks.mym && <input type="hidden" name="mym" value={socialLinks.mym} />}
                    {socialLinks.tiktok && <input type="hidden" name="tiktok" value={socialLinks.tiktok} />}
                    {socialLinks.x && <input type="hidden" name="x" value={socialLinks.x} />}
                    {socialLinks.facebook && <input type="hidden" name="facebook" value={socialLinks.facebook} />}
                    {socialLinks.twitch && <input type="hidden" name="twitch" value={socialLinks.twitch} />}
                    {socialLinks.youtube && <input type="hidden" name="youtube" value={socialLinks.youtube} />}
                    {socialLinks.imdb && <input type="hidden" name="imdb" value={socialLinks.imdb} />}
                    {socialLinks.fansly && <input type="hidden" name="fansly" value={socialLinks.fansly} />}
                    {socialLinks.other && <input type="hidden" name="other" value={socialLinks.other} />}
                </div>
            )}
        </div>
    );
}

export default ImageDisplay;
